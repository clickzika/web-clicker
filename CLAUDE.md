# CLAUDE.md — Project Context

This file is auto-generated during project setup. It is loaded automatically by Claude Code on every session.

---

## Project

Name: web-clicker
Description: Python CLI automation tool that opens a browser, fills in login credentials, clicks the submit button, and runs a configurable sequence of post-login steps. All behaviour controlled via a single config file — no coding required to change targets or flows.
Repository: (local — no remote configured)
Status: Active
Created: 2026-04-21

---

## Session Start — Every Agent Reads These Files First

Before responding to ANYTHING, read in this exact order:

1. `CLAUDE.md` — project stack, conventions, workflow rules (this file)
2. `~/.claude/USER.md` — who the user is, skill level, communication preferences
3. `MEMORY.md` — decisions made, handoff log, what failed before
4. `memory/progress.json` — **current gate/task progress** (if exists)

Then:
- Check `memory/progress.json` for in-progress work — if found, show resume prompt
- Calibrate output depth to USER.md skill level
- Do NOT repeat work already done today

---

## What This Tool Does

`web-clicker` is a Selenium-based login automation script. It:

1. Launches Chrome (headless or headed)
2. Navigates to a configured URL
3. Fills in username and password using configurable CSS/XPath/ID selectors
4. Clicks the login/submit button
5. Executes `POST_LOGIN_STEPS` — an ordered list of actions (click, type, navigate, wait, screenshot, assert_url)
6. Prints the final URL + page title

Run it with:
```bash
python clicker.py              # uses HEADLESS setting from config.py
python clicker.py --headless   # force headless (no browser window)
python clicker.py --headed     # force headed (shows browser window)
```

---

## Tech Stack

| Layer      | Technology              | Version  |
|------------|-------------------------|----------|
| Language   | Python                  | 3.11+    |
| Automation | Selenium WebDriver      | >=4.6.0  |
| Browser    | Chrome + ChromeDriver   | system   |
| Config     | Plain Python module     | —        |
| Tests      | None                    | —        |
| CI/CD      | None                    | —        |

---

## File Map

```
web-clicker/
├── clicker.py      — main script: driver setup, login steps 1–4, run_steps() dispatcher
├── config.py       — ALL configurable values (URL, credentials, selectors, POST_LOGIN_STEPS)
└── requirements.txt — pip dependencies (selenium>=4.6.0)
```

### clicker.py — Key Functions

| Function | Purpose |
|---|---|
| `build_driver(headless)` | Creates Chrome WebDriver with anti-detection flags |
| `resolve_locator(selector)` | Converts config selector dict → `(By, value)` tuple |
| `wait_and_find(driver, selector, timeout)` | Waits until element is clickable |
| `wait_visible(driver, selector, timeout)` | Waits until element is visible (for inputs) |
| `run()` | Orchestrates login steps 1–4 then calls `run_steps()` |
| `run_steps(driver, steps, timeout)` | Dispatches each step in `POST_LOGIN_STEPS` |

### config.py — All Settings

| Setting | Type | Purpose |
|---|---|---|
| `URL` | str | Target page to open |
| `USERNAME` | str | Login username ⚠️ plain text |
| `PASSWORD` | str | Login password ⚠️ plain text |
| `USERNAME_SELECTOR` | dict | `{"by": "css\|xpath\|id\|name\|class\|tag\|text", "value": "..."}` |
| `PASSWORD_SELECTOR` | dict | Same format — targets password input |
| `BUTTON_SELECTOR` | dict | Same format — targets submit button |
| `HEADLESS` | bool | `True` = no browser window, `False` = visible |
| `WAIT_TIMEOUT` | int | Max seconds to wait for each element (default: 10) |
| `WAIT_AFTER_CLICK` | int | Seconds to pause after clicking before quitting (default: 3) |
| `POST_LOGIN_STEPS` | list | Ordered sequence of actions to run after login (see Step Actions below) |

