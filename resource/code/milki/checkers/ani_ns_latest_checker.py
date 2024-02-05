import maya.cmds as cmds
from checker import Checker

from maya_md import neon
from general_md_3x import LUCY
from os import path, listdir
import re

class ANINsLatestChekcer(Checker):

    warn_count = -1
    clear_items = []

    def __init__(self):
        Checker.__init__(self)
        self.set_title("Rig latest Check")
        self.warnings = []
        

    

    def execute(self, targets):
        def get_pub_dir(_path :str) -> str:
            if "\\" in _path:
                _path = _path.replace("\\", "/")
            return path.dirname(path.dirname(_path))

        def get_version_from_fullpath(_path :str) -> str:
            dirpath = path.dirname(_path)
            return dirpath.split('/')[-1]
            
        def is_the_latest(pub_dir :str, tar_vernum :str) -> bool:
            def compare_version(left_vernum :str, right_vernum :str) -> str:
                try:
                    left_vernum = int(left_vernum.replace("v", ""))
                    right_vernum = int(right_vernum.replace("v", ""))
                except:
                    return ""
                if left_vernum > right_vernum:
                    return "left_win"
                elif left_vernum == right_vernum:
                    return "the_latest"
                else:
                    return "right_win"
                    
                    
            ver_folder_list = listdir(pub_dir)
            for ver_folder in ver_folder_list:
                if re.search(r"v\d+", ver_folder):
                    res = compare_version(ver_folder, tar_vernum)
                    if res == "":
                        continue
                    if res == "left_win":
                        return False
            return True




        print('Execute Rig latest Checker')
        self.warn_count = 0


        all_ns_list = neon.get_all_RNs()

        for cur_ns in all_ns_list:
            
            if neon.is_NS_node(cur_ns) == False:
                continue

            if neon.is_NS_loaded(cur_ns) == False:
                continue

            ref_fullpath = neon.get_RN_path(cur_ns)
            
            pub_dir   = get_pub_dir(ref_fullpath)
            ns_vernum = get_version_from_fullpath(ref_fullpath)
            
            res = is_the_latest(pub_dir, ns_vernum)
            
            if res == False:
                self.add_item(cur_ns, 'The rig data is not the latest', "error", cur_ns)
                self.warn_count += 1
            else:
                self.clear_items.append(cur_ns)


        self.clear_items = list(set(self.clear_items))




    def is_all_clear(self):
        return self.warn_count == 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        self.add_item(msg, "Clear", "clear")


    def virtual_clear(self):
        self.warn_count = 0
