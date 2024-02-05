import selector
# reload (selector)
from selector import Selector
import maya.cmds as cmds
import socket

from maya_md import neon


class SimSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("Sim Options")
        print('yeti simulation option created')







    def refresh(self):
        self._items = []


        self._items.append(["Edit", 'Samples', [3.0]])


        start_frame = neon.get_start_time()
        end_frame = neon.get_end_time()

        self._items.append(["Edit", 'Start Frame', [start_frame]])
        self._items.append(["Edit", 'End Frame', [end_frame]])

    def get_items(self):
        return self._items
