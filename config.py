# ============================================================
#  Web Clicker — Configuration
#  Edit values in this file to change behaviour.
# ============================================================

from datetime import datetime
_today = datetime.now().strftime("%Y%m%d")

# Target website URL
URL = "https://stage.fundconnext.com/"

# -------- Credentials --------
USERNAME = "uat_natthaphatw"
PASSWORD = "Inw@1596321"

# -------- Selectors --------
# CSS selector for the username input
USERNAME_SELECTOR = {"by": "css", "value": "input[name='username']"}

# CSS selector for the password input
PASSWORD_SELECTOR = {"by": "css", "value": "input[name='password']"}

# CSS selector for the login/submit button
BUTTON_SELECTOR = {"by": "css", "value": "button[type='submit']"}

# Folder containing files to upload
UPLOAD_DIR = r"C:\Temp\V4.0"

# -------- Browser Settings --------

# True = run without a browser window (headless)
# False = show the browser window (headed)
HEADLESS = False

# Maximum seconds to wait for an element before timeout
WAIT_TIMEOUT = 10

# Seconds to pause after clicking login before running post-login steps
WAIT_AFTER_CLICK = 3

# -------- Upload Groups --------
# Each row: (filename without date and extension, file-input id, upload-button id)
# Add or remove rows to manage which files are uploaded.
_UPLOADS = [
    ("LHFUND_FUND_RULES",            "fund-rules-v4FileInput",            "fund-rules-v4UploadButton"),
    ("LHFUND_FUNDMAPPING",           "fund-mapping-v1FileInput",          "fund-mapping-v1UploadButton"),
    ("LHFUND_SWITCHING_MATRIX",      "fund-switching-matrix-v2TextInput", "fund-switching-matrix-v2UploadButton"),
    ("LHFUND_FUND_CALENDAR",         "fund-calendar-v1TextInput",         "fund-calendar-v1UploadButton"),
    ("LHFUND_TRADE_CALENDAR",        "trade-calendar-v2TextInput",        "trade-calendar-v2ClearButton"),
    ("LHFUND_FUND_FEE",              "fund-feeTextInput",                 "fund-feeUploadButton"),
]

_groups = []
for _fname, _finput, _fbtn in _UPLOADS:
    _groups += [
        {"action": "check_file", "file": rf"{UPLOAD_DIR}\{_today}_{_fname}.txt"},
        {"action": "upload",     "selector": {"by": "id", "value": _finput},
                                 "file": rf"{UPLOAD_DIR}\{_today}_{_fname}.txt"},
        {"action": "wait",       "seconds": 2},
        {"action": "click",      "selector": {"by": "id", "value": _fbtn}},
        {"action": "wait",       "seconds": 10},
    ]

# -------- Post-Login Steps --------
POST_LOGIN_STEPS = [
    {"action": "navigate", "url": "https://stage.fundconnext.com/amcUpload/fundProfileUpload"},
    {"action": "wait",     "seconds": 10},
    *_groups,
]
