from selenium.webdriver.common.by import By
from .public import sleep, likelihood
from .logging import log
from .public import scrolling
import re
from .App.app import Mobile
from _classes.setting import Setting
import pyautogui
import random
import time
import math

mobile = Mobile()
setting = Setting()

def bezier_mouse_move(x, y, duration=None):
    start_x, start_y = pyautogui.position()

    if duration is None:
        distance = math.hypot(x - start_x, y - start_y)
        duration = min(max(distance / 1800, 0.15), 0.7)
    # Control points (curvature)
    cp1 = (
        start_x + random.randint(-100, 100),
        start_y + random.randint(-100, 100)
    )
    cp2 = (
        x + random.randint(-100, 100),
        y + random.randint(-100, 100)
    )

    steps = max(20, int(duration * 60))  # high resolution = smoother

    for i in range(steps):
        t = i / steps

        # Cubic Bezier formula
        xt = (
            (1 - t)**3 * start_x +
            3 * (1 - t)**2 * t * cp1[0] +
            3 * (1 - t) * t**2 * cp2[0] +
            t**3 * x
        )
        yt = (
            (1 - t)**3 * start_y +
            3 * (1 - t)**2 * t * cp1[1] +
            3 * (1 - t) * t**2 * cp2[1] +
            t**3 * y
        )

        pyautogui.moveTo(xt, yt)
        if steps > 25:
            time.sleep(duration / steps)
def human_click(x, y):
    bezier_mouse_move(x, y)
    time.sleep(random.uniform(0.05, 0.2))
    pyautogui.click()
def human_typing(text, min_delay=0.05, max_delay=0.18):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(min_delay, max_delay))
def advanced_human_typing_en(text):
    for char in text:
        # random typo chance
        if random.random() < 0.04:
            wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
            pyautogui.write(wrong_char)
            time.sleep(random.uniform(0.12, 0.28))
            pyautogui.press("backspace")
            time.sleep(random.uniform(0.12, 0.28))

        pyautogui.write(char)
        if char == " ":
            time.sleep(random.uniform(0.35, 0.6))
        else:
            time.sleep(random.uniform(0.12, 0.28))
def human_scroll(driver, direction=None):
    # direction: "down", "up", or None (random)
    if direction is None:
        direction = random.choice(["down", "up"])

    current_y = driver.execute_script("return window.pageYOffset")
    viewport = driver.execute_script("return window.innerHeight")

    # total scroll distance
    distance = random.randint(int(viewport * 0.3), int(viewport * 1.2))
    distance = distance if direction == "down" else -distance

    duration = random.uniform(0.4, 1.2)
    steps = random.randint(20, 40)

    for i in range(steps):
        t = i / steps

        # ease-out momentum
        t = 1 - pow(1 - t, 3)

        y = current_y + int(distance * t)

        driver.execute_script(f"window.scrollTo(0, {y})")

        time.sleep(duration / steps)

    # reading pause
    time.sleep(random.uniform(0.3, 1.2))

    # small correction scroll (very human)
    if random.random() < 0.35:
        correction = random.randint(-120, 120)
        driver.execute_script(
            f"window.scrollBy(0, {correction})"
        )
def human_reading_scroll(driver):
    viewport = driver.execute_script("return window.innerHeight")

    scrolls = random.randint(2, 5)

    for _ in range(scrolls):
        human_scroll(driver)

        # simulate reading
        time.sleep(random.uniform(0.6, 1.8))

        # occasional small up scroll
        if random.random() < 0.25:
            driver.execute_script(
                f"window.scrollBy(0, {-random.randint(60, 160)})"
            )
            time.sleep(random.uniform(0.2, 0.6))

def get_element_screen_position(driver, element):
    rect = element.rect

    window_position = driver.get_window_position()
    window_x = window_position['x']
    window_y = window_position['y']

    chrome_ui_height = 85  # adjust if needed (tabs + address bar)

    x = window_x + rect['x'] + rect['width'] / 2
    y = window_y + rect['y'] + rect['height'] / 2 + chrome_ui_height

    return int(x), int(y)

def idle_mouse_move():
    x, y = pyautogui.position()
    bezier_mouse_move(
        x + random.randint(-30, 30),
        y + random.randint(-30, 30),
        duration=random.uniform(0.2, 0.6)
    )


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
        idle_mouse_move()
        human_scroll(driver)
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
            idle_mouse_move()
            human_reading_scroll(driver)
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
        sleep(6)

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
        human_click(*three_dots_tools_pos_mac)
        log("clicking on three dots menu...")
        sleep(6)

        # click on more tools
        human_click(*more_tools_pos_mac)
        log("clicking on more tools...")
        sleep(6)

        # click on dev tools
        human_click(*dev_tools_pos_mac)
        sleep(6)
        log("clicking on developer tools...")

        # click on device toolbar
        human_click(*device_toolbar_pos_mac)
        sleep(6)
        log("clicking on device toolbar to enable mobile mode...")

        # click on responsive mode
        human_click(*responsive_pos_mac)
        sleep(6)
        log("selecting responsive mode...")

        # click on iphone 12 pro device
        human_click(*iphone_pos_mac)
        log("selecting iPhone 12 Pro device...")        
        sleep(6)

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
                    idle_mouse_move()
                    human_reading_scroll(driver)
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
                    sleep(5)
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
