import asyncio
# from .._dependencies.functions.public import scroll , sleep

class Address:
    
    def __init__(self,ip):
        self.checked = False
        self.ip = ip
        
    def check(self):
        self.checked = True
        
        
