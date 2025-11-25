from seleniumwire import webdriver

class Link:
    def __init__(self,container,id,address):
        self.container = container
        self.id = id
        self.address = address
        self.status = True
        self.views = 0
    
    def add_view(self):
        self.views += 1
        
    def status(status:bool):
        status = status
        
    def view(self,driver:webdriver.Chrome):
        driver.switch_to.new_window("tab")
        driver.get(self.address)
        
        
    
    
    