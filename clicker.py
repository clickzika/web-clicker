"""
Web Clicker — เปิดเว็บ, กรอก username/password และคลิกปุ่ม Login
ตามที่กำหนดใน config.py
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import config


# ── Mapping วิธีการ locate element ──────────────────────────
BY_MAP = {
    "css":   By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "id":    By.ID,
    "name":  By.NAME,
    "class": By.CLASS_NAME,
    "tag":   By.TAG_NAME,
}


def build_driver(headless: bool) -> webdriver.Chrome:
    """สร้าง Chrome WebDriver ตาม mode ที่เลือก"""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        print("[Browser] Headless mode — ไม่แสดงหน้าต่าง browser")
    else:
        print("[Browser] Headed mode — แสดงหน้าต่าง browser")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def resolve_locator(selector: dict) -> tuple:
    """แปลง selector config เป็น (By, value) tuple"""
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
            f"ไม่รู้จัก by='{by_key}'. รองรับ: {list(BY_MAP.keys()) + ['text']}"
        )


def wait_and_find(driver: webdriver.Chrome, selector: dict, timeout: int):
    """รอจนกว่า element จะ clickable แล้วคืนค่า"""
    locator = resolve_locator(selector)
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_visible(driver: webdriver.Chrome, selector: dict, timeout: int):
    """รอจนกว่า element จะมองเห็น (ใช้กับ input fields)"""
    locator = resolve_locator(selector)
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


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
        # ── Step 1: เปิดหน้าเว็บ ─────────────────────────────
        print(f"\n[1/4] เปิด: {config.URL}")
        driver.get(config.URL)
        print(f"      ชื่อหน้า: {driver.title}")

        # ── Step 2: กรอก Username ────────────────────────────
        print(f"\n[2/4] กรอก Username")
        username_field = wait_visible(
            driver, config.USERNAME_SELECTOR, config.WAIT_TIMEOUT
        )
        username_field.clear()
        username_field.send_keys(config.USERNAME)
        print(f"      กรอกแล้ว: {config.USERNAME}")

        # ── Step 3: กรอก Password ────────────────────────────
        print(f"\n[3/4] กรอก Password")
        password_field = wait_visible(
            driver, config.PASSWORD_SELECTOR, config.WAIT_TIMEOUT
        )
        password_field.clear()
        password_field.send_keys(config.PASSWORD)
        print(f"      กรอกแล้ว: {'*' * len(config.PASSWORD)}")

        # ── Step 4: คลิกปุ่ม ─────────────────────────────────
        print(f"\n[4/4] คลิกปุ่ม Login")
        submit_btn = wait_and_find(
            driver, config.BUTTON_SELECTOR, config.WAIT_TIMEOUT
        )
        print(f"      พบปุ่ม: <{submit_btn.tag_name}> text='{submit_btn.text.strip()}'")
        submit_btn.click()
        print("      คลิกแล้ว ✓")

        # ── รอผลลัพธ์ ─────────────────────────────────────────
        time.sleep(config.WAIT_AFTER_CLICK)
        print(f"\n[เสร็จสิ้น]")
        print(f"  URL ปัจจุบัน: {driver.current_url}")
        print(f"  ชื่อหน้า    : {driver.title}")

    except TimeoutException as e:
        print(f"\n[ERROR] Timeout — ไม่พบ element ภายใน {config.WAIT_TIMEOUT} วินาที")
        print(f"        รายละเอียด: {e.msg}")
        print("        ลองเปิดด้วย --headed แล้วดูว่า selector ถูกต้องไหม")
        sys.exit(1)
    except NoSuchElementException as e:
        print(f"\n[ERROR] ไม่พบ element: {e.msg}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        if not config.HEADLESS:
            print("\n(รอ 5 วินาที ก่อนปิด browser...)")
            time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    if "--headless" in sys.argv:
        config.HEADLESS = True
        print("[Override] Headless mode จาก command line")
    elif "--headed" in sys.argv:
        config.HEADLESS = False
        print("[Override] Headed mode จาก command line")

    run()
