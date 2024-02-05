import json
import shutil, os
import pprint
from sys import argv

def read_json(write_json_path):
    with open(write_json_path, 'r') as f:
        json_data_from_file = json.load(f)
    return json_data_from_file

def set_mdl_arnold_attr():
    '''
    in :
       - argv[0] : python code path
       - argv[1] : arnold attr info of all shape from ldv (dict)

    out :

    '''
    import maya.standalone
    maya.standalone.initialize()
    import maya.cmds as cmds

    mdl_pub_full_path = argv[1]
    json_full_path = argv[2]

    cmds.file(mdl_pub_full_path, force=True, open=True)



    imported_attr_info_dict = read_json(json_full_path)
    for key_attr_name, value_attr_value in imported_attr_info_dict.items():
        if '|' in key_attr_name:
            key_attr_name = key_attr_name.replace('|', '*|*')
        else:
            key_attr_name = key_attr_name.replace('GEOShape', 'GEOShape*')
            key_attr_name = '*{0}'.format(key_attr_name)

        all_attr_tar_list = cmds.ls(key_attr_name)
        for _tar_attr in all_attr_tar_list:
            try:
                cmds.setAttr(_tar_attr, value_attr_value)
            except:
                pass

    # imported_attr_info_list = import_attr_info_str.split('/')
    # for attr_info_set in imported_attr_info_list:
    #     attr_and_value_list = attr_info_set.split(':')
    #     target_attr = attr_and_value_list[0]
    #     target_attr_value = attr_and_value_list[1]
    #     cmds.setAttr(target_attr, target_attr_value)

    cmds.file(save=True, type="mayaAscii")


if __name__ == "__main__":
    set_mdl_arnold_attr()
