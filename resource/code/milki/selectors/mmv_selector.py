import selector
# reload (selector)
from selector import Selector

from general_md_3x import LUCY

from os import listdir, path
from re import search



def get_nukever_list() -> list:
    def get_int_vernum(str_info :str) -> int:
        try:
            search_res = search(r"\_v\d+", str_info).group()
            search_res = int(search_res.replace("_v", ""))
        except:
            return 1
        return search_res
        
        
    scene_dir = LUCY.get_scenes_dir()
    nuke_dev_dir = f"{scene_dir}/nuke"
    
    if path.exists(nuke_dev_dir) == False:
        return []
    
    scene_list = listdir(nuke_dev_dir)
    
    scene_list.sort()
    
    last_ver_file  = scene_list[-1]
    first_ver_file = scene_list[0]
    
    last_ver  = get_int_vernum(last_ver_file)
    first_ver = get_int_vernum(first_ver_file)
    return [last_ver, first_ver]
    


class MMVSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("MMV Options")
        print('mmv option created')
        self._items = []
        
        ver_info = get_nukever_list()
        if ver_info == []:
            default_value = 0
            max_value     = 0
            min_value     = 0
        else:    
            default_value = ver_info[0]
            max_value     = ver_info[0]
            min_value     = ver_info[1]
        self._items.append(["spinbox", 'Description 에 입력할 nuke version', [[default_value, max_value, min_value]]] )
        
    # def refresh(self):
    #     self._items = []
        
    #     self._items.append(["spinbox", 'nuke version', ['001']] )
        
        

    def get_items(self):
        return self._items
