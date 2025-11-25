import time
from appium import webdriver
from appium.options.android import UiAutomator2Options


def toggle_mobile_data():
    caps = {
        "platformName": "Android",
        "deviceName": "2429c3a4",
        "automationName": "UiAutomator2",
        "appPackage": "com.android.settings",
        "appActivity": ".Settings",
        "noReset": True
    }
    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        print("Data Turning Off..")
        driver.execute_script("mobile: shell", {
            "command": "svc",
            "args": ["data", "disable"]
        })
        time.sleep(5)

        print("Data Turning On..")
        driver.execute_script("mobile: shell", {
            "command": "svc",
            "args": ["data", "enable"]
        })
        time.sleep(5)

        print("Data Reset Done! ")

    except Exception as e:
        print(f"Turning On/Off Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    toggle_mobile_data()
