class BasicItem():

    type_name = "Basic Item"
    title = "title"
    panel = None

    def __init__(self):
        print('basic init')
        pass

    def set_type(self, type_name):
        self.type_name = type_name
    
    def set_title(self, title):
        self.title = title
    
    def set_panel(self, panel):
        self.panel = panel

    def get_type(self):
        return self.type_name
    
    def get_title(self):
        return self.title
    
    def get_panel(self):
        return self.panel