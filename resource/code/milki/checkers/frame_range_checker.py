# -*- coding:utf-8 -*-

import sys
if sys.version_info.major == 3:
    from importlib import reload
import checker
reload(checker)
from checker import Checker
if sys.platform.count("win"):
    import neon
else:
    from maya_md import neon
from general_md_3x import LUCY
class FrameRangeChecker(Checker):
    m_sg_tk = None
    warn_count = 0
    clear_items = []
    def __init__(self, m_sg_tk):
        Checker.__init__(self)
        self.m_sg_tk = m_sg_tk._get_sg()
        self.set_title("Frame range Check")


    def get_sg_frame_info(self):
        '''
        return value : [{'id': 11442, 'sg_cut_in': 1001, 'sg_cut_out': 1100, 'type': 'Shot'}]
        '''
        prj = LUCY.get_project()
        shot = LUCY.get_shot()
        t_filter = [['project','name_is', prj],['code', 'is', shot]]
        t_field = ['sg_cut_in','sg_cut_out']

        return self.m_sg_tk.find_one('Shot',t_filter,t_field)

    def execute(self, targets):
        self.warn_count = 0
        sg_frame_info = self.get_sg_frame_info()
        if sg_frame_info == None:
            # self.clear_items.append("There is no Frame range")
            return

        sg_start_time = sg_frame_info['sg_cut_in']
        if sg_start_time != None:
            sg_start_time = float(sg_start_time)
        else:
            self.warn_count += 1
            self.add_warnning(sg_start_time, 'start frame in shotgun is not specified, check in shotgun shot page', 'error')

        sg_end_time = sg_frame_info['sg_cut_out']
        if sg_end_time != None:
            sg_end_time = float(sg_end_time)
        else:
            self.warn_count += 1
            self.add_warnning(sg_end_time, 'end frame in shotgun is not specified, check in shotgun shot page', 'error')

        cur_scn_start_time = neon.get_start_time()
        cur_scn_end_time = neon.get_end_time()

        if sg_start_time != cur_scn_start_time:
            cur_scn_start_time=str(cur_scn_start_time)
            self.add_warnning( cur_scn_start_time, 'start frame num is not matched with shotgun start frame num', 'error')
            self.warn_count += 1
        else:
            print('start frame is matched')
            clear_start_msg = 'Start : {0}'.format(cur_scn_start_time)
            self.clear_items.append(clear_start_msg)

        if sg_end_time != cur_scn_end_time:
            cur_scn_end_time= str(cur_scn_end_time)
            self.add_warnning(cur_scn_end_time, 'end frame num is not matched with shotgun end frame num', 'error')
            self.warn_count += 1
        else:
            print('end frame is matched')
            clear_end_msg = 'End : {0}'.format(cur_scn_end_time)
            self.clear_items.append(clear_end_msg)



    def is_all_clear(self):
        print('warn  count: {0}'.format(self.warn_count))
        return self.warn_count == 0

    def virtual_clear(self):
        self.warn_count = 0

    def show_all_clear_items(self):
        clear_items_set = set(self.clear_items)
        for clear_item in clear_items_set:
            self.add_item(clear_item, "Clear", "clear")
