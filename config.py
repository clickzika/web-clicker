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

# -------- Post-Login Steps --------
# ลำดับ action ที่ต้องการให้รันหลัง login สำเร็จ
# ตั้งเป็น [] เพื่อข้ามขั้นตอนนี้
#
# action ที่รองรับ:
#   click       — คลิก element (ต้องมี "selector")
#   type        — พิมพ์ข้อความ (ต้องมี "selector" และ "text")
#   navigate    — เปิด URL ใหม่ (ต้องมี "url")
#   wait        — หน่วงเวลา (ต้องมี "seconds")
#   screenshot  — บันทึกภาพหน้าจอ (ต้องมี "filename")
#   assert_url  — ตรวจสอบว่า URL ปัจจุบันมีข้อความที่กำหนด (ต้องมี "contains")
#   js          — รัน JavaScript ผ่าน driver.execute_script() (ต้องมี "script")
#


POST_LOGIN_STEPS = [
    {"action": "navigate", "url": "https://stage.fundconnext.com/amcUpload/fundProfileUpload"},
    {"action": "wait",     "seconds": 3},
    {"action": "check_file", "file": rf"{UPLOAD_DIR}\{_today}_LHFUND_FUND_RULES.txt"},
    {"action": "upload",     "selector": {"by": "id", "value": "fund-rules-v4FileInput"}, "file": rf"{UPLOAD_DIR}\{_today}_LHFUND_FUND_RULES.txt"},
    {"action": "wait",     "seconds": 2},
    {"action": "click",    "selector": {"by": "id", "value": "fund-rules-v4UploadButton"}},
]
