# ============================================================
#  Web Clicker — Configuration
#  แก้ไขค่าต่างๆ ในไฟล์นี้ตามที่ต้องการ
# ============================================================

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

# -------- ตั้งค่า Browser --------

# True = ไม่แสดงหน้าต่าง browser (headless)
# False = แสดงหน้าต่าง browser ให้เห็น (headed)
HEADLESS = False

# รอ element โหลดสูงสุดกี่วินาที (ก่อน timeout)
WAIT_TIMEOUT = 10

# รอหลังคลิกกี่วินาที (ให้ผลลัพธ์โหลด)
WAIT_AFTER_CLICK = 3
