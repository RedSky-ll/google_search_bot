class Handles:
    def __init__(self,id):
        self.id = None
        
    def add_handle(self,id):
        if(self.id == None):
            self.id = dict()
            self.id["Home"] = id
        else :
            keys = []
            for key in self.id.keys():
                keys.append(int(key))
            self.id[f"{max(keys) + 1}"] = id
                
        