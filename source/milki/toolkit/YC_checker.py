
from importlib import reload
import maya.cmds as cmds
import maya.mel as mel

import os, pprint, time, json, re, sys


from source.YCPackages import (neon, yt_py)


from source.YC_core_module import (__PUB_PATH_TEMPLATE__,
                                    get_assetname,
                                    get_pub_paths)


def remove_shape_postfix(tar_list):
    shape_re_ex = re.compile('Shape$|Shape\w+$')
    for _idx, _node in enumerate(tar_list):
        if shape_re_ex.search(_node):
            print('before : {0}'.format(_node))
            tar_list[_idx] = shape_re_ex.sub('', tar_list[_idx])
            print('after : {0}'.format(tar_list[_idx]))
            print('================')

def get_set_list(yeti_list :list) -> list:
    set_list = []
    for cur_yeti in yeti_list:
        connected_nodes = cmds.listConnections(cur_yeti, d=False, s=True, sh=True)
        for node in connected_nodes:
            if cmds.nodeType(node) == "objectSet":
                set_list.append({"YETI":cur_yeti, "SET":node})
    return set_list
        



def check_setname_and_fix() -> None:
    all_yetiND_list     = cmds.ls(type='pgYetiMaya')
    all_set_list        = get_set_list(all_yetiND_list)
    for set_yeti_pair in all_set_list:
        cur_yeti  = set_yeti_pair["YETI"]
        _set_node = set_yeti_pair["SET"]
        if re.search(r"set\_\d{3}$", _set_node):
            to_set_name = re.sub(r"set\_\d{3}$", "set", _set_node)
            to_set_name = cmds.rename(_set_node, to_set_name)
            yt_py.update_set_name(cur_yeti, _set_node, to_set_name)



def check_yeti_components_name_convention() -> list:

    prefix_error_list   = []
    postfix_error_list  = []

    asset_name = get_assetname()
    if asset_name == "":
        return ["There is no selected asset"]

    all_yetiND_list     = cmds.ls(type='pgYetiMaya')
    all_groomND_list    = cmds.ls(type='pgYetiGroom')
    whole_list = all_yetiND_list + all_groomND_list
    
    remove_shape_postfix(all_yetiND_list)
    remove_shape_postfix(all_groomND_list)


    for _node in all_yetiND_list+all_groomND_list:
        prefix_name = _node.split('_')[0]
        if prefix_name != asset_name:
            prefix_error_list.append(_node)


    
    for _y_node in all_yetiND_list:
        if re.search(r"YETI\_\d{3}$", _y_node):
            to_yeti_name = re.sub(r"YETI\_\d{3}$", "YETI", _y_node)
            _y_node = cmds.rename(_y_node, to_yeti_name)
        postfix_name = _y_node.split('_')[-1]
        if postfix_name != 'YETI':
            postfix_error_list.append(_y_node)
            


    for _g_node in all_groomND_list:
        postfix_name = _g_node.split('_')[-1]
        if postfix_name != 'GRM':
            postfix_error_list.append(_g_node)

    
    return prefix_error_list + postfix_error_list

