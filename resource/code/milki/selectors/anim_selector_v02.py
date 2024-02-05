import selector
# reload (selector)
from selector import Selector
import maya.cmds as cmds
import socket



from maya_md import neon
from general_md_3x import LUCY



class AnimSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("Anim Options")
        print('anim option created')
        if LUCY.get_pipe_step() == 'layout':
            self.anim_selection_dict = {'Export type':[ 'alembic cache', 'arnold scene source (ass)', 'maya'], \
                                    'Export Options':['World space', 'Write Visibility', 'Filter Euler Rotations', 'Strip Namespaces', 'UV write']
                                    }
        else:
            self.anim_selection_dict = {'Export type':[ 'alembic cache', 'arnold scene source (ass)', 'maya'], \
                                    'Export Options':['World space', 'Write Visibility', 'Filter Euler Rotations', 'Strip Namespaces', 'UV write']
                                    }

        # self._items = []
        # type_option_list= anim_selection_dict['Export type']
        # self._items.append(["List", 'Export Order', type_option_list] )
        # cache_option_list= anim_selection_dict['Export Options']
        # self._items.append(["CheckBox", 'Export Options', cache_option_list])
        # self._items.append(["CheckBox", 'Deadline Submit',['submit']])
        # self._items.append(["Edit", 'Step', [1.0]])

    def refresh(self):
        self._items = []
        type_option_list= self.anim_selection_dict['Export type']
        self._items.append(["List", 'Export Order', type_option_list] )
        cache_option_list= self.anim_selection_dict['Export Options']
        self._items.append(["CheckBox", 'Export Options', cache_option_list])
        self._items.append(["CheckBox", 'Deadline Submit',['submit']])
        self._items.append(["Edit", 'Step', [1.0]])
        # if socket.gethostname() == '3DCGI-TD-STY':
        # start_frame = cmds.getAttr("defaultRenderGlobals.fs")
        # end_frame = cmds.getAttr("defaultRenderGlobals.ef")

        start_frame = neon.get_start_time()
        end_frame = neon.get_end_time()

        self._items.append(["Edit", 'Start Frame', [start_frame]])
        self._items.append(["Edit", 'End Frame', [end_frame]])

    def get_items(self):
        return self._items
