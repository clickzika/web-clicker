# ============================================================
#  Web Clicker — Configuration
#  แก้ไขค่าต่างๆ ในไฟล์นี้ตามที่ต้องการ
# ============================================================

from datetime import datetime
_today = datetime.now().strftime("%Y%m%d")

# URL ของหน้าเว็บที่ต้องการเปิด
URL = "https://stage.fundconnext.com/"

# -------- Credentials --------
USERNAME = "uat_natthaphatw"
PASSWORD = "Inw@1596321"

# -------- Selectors --------
# CSS selector ของ input username
USERNAME_SELECTOR = {"by": "css", "value": "input[name='username']"}

# CSS selector ของ input password
PASSWORD_SELECTOR = {"by": "css", "value": "input[name='password']"}

# CSS selector ของปุ่ม Login
BUTTON_SELECTOR = {"by": "css", "value": "button[type='submit']"}

# โฟลเดอร์ที่เก็บไฟล์สำหรับอัพโหลด
UPLOAD_DIR = r"C:\Users\click\Desktop"

# -------- ตั้งค่า Browser --------

# True = ไม่แสดงหน้าต่าง browser (headless)
# False = แสดงหน้าต่าง browser ให้เห็น (headed)
HEADLESS = False

# รอ element โหลดสูงสุดกี่วินาที (ก่อน timeout)
WAIT_TIMEOUT = 10

# รอหลังคลิกกี่วินาที (ให้ผลลัพธ์โหลด)
WAIT_AFTER_CLICK = 3

# -------- Upload Groups --------
# แต่ละแถว: (ชื่อไฟล์ไม่มีวันที่และนามสกุล, file-input id, upload-button id)
# เพิ่ม/ลบแถวเพื่อจัดการไฟล์ที่ต้องอัพโหลด
_UPLOADS = [
    ("LHFUND_FUND_RULES",            "fund-rules-v4FileInput",            "fund-rules-v4UploadButton"),
    ("LHFUND_FUNDMAPPING",           "fund-mapping-v1FileInput",          "fund-mapping-v1UploadButton"),
    ("LHFUND_FUND_SWITCHING_V1",     "fund-switching-matrix-v1FileInput", "fund-switching-matrix-v1UploadButton"),
    ("LHFUND_FUND_SWITCHING_V2",     "fund-switching-matrix-v2FileInput", "fund-switching-matrix-v2UploadButton"),
    ("LHFUND_FUND_CALENDAR",         "fund-calendar-v1FileInput",         "fund-calendar-v1UploadButton"),
    ("LHFUND_TRADE_CALENDAR",        "trade-calendar-v2FileInput",        "trade-calendar-v2UploadButton"),
    ("LHFUND_FUND_FEE",              "fund-feeFileInput",                 "fund-feeUploadButton"),
    # ("LHFUND_FILE8",               "file8FileInput",                    "file8UploadButton"),
    # ("LHFUND_FILE9",               "file9FileInput",                    "file9UploadButton"),
    # ("LHFUND_FILE10",              "file10FileInput",                   "file10UploadButton"),
]

_groups = []
for _fname, _finput, _fbtn in _UPLOADS:
    _groups += [
        {"action": "check_file", "file": rf"{UPLOAD_DIR}\{_today}_{_fname}.txt"},
        {"action": "upload",     "selector": {"by": "id", "value": _finput},
                                 "file": rf"{UPLOAD_DIR}\{_today}_{_fname}.txt"},
        {"action": "wait",       "seconds": 2},
        {"action": "click",      "selector": {"by": "id", "value": _fbtn}},
    ]

# -------- Post-Login Steps --------
POST_LOGIN_STEPS = [
    {"action": "navigate", "url": "https://stage.fundconnext.com/amcUpload/fundProfileUpload"},
    {"action": "wait",     "seconds": 3},
    *_groups,
]
