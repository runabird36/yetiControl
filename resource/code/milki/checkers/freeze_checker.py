
import maya.cmds as cmds
import os, pprint

import checker
#reload (checker)
from checker import Checker


from maya_md import neon


class FreezeChecker(Checker):
    warn_count = -1
    clear_items = []

    def __init__(self):
        Checker.__init__(self)
        self.set_title("Freeze transform Check")
        self.condition_seventh_error_list = []
        self.warnings = []


    def check_each_GEO_freezed(self, each_shape):
        '''condition 7 : check mesh is freezed : check each transform mesh'''
        freeze_check_list=cmds.getAttr(each_shape+'.matrix')
        for element in freeze_check_list:
            if element != 1.0 and element != 0.0:
                return [each_shape, "is not freezed" ]



    def check_pivot_pos(self, each_transform):

        pivot_ws_pos_list = cmds.xform(each_transform,q=1,ws=1,rp=1)
        for pivot_ws_pos in pivot_ws_pos_list:
            if pivot_ws_pos != 0.0:
                return [each_transform, "pivot position is not [0,0,0]" ]



    def execute(self, targets):
        print('Execute freeze checker')
        

        root_grp = targets[0]
        neon.select_asset(root_grp)
        all_shape = cmds.ls(root_grp, dagObjects = True, shapes = True, transforms = True)


        err_list = []
        for shape in all_shape:
            shape_type = cmds.objectType(shape)
            #condition 7
            freeze_error_content=self.check_each_GEO_freezed(shape)

            if shape_type =='transform':
                pivot_pos_error_content=self.check_pivot_pos(shape)




            if freeze_error_content:
                err_list.append(freeze_error_content)
                continue
            elif pivot_pos_error_content:
                err_list.append(pivot_pos_error_content)
                pivot_pos_error_content = []
                continue
            else:
                self.clear_items.append(shape)



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
