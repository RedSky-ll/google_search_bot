from selenium.webdriver.common.by import By
from .public import getIp, sleep, likelihood
from .logging import log
from selenium import webdriver
from .public import scrolling
import re
from .App.app import Mobile
from _classes.setting import Setting
import pyautogui
import time

mobile = Mobile()
setting = Setting()


def getNewIp(mobile):
    try:
        if mobile is None:
            return
        mobile.init()
        mobile.airplane(setting)
    except Exception as ex:
        log(f"موبایل خطا داد \n{ex}\n")
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
                    log(f"{_address} در این آدرس تشخیص داده شدیم")
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
            log(f"{_address} بازدید با موفقیت ثبت شد ")
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
    """نسخه نهایی خودکار با مختصات دقیق Responsive و iPhone 12 Pro"""
    setting.fill()
    try:
        log("در حال فعال‌سازی DevTools و حالت موبایل با شورتکات‌ها...")
        time.sleep(1.5)

        # باز کردن DevTools
        pyautogui.hotkey('ctrl', 'shift', 'i')
        time.sleep(2.0)

        # فعال کردن Device Toolbar (حالت موبایل)
        pyautogui.hotkey('ctrl', 'shift', 'm')
        time.sleep(2.0)

        log("✅ DevTools و حالت موبایل فعال شدند (Ctrl+Shift+I سپس Ctrl+Shift+M)")

        # مختصات‌های نهایی گرفته‌شده
        responsive_pos = (377, 131)
        iphone_pos = (377, 309)

        # کلیک خودکار روی Responsive
        time.sleep(1)
        pyautogui.click(responsive_pos)
        log(f"📍 کلیک روی Responsive انجام شد در {responsive_pos}")

        # کلیک خودکار روی iPhone 12 Pro
        time.sleep(1)
        pyautogui.click(iphone_pos)
        log(f"📱 کلیک روی iPhone 12 Pro انجام شد در {iphone_pos}")

        # رفرش صفحه برای اطمینان از فعال بودن حالت موبایل
        try:
            driver.refresh()
        except:
            pass

        log("🔄 صفحه در حالت موبایل رفرش شد.")
        try:
            sleep(setting.mobile_sleep)
        except:
            sleep(6)

        log("✅ حالت موبایل با موفقیت فعال و تنظیم شد.")
    except Exception as e:
        log(f"❌ خطا در فعال‌سازی حالت موبایل: {e}")


def fillLinks(driver, Link, Links, scraper):
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
    except Exception:
        log("[13302] هیچ لینکی درون صفحه وجود نداشت")
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
            log(f"خطا در پردازش لینک: {e}")
            continue

    if not found:
        log("هیچ لینک هدفی پیدا نشد")
    else:
        log("تمام لینک‌های هدف بررسی شدند")

    return Links
