import selector
from selector import Selector
import maya.cmds as cmds


class HairSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("Hair pub Options")
        print('Hair option created')



        self._items = []
        self._items.append(["CheckBox", 'pub with Scene pub', ["publish with Maya"]])
        




    def get_items(self):
        return self._items
