import random
import time
import selenium
import requests
import json
import re

ips = ["https://api.ipify.org?format=json","https://api.myip.com"]
def randomtime(speed)->float:
    return random.uniform(0,1) * speed
def sleep(speed=6):
    time.sleep(randomtime(speed=speed))
    
def typing(element,text):
    for char in text:
        element.send_keys(char)
        sleep(randomtime(speed=1))
def scroll(driver, element , x=0, y=0):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});",element)

def scrolling(driver):
    total_scroll = random.randint(-300,300)
    step = 10
    for y in range(0, total_scroll, step):
        time.sleep(random.uniform(0.01, 0.1))
        driver.execute_script(f"window.scrollTo(0,{y})")
def getIp():
    for _ip in ips:
        try:
            _res = requests.get(_ip,timeout=5)
            if _res is not None:
                return _res.json()["ip"]
            else :
                continue
        except :
            continue

def clean(value:str):
    value = value.replace("https://","")
    value = value.replace("http://","")
    value = value.replace("www.","")
    value = value.rstrip(".")
    return value

import re

def clean(value: str) -> str:
    value = value.replace("https://", "")
    value = value.replace("http://", "")
    value = value.replace("www.", "")

    value =  value.replace(r"/+","")
    value = value.rstrip(".")
    value = value.rstrip("/")
    return value

def likelihood(setting, value: str) -> bool:
    value = clean(value)  
    for _link in setting.my_sites:
        domain = clean(str(_link))
        if re.search(domain, value):
            return True
    return False

