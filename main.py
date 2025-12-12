import time
import datetime
import random
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc

# // mine
from _classes.setting import Setting
from _classes._link import Links
from _classes.Link import Link
from _classes._handles import Handles
from _classes.Address import Address
from _dependencies.functions.logging import log
from _dependencies.functions.public import sleep , scroll , typing , scrolling , getIp , likelihood 
from _dependencies.functions.chrome import fillLinks , getNewIp, authHandle , activate_mobile_mode , phoneclick
from _dependencies.functions.App.app import Mobile
# // mine

setting = Setting()
setting.fill()
address = Address("192.168.1.1")
# address = Address(getIp())
mobile = Mobile()

mobile_emulation = {
    "deviceName": setting.device 
}

# chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)



if setting.proxy_server:
    wire_options = {
        'proxy': {
            'http': 'http://td-customer-IfAQNf534fkj:mUwxx5wls9vd@tihb7yjb.pr.thordata.net:9999',
            'https': 'https://td-customer-IfAQNf534fkj:mUwxx5wls9vd@tihb7yjb.pr.thordata.net:9999',
            'no_proxy': 'localhost,127.0.0.1'  
        }
    }
else:
    wire_options = {}

try:
    mobile.init()
    pass
except Exception as ex:
    log(f"موبایل خطا داد \n{ex}\n")
def scraper():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    global chrome
    # هر بار Links جدید ساخته میشه
    LinksObj = Links()



    chrome = uc.Chrome(options=chrome_options)
    setting = Setting()
    setting.fill()
    chrome.get("https://google.com/")
    log("مرورگر وارد گوگل شد")
    scrolling(chrome)
    
    # هندل پاپ آپ اولیه
    try:
        _buttons = WebDriverWait(chrome,15).until(EC.presence_of_all_elements_located((By.TAG_NAME,"button")))
        for _button in _buttons:
            try:
                _div = _button.find_element(By.TAG_NAME,"div")
                if _div.text.strip() in setting.accepts:
                    sleep()
                    scroll(chrome,_div,0,400)
                    sleep(9)
                    _div.click()
                    _button.click()
                    log("پاپ اپ هندل شد")
                    break
            except:
                pass
    except:
        log("پاپ اپی برای استارت تعریف نشده")

    _searchElement = WebDriverWait(chrome,15).until(EC.visibility_of_element_located((By.NAME,"q")))
    sleep(12)
    scrolling(chrome)
    typing(_searchElement,setting.query)
    sleep(12) 
    _searchElement.send_keys(Keys.ENTER)
    del _searchElement       
    authHandle(chrome,setting)
    
    # چک کردن کپچا
    try:
        form = chrome.find_element(By.ID,"captcha-form")
        if (form.get_attribute("id").strip() == "captcha-form"):
            log("مرورگر توسط گوگل ربات تشخیص داده شد")
            chrome.execute_script("alert('ربات نیاز به ایپی جدید دارد');")
            getNewIp(mobile)
            chrome.quit()
            return
    except:
        log("با موفقیت وارد صفحه اصلی شدیم")

    # هندل دوباره پاپ آپ در نتایج
    try:
        _buttons = WebDriverWait(chrome,15).until(EC.presence_of_all_elements_located((By.TAG_NAME,"button")))
        for _button in _buttons:
            try:
                _div = _button.find_element(By.TAG_NAME,"div")
                if _div.text.strip() in setting.accepts:
                    sleep()
                    scroll(chrome,_div,0,400)
                    sleep(7)
                    _div.click()
                    log("در صفحه اصلی پاپ اپی پیدا نشد ")
                    break
            except:
                pass
    except:
        log("در صفحه اصلی پاپ اپی پیدا نشد ")

    # پر کردن لینک‌ها
    scrolling(chrome)
    activate_mobile_mode(chrome)

    out = fillLinks(chrome, Link, LinksObj, scraper)
    try:
        if len(out.links) != 0:
            for _link in out.links:
                sleep(2)
                if likelihood(setting, _link.address):
                    _link.container.click()
                    _address = _link.address
                    phoneclick(chrome)
                    authHandle(chrome,setting,_address)
                    sleep(3)
                    getNewIp(mobile)
                    sleep(3)
                else:
                    log(f"{_link.address} جزو تارگت های ما نیست")

            log("تمامی اسپانسر ها با موفقیت چک شدند")
        else:
            log("اسپانسر پیدا نشد")
    except Exception as ex:
        log(f"مشکل ناشناخته ای رخ داده {ex}")

    # بستن مرورگر و آی‌پی جدید
    getNewIp(mobile)
    chrome.quit()
    log("مرورگر بسته شد و برای اجرای بعدی آماده است")


if __name__ == "__main__":
    log("برنامه استارت شد ----")
    while True:
        try:
            scraper()
        except Exception as ex:
            log(f"[1304] خطا هنگام اجرای برنامه \n{ex}\n")
            try:
                chrome.quit()
            except:
                pass
        sleep()

def unsave_activity_history():
    try:
        log("در حال غیرفعال‌سازی ذخیره تاریخچه فعالیت‌ها...")
        chrome.get("chrome://settings/privacySandbox")
        sleep(3)
        try:
            toggle = WebDriverWait(chrome, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'settings-toggle-button[aria-label="غیرفعال‌سازی تاریخچه فعالیت‌ها"]'))
            )
            toggle.click()
            log("✅ ذخیره تاریخچه فعالیت‌ها غیرفعال شد.")
        except Exception as e:
            log(f"❌ خطا در غیرفعال‌سازی تاریخچه فعالیت‌ها: {e}")
    except Exception as e:
        log(f"❌ خطا در دسترسی به تنظیمات حریم خصوصی: {e}")