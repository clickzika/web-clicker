"""
Web Clicker — Opens a browser, fills in login credentials, clicks submit,
and runs a configurable sequence of post-login steps defined in config.py.
"""

import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import config


# ── Locator strategy mapping ─────────────────────────────────
BY_MAP = {
    "css":   By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "id":    By.ID,
    "name":  By.NAME,
    "class": By.CLASS_NAME,
    "tag":   By.TAG_NAME,
}


class SkipGroup(Exception):
    """Raised by check_file when the file is missing — signals run_steps to skip to the next group."""
    pass


def build_driver(headless: bool) -> webdriver.Chrome:
    """Create and return a Chrome WebDriver in headless or headed mode."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        print("[Browser] Headless mode — no browser window")
    else:
        print("[Browser] Headed mode — browser window visible")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def resolve_locator(selector: dict) -> tuple:
    """Convert a selector config dict to a (By, value) tuple for Selenium."""
    by_key = selector["by"].lower()
    value = selector["value"]

    if by_key == "text":
        xpath = (
            f"//*[self::button or self::a or self::input]"
            f"[normalize-space(.)='{value}' or @value='{value}']"
        )
        return (By.XPATH, xpath)
    elif by_key in BY_MAP:
        return (BY_MAP[by_key], value)
    else:
        raise ValueError(
            f"Unknown by='{by_key}'. Supported: {list(BY_MAP.keys()) + ['text']}"
        )


def _to_css(selector: dict) -> str:
    """Convert a selector config dict to a CSS string for CDP DOM.querySelector."""
    by_key = selector["by"].lower()
    val = selector["value"]
    if by_key == "id":
        return f"#{val}"
    elif by_key == "css":
        return val
    elif by_key == "name":
        return f"[name='{val}']"
    return val


def wait_and_find(driver: webdriver.Chrome, selector: dict, timeout: int):
    """Wait until an element is clickable and return it."""
    locator = resolve_locator(selector)
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_visible(driver: webdriver.Chrome, selector: dict, timeout: int):
    """Wait until an element is visible and return it."""
    locator = resolve_locator(selector)
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


# ── Action handlers ──────────────────────────────────────────

def _do_check_file(driver, step, timeout):
    path = step["file"]
    if not os.path.exists(path):
        print(f"        File not found: {path}")
        print("        Skipping this group → moving to next group")
        raise SkipGroup()
    print(f"        File found: {path} ✓")


def _do_click(driver, step, timeout):
    el = wait_and_find(driver, step["selector"], timeout)
    print(f"        Found button: {el.text.strip()}")
    el.click()
    print("        Clicked ✓")


def _do_type(driver, step, timeout):
    el = wait_visible(driver, step["selector"], timeout)
    el.clear()
    el.send_keys(step["text"])
    print(f"        Typed: {step['text']}")


def _do_navigate(driver, step, timeout):
    driver.get(step["url"])
    print(f"        Navigated to: {step['url']}")
    print(f"        Page title: {driver.title}")


def _do_wait(driver, step, timeout):
    secs = step["seconds"]
    print(f"        Waiting {secs}s...")
    time.sleep(secs)


def _do_screenshot(driver, step, timeout):
    driver.save_screenshot(step["filename"])
    print(f"        Screenshot saved: {step['filename']} ✓")


def _do_assert_url(driver, step, timeout):
    contains = step["contains"]
    current = driver.current_url
    if contains not in current:
        print(f"        [ERROR] assert_url failed")
        print(f"                Expected to contain: '{contains}'")
        print(f"                Current URL: {current}")
        sys.exit(1)
    print(f"        URL contains '{contains}' ✓")


def _do_js(driver, step, timeout):
    result = driver.execute_script(step["script"])
    print("        JS executed ✓")
    if result is not None:
        print(f"        Result: {result}")


def _do_upload(driver, step, timeout):
    css_sel = _to_css(step["selector"])
    doc = driver.execute_cdp_cmd("DOM.getDocument", {})
    result = driver.execute_cdp_cmd("DOM.querySelector", {
        "nodeId": doc["root"]["nodeId"],
        "selector": css_sel,
    })
    node_id = result["nodeId"]
    if node_id == 0:
        raise ValueError(f"upload: element '{css_sel}' not found in DOM")
    driver.execute_cdp_cmd("DOM.setFileInputFiles", {
        "files": [step["file"]],
        "nodeId": node_id,
    })
    print(f"        File sent: {step['file']} ✓")


HANDLERS = {
    "check_file": _do_check_file,
    "click":      _do_click,
    "type":       _do_type,
    "navigate":   _do_navigate,
    "wait":       _do_wait,
    "screenshot": _do_screenshot,
    "assert_url": _do_assert_url,
    "js":         _do_js,
    "upload":     _do_upload,
}


def run_steps(driver: webdriver.Chrome, steps: list, timeout: int):
    """Run each step in POST_LOGIN_STEPS in order."""
    if not steps:
        return

    print(f"\n[Post-Login] Running {len(steps)} steps")
    idx = 0
    while idx < len(steps):
        step = steps[idx]
        action = step.get("action", "").lower()
        print(f"\n  [{idx + 1}/{len(steps)}] action: {action}")

        handler = HANDLERS.get(action)
        if handler is None:
            raise ValueError(
                f"Unknown action='{action}'. Supported: {', '.join(HANDLERS)}"
            )

        try:
            handler(driver, step, timeout)
        except SkipGroup:
            idx += 1
            while idx < len(steps) and steps[idx].get("action", "").lower() != "check_file":
                print(f"\n  [{idx + 1}/{len(steps)}] action: {steps[idx].get('action')} — skipped")
                idx += 1
            continue

        idx += 1


def run():
    print("=" * 50)
    print("  Web Clicker — Login")
    print("=" * 50)
    print(f"URL      : {config.URL}")
    print(f"Username : {config.USERNAME}")
    print(f"Password : {'*' * len(config.PASSWORD)}")
    print(f"Headless : {config.HEADLESS}")
    print("=" * 50)

    driver = build_driver(headless=config.HEADLESS)

    try:
        # Step 1: Open website
        print(f"\n[1/4] Opening: {config.URL}")
        driver.get(config.URL)
        print(f"      Page title: {driver.title}")

        # Step 2: Fill username
        print(f"\n[2/4] Filling username")
        username_field = wait_visible(driver, config.USERNAME_SELECTOR, config.WAIT_TIMEOUT)
        username_field.clear()
        username_field.send_keys(config.USERNAME)
        print(f"      Entered: {config.USERNAME}")

        # Step 3: Fill password
        print(f"\n[3/4] Filling password")
        password_field = wait_visible(driver, config.PASSWORD_SELECTOR, config.WAIT_TIMEOUT)
        password_field.clear()
        password_field.send_keys(config.PASSWORD)
        print(f"      Entered: {'*' * len(config.PASSWORD)}")

        # Step 4: Click login button
        print(f"\n[4/4] Clicking login button")
        submit_btn = wait_and_find(driver, config.BUTTON_SELECTOR, config.WAIT_TIMEOUT)
        print(f"      Found: <{submit_btn.tag_name}> text='{submit_btn.text.strip()}'")
        submit_btn.click()
        print("      Clicked ✓")

        time.sleep(config.WAIT_AFTER_CLICK)

        run_steps(driver, config.POST_LOGIN_STEPS, config.WAIT_TIMEOUT)

        print(f"\n[Done]")
        print(f"  Current URL : {driver.current_url}")
        print(f"  Page title  : {driver.title}")

    except TimeoutException as e:
        print(f"\n[ERROR] Timeout — element not found within {config.WAIT_TIMEOUT}s")
        print(f"        Detail: {e.msg}")
        print("        Try running with --headed to inspect the page")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        if not config.HEADLESS:
            print("\n(Waiting 5s before closing browser...)")
            time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    if "--headless" in sys.argv:
        config.HEADLESS = True
        print("[Override] Headless mode from command line")
    elif "--headed" in sys.argv:
        config.HEADLESS = False
        print("[Override] Headed mode from command line")

    run()
