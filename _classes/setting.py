import json
import re
class Setting:
    
    def __init__(self):
        self.my_sites = []
        self.query = ""
        self.accepts = []
        self.proxy_server = ""
        self.ipaddress = ""
        self.max_attempts = 0
        self.errors = []
        self.mobile_name = ""
        self.mobile_platform = ""
        self.mobile_sleep = 0
    
    
    def fill(self) -> None:
        data = open("./_dependencies/data/setting.json","r",encoding="UTF-8").read()
        data = json.loads(data)
        self.my_sites = data["MY_SITES"]
        self.query = data["QUERY"]
        self.accepts = data["ACCEPTIES"]
        self.proxy_server = data["PROXY_SERVER"]
        self.max_attempts = data["MAX_ATTEMPT"]
        self.errors = data["ERRORS"]
        self.device_id = data["DEVICE_ID"]
        self.device_platform = data["DEVICE_PLATFORM"]
        self.airplane_x = data["AIRPLANE_X"]
        self.airplane_y = data["AIRPLANE_Y"]
        self.mobile_sleep = data["MOBILE_SLEEP"]
        self.device = data["DEVICE"]
        self.inspect_location = data["INSPECT_LOCATION"]
        self.mobile_toggle = data["MOBILE_TOGGLE"]
        # self.query = urllib.parse.quote(data["QUERY"])

        del data
    
    def ip(self,value):
        self.ipaddress = value
    
    def add_site(self,value):
        self.my_sites.append(value)
    def drop_site(self,value):
        for _link in self.my_sites:
            _search = re.search(_link,value)
            if (_search):
                self.my_sites.remove(_link)
                return 
            else :
                pass
    @property
    def ip(self)->str:
        return self.ipaddress
    
    def __str__(self):
        return self.query