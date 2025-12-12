import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
import pyautogui

from _classes.setting import Setting
from _classes._link import Links
from _classes.Link import Link
from _classes.Address import Address
from _dependencies.functions.logging import log
from _dependencies.functions.public import sleep , scroll , typing , scrolling, likelihood 
from _dependencies.functions.chrome import fillLinks , getNewIp, authHandle , activate_mobile_mode , phoneclick
from _dependencies.functions.App.app import Mobile

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
    log(f"mobile error \n{ex}\n")
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
    #create Links object every time to avoid data persistence between runs
    LinksObj = Links()



    chrome = uc.Chrome(options=chrome_options)
    setting = Setting()
    setting.fill()

    #turning off Search customisation
    search_custom_btn_pos = (1057, 240)
    chrome.get("https://www.google.com/history/optout?hl=en-IR")
    sleep(12)
    pyautogui.click(search_custom_btn_pos)
    sleep(12)

    chrome.get("https://google.com/")
    log("browser entered google")
    scrolling(chrome)
    
    # handle startup popups
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
                    log("popup handled")
                    break
            except:
                pass
    except:
        log("no startup popup defined")

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
            log("browser known as bot by google captcha")
            chrome.execute_script("alert('bot need new IP');")
            getNewIp(mobile)
            chrome.quit()
            return
    except:
        log("successfully entered the main page")

    # handle popups again in results
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
                    log("no popup found on main page")
                    break
            except:
                pass
    except:
        log("no popup found on main page")

    # filling links
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
                    scrolling(chrome)
                    scrolling(chrome)

                    phoneclick(chrome)
                    authHandle(chrome,setting,_address)
                    sleep(12)
                    # getNewIp(mobile)
                else:
                    log(f"{_link.address} is not one of our targets")

            log("all sponsors have been checked successfully")
        else:
            log("no sponsors found")
    except Exception as ex:
        log(f"an unknown error occurred {ex}")

    # closing browser and new IP
    getNewIp(mobile)
    chrome.quit()
    log("browser closed and ready for next run")


if __name__ == "__main__":
    log("program started ----")
    while True:
        try:
            scraper()
        except Exception as ex:
            log(f"[1304] error while running program \n{ex}\n")
            try:
                chrome.quit()
            except:
                pass
        sleep()

def unsave_activity_history():
    try:
        log("disabling activity history saving...")
        chrome.get("chrome://settings/privacySandbox")
        sleep(3)
        try:
            toggle = WebDriverWait(chrome, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'settings-toggle-button[aria-label="Disable activity history saving"]'))
            )
            toggle.click()
            log("✅ activity history saving disabled.")
        except Exception as e:
            log(f"❌ error disabling activity history saving: {e}")
    except Exception as e:
        log(f"❌ error accessing privacy settings: {e}")