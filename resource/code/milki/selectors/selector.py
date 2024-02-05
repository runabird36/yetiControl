import basic_item
# reload (basic_item)
from basic_item import BasicItem

class Selector(BasicItem):
    
    

    def __init__(self):
        # BasicItem.__init__(self)
        BasicItem.__dict__['__init__'](self)
        self.set_type("Selector")
        print('selector created')
    
    def get_select_infos(self):
        if self.panel is None:
            return

        return self.panel.get_select_infos()
    
    def set_signal(self, from_widget :str, to_widget :str) -> None:
        if self.panel is None:
            return
        
        self.panel.set_signal(from_widget, to_widget)
    
    def add_select_items(self, widget_type, title, items):
        select_item = {}
        
        select_item["title"] = title
        select_item["type"] = widget_type
        select_item["items"] = items
        self.select_items.append(select_item)
    

    def set_select_widgets(self, items):
        if self.panel is None:
            return
        
        for select_item in items:
            widget_type = select_item[0]
            title = select_item[1]
            elems = select_item[2]
            
            self.panel.add_select_widget(widget_type, title, elems)

        
        
        
    
