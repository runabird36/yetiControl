import selector
# reload (selector)
from selector import Selector

class FreezeSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("MDL Option")
        self._items = []
        self._items.append(["CheckBox", 'History', ["History Check"]])
        self._items.append(["CheckBox", 'Name', ["Name Check"]])
        self._items.append(["CheckBox", 'Freeze', ["Freeze Check"]])
        self._items.append(["CheckBox", 'UVset', ["UVset Check"]])


    def get_items(self):
        return self._items
