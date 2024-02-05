import maya.cmds as cmds
import os

import checker
# reload (checker)
from checker import Checker

from pprint import pprint


from maya_md import neon


class HistoryChekcer(Checker):

    warn_count = -1
    clear_items = []
    def __init__(self):
        Checker.__init__(self)
        self.set_title("Transform History Check")
        self._except_list = ['initialShadingGroup']
        self._except_nodeType_list = ['groupId', 'objectSet']

    def findRelatedDeltaMush(self, geometry, each_mesh):
        """
        Return the delta mush deformer attached to the specified geometry

        Args:
          geometry (str): Geometry object/transform to query

        Returns:
          str
        """
        # Check geometry
        if not cmds.objExists(geometry):
            raise Exception('Object '+geometry+' does not exist!')

        hist = cmds.listHistory(geometry, pdo=1)
        if hist is None:
            return


        hist = list(set(hist) - set(self._except_list))
        removed_history_list = []
        for _check_tar in hist:
            if cmds.nodeType(_check_tar) in self._except_nodeType_list:
                continue
            else:
                removed_history_list.append(_check_tar)
        if removed_history_list:
            return [each_mesh , "history exist : {0}, type : {1}".format(each_mesh, removed_history_list[0])]



    def check_history_exist(self, each_mesh_full_path, each_mesh):
        '''condition 6 : every trasform history should be deleted'''
        obj_history_list = []
        shadingEngines = []
        only_transform_history = []
        obj_history_list = cmds.listHistory(each_mesh_full_path, future = True)
        shadingEngines = cmds.listConnections(obj_history_list,t='shadingEngine')


        if shadingEngines == None or obj_history_list == None:
            return
        only_transform_history = set(obj_history_list) - set(shadingEngines)



        # gather remove targets by object type
        remove_target_stack = []
        for history in only_transform_history:
            history_type = cmds.objectType(history)


            if history_type == 'objectSet':
                remove_target_stack.append(history)
            elif history_type == 'nodeGraphEditorInfo':
                remove_target_stack.append(history)
            elif history_type == 'renderLayer':
                remove_target_stack.append(history)


        # remove history from 'only_transform_history' list that doen't have to delete
        for target in remove_target_stack:
            only_transform_history.remove(target)



        if len(only_transform_history) > 1:
            for error_target in only_transform_history:
                error_type = cmds.objectType(error_target)
                if error_type == 'mesh':
                    continue
                else:
                    return [each_mesh , "history exist : {0}, type : {1}".format(error_target, error_type)]




    def execute(self, targets):
        print('Execute history checker')
        root_grp = targets[0]
        error_content = []
        neon.select_asset(root_grp)
        all_shape = cmds.ls(root_grp, dagObjects = True, long = True, shapes = True)

        divider = '|'
        mesh_index = -1
        list_for_reset_warn_count = []
        for  shape in all_shape:
            shape_list = shape.split(divider)

            each_mesh = shape_list[mesh_index]
            # condition 6
            error_content = self.findRelatedDeltaMush(shape, each_mesh)
            if error_content:
                list_for_reset_warn_count.append(error_content)
                # self.add_warnning(error_content[0], error_content[1], "error", error_content[0])
                self.warn_count += 1
            else:
                # 'history clear!'
                self.clear_items.append(each_mesh)

        if list_for_reset_warn_count == []:
            self.warn_count = 0
        else:
            self.add_items(list_for_reset_warn_count)


    def is_all_clear(self):
        return self.warn_count == 0

    def virtual_clear(self):
        self.warn_count = 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        self.add_items([["", msg]])
