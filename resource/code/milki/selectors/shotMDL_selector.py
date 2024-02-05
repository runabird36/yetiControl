from importlib import reload
import selector
reload (selector)
from selector import Selector
import maya.cmds as cmds
import socket



from maya_md import neon


class ShotMDLSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("Shot MDL Options")
        print('shot mdl option created')

        self.anim_selection_dict = {'Export type':['alembic cache', 'maya'], \
                                'Export Options':['World space', 'Write Visibility', 'Filter Euler Rotations', 'Strip Namespaces', 'UV write']
                                }



    def refresh(self):
        self._items = []
        type_option_list= self.anim_selection_dict['Export type']
        self._items.append(["List", 'Export Order', type_option_list] )
        cache_option_list= self.anim_selection_dict['Export Options']
        self._items.append(["CheckBox", 'Export Options', cache_option_list])
        # self._items.append(["CheckBox", 'Deadline Submit',['submit']])
        self._items.append(["CheckBox", 'Is Sequence',['abc sequence']])
        self._items.append(["Edit", 'Step', [1.0]])

        start_frame = neon.get_start_time()
        end_frame = neon.get_end_time()
        # end_frame = start_frame

        self._items.append(["Edit", 'Start Frame', [start_frame]])
        self._items.append(["Edit", 'End Frame', [end_frame]])
        self._items.append(["CheckBox", 'Bake with Handle',['Bake with Handle']])
        self._items.append(["Edit", 'Handle', ["5"]])
        

    def set_siganls(self) -> None:
        self.set_signal("abcsequencecheckbox", "endframelineedit")


    def get_items(self):
        return self._items
