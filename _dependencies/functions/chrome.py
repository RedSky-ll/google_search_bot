from selenium.webdriver.common.by import By
from .public import sleep, likelihood
from .logging import log
from .public import scrolling
import re
from .App.app import Mobile
from _classes.setting import Setting
import pyautogui


mobile = Mobile()
setting = Setting()


def getNewIp(mobile):
    try:
        if mobile is None:
            return
        mobile.init()
        mobile.airplane(setting)
    except Exception as ex:
        log(f"mobile error \n{ex}\n")
    finally:
        try:
            sleep(setting.mobile_sleep)
        except:
            sleep(5)


def authHandle(driver, setting, _address="[ No Address ]"):
    try:
        _body = driver.find_element(By.TAG_NAME, "body")
        scrolling(driver)
        _errors = 0
        for _error in setting.errors:
            try:
                if re.search(_error, _body.text):
                    _errors += 1
                    log(f"{_address} detected on this address")
                    break
            except:
                continue
        if _errors == 0:
            sleep(3)
            scrolling(driver)
            sleep(3)
            scrolling(driver)
            sleep(3)
            scrolling(driver)
            log(f"{_address} visit recorded successfully")
    except Exception:
        pass


def phoneclick(driver):
    try:
        _alist = driver.find_elements(By.TAG_NAME, "a")
    except:
        return
    for _a in _alist:
        try:
            _href = _a.get_attribute("href")
            if _href and "tel:" in _href:
                driver.execute_script("arguments[0].click();", _a)
                break
        except:
            continue


def activate_mobile_mode(driver):
    """the final function to enable mobile mode using pyautogui to control chrome devtools"""
    setting.fill()
    try:
        log("enabling DevTools and mobile mode using shortcuts...")
        sleep(10)

        #win
        three_dots_tools_pos_win = (1908, 92) 
        more_tools_pos_win = (1707, 768) 
        dev_tools_pos_win = (1394, 960) 
    
        device_toolbar_pos_win = (1305, 136) 
        responsive_pos_win = (412, 137)
        iphone_pos_win = (383, 308)

        #mac
        three_dots_tools_pos_mac = (1418, 102)
        more_tools_pos_mac = (1374, 624)
        dev_tools_pos_mac = (1009, 789)
        device_toolbar_pos_mac = (925, 121)
        iphone_pos_mac = (289, 227)
        responsive_pos_mac = (264, 139)
        
        # click on three dots menu
        pyautogui.click(three_dots_tools_pos_win)
        log("clicking on three dots menu...")
        sleep(10)

        # click on more tools
        pyautogui.click(more_tools_pos_win)
        log("clicking on more tools...")
        sleep(10)

        # click on dev tools
        pyautogui.click(dev_tools_pos_win)
        sleep(10)
        log("clicking on developer tools...")

        # click on device toolbar
        pyautogui.click(device_toolbar_pos_win)
        sleep(10)
        log("clicking on device toolbar to enable mobile mode...")

        # click on responsive mode
        pyautogui.click(responsive_pos_win)
        sleep(10)
        log("selecting responsive mode...")

        # click on iphone 12 pro device
        pyautogui.click(iphone_pos_win)
        log("selecting iPhone 12 Pro device...")        
        sleep(10)

        #refresh the page to certain the mobile mode is applied
        try:
            driver.refresh()
        except:
            pass

        log("refreshing page on mobile mode 🔄...")
        try:
            sleep(setting.mobile_sleep)
        except:
            sleep(6)

        log("✅ mobile mode enabled successfully.")
    except Exception as e:
        log(f"❌ error on enabling mobile mode: {e}")


def fillLinks(driver, Link, Links, scraper):
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
    except Exception:
        log("[13302] no links found on the page.")
        return Links

    found = False
    for link in links:
        try:
            href = link.get_attribute("href")
            text = link.text or ""
        except:
            continue

        if not href:
            continue

        try:
            if likelihood(setting, text):
                found = True
                log(f"لینک هدف پیدا شد: {href}")

                # اسکرول و کلیک ایمن
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    sleep(1)
                    driver.execute_script("arguments[0].click();", link)
                except Exception:
                    try:
                        link.click()
                    except:
                        log("کلیک روی لینک انجام نشد، رد شد")
                        continue

                # پس از کلیک، صبر و تعامل با صفحه جدید
                sleep(6)
                try:
                    scrolling(driver)
                except:
                    pass
                sleep(2)
                try:
                    phoneclick(driver)
                except:
                    pass
                sleep(2)

                # بازگشت به صفحه نتایج
                try:
                    driver.back()
                except:
                    log("بازگشت به صفحه قبل انجام نشد")
                sleep(3)
        except Exception as e:
            log(f"error on processing link: {e}")
            continue

    if not found:
        log("no target links found.")
    else:
        log("all target links have been checked.")

    return Links
