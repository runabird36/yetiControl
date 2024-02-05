import maya.cmds as cmds
import os, re
import collections

import checker
#reload (checker)
from checker import Checker


from maya_md import (neon, yt_py)
from general_md_3x import LUCY


import re



class CFXNameChekcer(Checker):

    warn_count = -1
    clear_items = []

    def __init__(self):
        Checker.__init__(self)
        self.set_title("CFX Name Check")
        self.warnings = []
        self.shape_re_ex = re.compile('Shape$|Shape\w+$')

    def remove_shape_postfix(self, tar_list):
        for _idx, _node in enumerate(tar_list):
            if self.shape_re_ex.search(_node):
                print('before : {0}'.format(_node))
                tar_list[_idx] = self.shape_re_ex.sub('', tar_list[_idx])
                print('after : {0}'.format(tar_list[_idx]))
                print('================')

    def execute(self, targets):
        def get_set_list(yeti_list :list) -> list:
            set_list = []
            for cur_yeti in yeti_list:
                connected_nodes = cmds.listConnections(cur_yeti, d=False, s=True, sh=True)
                for node in connected_nodes:
                    if cmds.nodeType(node) == "objectSet":
                        set_list.append({"YETI":cur_yeti, "SET":node})
            return set_list
        
        print('Execute name checker')
        self.warn_count = 0

        asset_name = LUCY.get_assetname()

        all_yetiND_list     = cmds.ls(type='pgYetiMaya')
        all_groomND_list    = cmds.ls(type='pgYetiGroom')
        all_set_list        = get_set_list(all_yetiND_list)
        whole_list = all_yetiND_list + all_groomND_list
        
        self.remove_shape_postfix(all_yetiND_list)
        self.remove_shape_postfix(all_groomND_list)

        for _node in all_yetiND_list+all_groomND_list:
            prefix_name = _node.split('_')[0]
            if prefix_name == asset_name:
                self.clear_items.append(_node)
            else:
                self.add_item(_node, 'The Node is not started with asset name({0})'.format(asset_name), "error", _node)
                self.warn_count += 1


        for _y_node in all_yetiND_list:
            if re.search(r"YETI\_\d{3}$", _y_node):
                to_yeti_name = re.sub(r"YETI\_\d{3}$", "YETI", _y_node)
                _y_node = cmds.rename(_y_node, to_yeti_name)
            postfix_name = _y_node.split('_')[-1]
            if postfix_name == 'YETI':
                self.clear_items.append(_y_node)
            else:
                self.add_item(_y_node, 'Yeti Node is not end with \'YETI\''.format(asset_name), "error", _y_node)
                self.warn_count += 1

        for _g_node in all_groomND_list:
            postfix_name = _g_node.split('_')[-1]
            if postfix_name == 'GRM':
                self.clear_items.append(_g_node)
            else:
                self.add_item(_g_node, 'Yeti Node is not end with \'GRM\''.format(asset_name), "error", _g_node)
                self.warn_count += 1


        for set_yeti_pair in all_set_list:
            cur_yeti  = set_yeti_pair["YETI"]
            _set_node = set_yeti_pair["SET"]
            if re.search(r"set\_\d{3}$", _set_node):
                to_set_name = re.sub(r"set\_\d{3}$", "set", _set_node)
                to_set_name = cmds.rename(_set_node, to_set_name)
                yt_py.update_set_name(cur_yeti, _set_node, to_set_name)



        self.clear_items = list(set(self.clear_items))




    def is_all_clear(self):
        return self.warn_count == 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        self.add_item(msg, "Clear", "clear")


    def virtual_clear(self):
        self.warn_count = 0
