
import maya.cmds as cmds
import os, pprint

import checker
#reload (checker)
from checker import Checker

from general_md_3x import LUCY
from maya_md import neon
from re import search


class LGTNameChecker(Checker):
    warn_count = -1
    clear_items = []

    def __init__(self):
        Checker.__init__(self)
        self.set_title("Light Name Check")
        self.condition_seventh_error_list = []
        self.warnings = []
        self.assetname= LUCY.get_assetname()



    def execute(self, targets):
        print('Light Name Check')
        
        all_check_tars = []

        print(targets)
        # root_grp = targets[0]
        # neon.select_asset(root_grp)
        for tar in targets:

            res = cmds.ls(tar, dagObjects = True, shapes = True, transforms = True, l=True)
            if res == None:
                continue
            all_check_tars.extend(res)



        err_list = []
        for target in all_check_tars:

            sn_target = target.split("|")[-1]
            print(target)
            print(sn_target)
            print('='*50)
            if search(r"lgt\_\w+\_GRP", sn_target):
                continue

            if sn_target.startswith(self.assetname) == False:
                err_list.append([sn_target, f"prefix이 없습니다 : {self.assetname}"])
            else:
                self.clear_items.append(sn_target)

            # shape_type = cmds.objectType(shape)
            # #condition 7
            # freeze_error_content=self.check_each_GEO_freezed(shape)

            # if shape_type =='transform':
            #     pivot_pos_error_content=self.check_pivot_pos(shape)




            # if freeze_error_content:
            #     err_list.append(freeze_error_content)
            #     continue
            # elif pivot_pos_error_content:
            #     err_list.append(pivot_pos_error_content)
            #     pivot_pos_error_content = []
            #     continue
            # else:
            #     self.clear_items.append(shape)


        pprint.pprint(err_list)
        if err_list == []:
            self.warn_count = 0
        else:
            # for err in err_list:
            #     self.add_warnning(err[0], err[1], 'error', err[0])
            #     self.warn_count += 1

            self.add_items(err_list)
            self.warn_count = len(err_list)



    def is_all_clear(self):
        return self.warn_count == 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        # self.add_item(msg, "Clear", "clear")
        self.add_items([["", msg]])
