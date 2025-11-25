from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
from _classes.setting import Setting
from _dependencies.functions.public import sleep
from _dependencies.functions.logging import log

class Mobile:
    def __init__(self):
        self.driver = None
        
    def init(self) -> bool:
        if self.driver is not None:
            return True
        try:
            options = UiAutomator2Options()
            options.platform_name = "Android"
            options.device_name = "60baa866"
            options.automation_name = "UIAutomator2"
            # نگه داشتن سشن در حالت idle
            options.set_capability("newCommandTimeout", 300)
            options.set_capability("noReset", True)
            # (اختیاری) اگر می‌خواهی دقیقاً به همین دیوایس وصل شود، باز کن:
            # options.set_capability("udid", "a0978021")

            # ✅ برای Appium v3 باید بدون /wd/hub وصل شویم
            self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

            log("✅ موبایل با موفقیت کانفیگ و به Appium متصل شد")
            return True
        except Exception as ex:
            log(f"❌ موبایل خطا داد در اتصال:\n{ex}")
            self.driver = None
            return False
        
    def airplane(self, setting: Setting):
        setting = Setting()
        setting.fill()
        try:
            # اطمینان از وجود سشن
            if self.driver is None:
                self.init()

            self.driver.open_notifications()
            sleep(7)
            self.driver.tap([(setting.airplane_x, setting.airplane_y)])
            sleep(24)
            self.driver.back()
            self.driver.back()

            self.driver.open_notifications()
            sleep(7)
            self.driver.tap([(setting.airplane_x, setting.airplane_y)])
            sleep(10)
            self.driver.back()
            self.driver.back()

            log("✅ حالت پرواز با موفقیت خاموش/روشن شد (IP جدید فعال شد)")
        except Exception as ex:
            log(f"❌ موبایل خطا داد در airplane:\n{ex}")
            try:
                if self.driver is not None:
                    self.driver.quit()
            except:
                pass
            finally:
                self.driver = None

    def shutdown(self):
        try:
            if self.driver is not None:
                self.driver.quit()
        except Exception:
            pass
        finally:
            self.driver = None
            log("📴 ارتباط با موبایل بسته شد")
