import selector
# reload (selector)
from selector import Selector
import maya.cmds as cmds
# import socket



from maya_md import neon




class MdlSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("Mdl pub Options")
        print('mdl option created')



        self._items = []
        # self._items.append(["List", 'Export Order', ['maya', 'alembic cache']] )
        self._items.append(["CheckBox", 'pub with Alembic', ["publish with alembic"]])
        self._items.append(["CheckBox", 'pub with Material', ["Lookdev is assigned"]])




    def get_items(self):
        return self._items
