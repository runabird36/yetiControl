import selector
# reload (selector)
from selector import Selector

import maya.cmds as cmds


from general_md_3x import LUCY


class LgtSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)

        print('lgt option created')

        cur_step = LUCY.get_pipe_step()
        # if cur_step == 'lyt':
        #     self.set_title("Lyt Options")
        #     self.ass_selection_dict = {'Export type':['ass', 'alembic cache', 'maya'], \
        #                             'Abc Export Options':['World space', 'Write Visibility', 'Filter Euler Rotations', 'Strip Namespaces', 'UV write'],\
        #                             'ASS Export Options':['option', 'camera', 'light', 'shape', 'shader', 'override', 'driver', 'filter']
                                    # }
        # elif cur_step == 'lgt':
        self.set_title("Lgt Options")
        self.ass_selection_dict = {'Export type':['ass', 'maya'],\
                                'ASS Export Options':['option', 'camera', 'light', 'shape', 'shader', 'override', 'driver', 'filter']
                                }

        # self._items = []
        # type_option_list= anim_selection_dict['Export type']
        # self._items.append(["List", 'Export Order', type_option_list] )
        # cache_option_list= anim_selection_dict['Export Options']
        # self._items.append(["CheckBox", 'Export Options', cache_option_list])
        # self._items.append(["CheckBox", 'Deadline Submit',['submit']])
        # self._items.append(["Edit", 'Step', [1.0]])

    def refresh(self):
        cur_step = LUCY.get_pipe_step()

        self._items = []
        type_option_list= self.ass_selection_dict['Export type']
        self._items.append(["List", 'Export Order', type_option_list] )

        # if cur_step == 'lyt':
        #     abc_cache_option_list= self.ass_selection_dict['Abc Export Options']
        #     self._items.append(["CheckBox", 'Abc Export Options', abc_cache_option_list])
        #     # self._items.append(["CheckBox", 'Deadline Submit',['submit']])
        #     self._items.append(["Edit", 'Step', [1.0]])
        # if cur_step in ['lyt', 'lgt']:
        start_frame = cmds.playbackOptions( q=True, min=True )
        end_frame = cmds.playbackOptions( q=True, max=True )

        ass_option_list= self.ass_selection_dict['ASS Export Options']
        self._items.append(["CheckBox", 'Ass Export Options', ass_option_list])
        self._items.append(["CheckBox", 'Sequence',['sequence']])
        self._items.append(["Edit", 'Start Frame', [start_frame]])
        self._items.append(["Edit", 'End Frame', [end_frame]])

    def get_items(self):
        return self._items
