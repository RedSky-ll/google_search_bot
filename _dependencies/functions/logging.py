import os
from datetime import datetime

# مسیر پوشه‌ی لاگ‌ها
LOG_DIR = "_dependencies/logs"
LOG_FILE = os.path.join(LOG_DIR, "log.txt")

# اطمینان از وجود پوشه
os.makedirs(LOG_DIR, exist_ok=True)

def log(message):
    """ثبت لاگ در فایل و چاپ در کنسول"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"⚠️ خطا در نوشتن لاگ: {e}")
