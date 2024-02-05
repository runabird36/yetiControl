
import maya.cmds as cmds
import os, pprint

import checker
#reload (checker)
from checker import Checker


from maya_md import neon



class UVsetChecker(Checker):
    warn_count = -1
    clear_items = []

    def __init__(self):
        Checker.__init__(self)
        self.set_title("UVset Check")
        self.condition_seventh_error_list = []
        self.warnings = []
        self.clear_items = []

        self.check_skip_list = ['baseLattice', 'lattice', 'nurbsCurve', 'locator', 'aiMeshLight']

    def check_multiple_UVsets(self, each_shape):
        # Check Multiple UV Sets

        # check skip with some type
        each_shape_type = cmds.objectType(each_shape)
        if each_shape_type in self.check_skip_list:
            return []

        # return uvset name list of each_shape
        UVsets_info = cmds.polyUVSet(each_shape,q=True,allUVSets=True)

        # check same name
        if UVsets_info != None:
            UVsets_info_set = set(UVsets_info)
            UVsets_info = list(UVsets_info_set)
        else:
            return []

        if len(UVsets_info) >= 2:
            return [each_shape, 'Multiple uvSet and uvSet name error(not \'map1\')']
        elif len(UVsets_info) == 1 and UVsets_info[0] != 'map1':
            return [each_shape, 'uvSet name error(not \'map1\')']
        else:
            return []

    def execute(self, targets):
        '''check
            1. multiple uvset of shapes
            2. name error : uvSet name must be 'map1'
                (if not map1, in maya case, make map1 additionally...)'''
        print('Execute UVset checker')
        



        root_grp = targets[0]
        neon.select_asset(root_grp)
        all_shape = cmds.ls(root_grp, dagObjects = True, shapes = True)


        err_list = []
        for shape in all_shape:

            uvSet_error_contents = self.check_multiple_UVsets(shape)

            if uvSet_error_contents:
                err_list.append(uvSet_error_contents)
            else:
                self.clear_items.append(shape)


        # pprint.pprint(err_list)
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

    def virtual_clear(self):
        self.warn_count = 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        # self.add_item(msg, "Clear", "clear")
        self.add_items([["", msg]])