---

## POST_LOGIN_STEPS — Step Actions

Each step in `POST_LOGIN_STEPS` is a dict with an `"action"` key:

| Action | Required keys | What it does |
|---|---|---|
| `click` | `selector` | Waits for element to be clickable, then clicks it |
| `type` | `selector`, `text` | Waits for element to be visible, clears it, types `text` |
| `navigate` | `url` | Navigates to a new URL |
| `wait` | `seconds` | Pauses for N seconds |
| `screenshot` | `filename` | Saves a screenshot to `filename` |
| `assert_url` | `contains` | Asserts current URL contains the given string, exits on failure |
| `js` | `script` | Executes arbitrary JavaScript via `driver.execute_script(script)` |

Example config:
```python
POST_LOGIN_STEPS = [
    {"action": "click",      "selector": {"by": "css", "value": "a.dashboard"}},
    {"action": "wait",       "seconds": 2},
    {"action": "screenshot", "filename": "dashboard.png"},
    {"action": "assert_url", "contains": "/dashboard"},
    # bypass disabled Angular input + trigger change detection
    {"action": "js", "script": "var el=document.getElementById('my-input'); el.removeAttribute('disabled'); el.value='/path/file.xlsx'; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));"},
]
```

Set to `[]` (empty list) to skip post-login steps entirely.

---

## Selector System

The `by` key supports these locator strategies:

| Value | Selenium Equivalent | Example `value` |
|---|---|---|
| `css` | `By.CSS_SELECTOR` | `input[name='username']` |
| `xpath` | `By.XPATH` | `//button[@type='submit']` |
| `id` | `By.ID` | `login-btn` |
| `name` | `By.NAME` | `username` |
| `class` | `By.CLASS_NAME` | `submit-button` |
| `tag` | `By.TAG_NAME` | `button` |
| `text` | auto-XPath | `Login` (matches button/a/input by visible text) |

---

## Current Target (config.py defaults)

- **URL:** `https://stage.fundconnext.com/`
- **Username:** `uat_natthaphatw`
- **Headless:** `False`

---

## ⚠️ Known Security Issue

Credentials are stored in plain text in `config.py`. If this file is ever pushed to a shared git repo, credentials will be exposed.

**Recommended fix:** Move credentials to a `.env` file and load via `python-dotenv`, then add `.env` to `.gitignore`.

---

## Code Conventions

- Language: Python 3.11+
- Style: PEP 8, Black formatting
- Naming: `snake_case` for all functions and variables
- Docstrings: Thai-language inline comments (project convention — match existing style)
- Commits: Conventional Commits — `feat/fix/chore/docs/refactor`

---

## Architecture Principles

- **Single responsibility:** `config.py` owns ALL configuration. `clicker.py` owns ALL logic.
- **No hardcoding in clicker.py** — all values come from `config`
- **Fail fast:** `sys.exit(1)` on any Selenium exception
- **Anti-detection:** navigator.webdriver suppressed; automation flags excluded

---

## Common Tasks for Future Sessions

| Task | What to change |
|---|---|
| Change target website | Update `URL` in `config.py` |
| Change credentials | Update `USERNAME` / `PASSWORD` in `config.py` |
| Change selectors | Update `*_SELECTOR` dicts in `config.py` |
| Add post-login steps | Add dicts to `POST_LOGIN_STEPS` in `config.py` |
| Add `.env` support | Install `python-dotenv`, replace hardcoded values |
| Add retry logic | Wrap steps in a retry loop in `run()` |
| Add screenshot | `driver.save_screenshot("result.png")` after click |
| Add scheduled runs | Use cron or Task Scheduler to call `python clicker.py --headless` |

---

## Autonomy Level

HIGH AUTONOMY — auto-approve all file edits, git, pip, test operations.
STOP only for: permanent deletion, push to remote, credential changes.

---

_Auto-generated: 2026-04-21_
