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
class FPSChecker(Checker):
    m_sg_tk = None
    warn_count = 0
    clear_items = []
    def __init__(self, m_sg_tk):
        Checker.__init__(self)
        self.m_sg_tk = m_sg_tk._get_sg()
        self.set_title("FPS Check")

    
    def get_project_fps(self):
        project_name = LUCY.get_project()
        fps = self.m_sg_tk.find_one("Project", [['sg_status', 'is', 'Active'], ["name", "is", project_name]], ["sg_3d_frame_rate"])
        if fps:
            return fps["sg_3d_frame_rate"]
        else:
            return None

    def execute(self, targets):
        self.warn_count = 0
        sg_fps_str = self.get_project_fps()
        

        
        if sg_fps_str != None:
            sg_fps = float(sg_fps_str)
            cur_fps = neon.get_fps_info()

            if sg_fps_str not in cur_fps:
                self.add_warnning( f"샷그리드 fps : {sg_fps_str}", f'현재 씬 fps : {cur_fps} / 샷그리드 fps와 불일치', 'error')
                self.warn_count += 1
            else:
                clear_fps_msg = f'CLERA - 현재 씬 fps : {cur_fps} == 샷그리드 fps : {sg_fps_str}'
                self.clear_items.append(clear_fps_msg)
                
        else:
            self.warn_count += 1
            self.add_warnning("없음", '샷그리드에 SEQ_info의 3D_Frame Rate 가 지정되어있지 않습니다.', 'error')
            

        
        



    def is_all_clear(self):
        print('warn  count: {0}'.format(self.warn_count))
        return self.warn_count == 0

    def virtual_clear(self):
        self.warn_count = 0

    def show_all_clear_items(self):
        clear_items_set = set(self.clear_items)
        for clear_item in clear_items_set:
            self.add_item(clear_item, "Clear", "clear")
