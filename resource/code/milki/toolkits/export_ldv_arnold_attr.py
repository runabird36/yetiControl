import maya.cmds as cmds
import os
import json

from maya_md import neon
from general_md_3x import LUCY

def get_mdl_taskname() -> str:

    all_rn_list = neon.get_all_RNs()
    _tar_rn = ""
    for _rn in all_rn_list:
        if "_mdl" in _rn:
            _tar_rn = _rn
            break

    # This case : 
    #   - ryan_GRP is not referenced (imported)
    if _tar_rn == "":
        ldv_fullpath = LUCY.get_full_path()
        mdl_task_dir = ldv_fullpath.split("lookdev")[0] + "/modeling"
        first_mdl_task = os.listdir(mdl_task_dir)[0]
        return first_mdl_task

    
    rn_fullpath = neon.get_RN_path(_tar_rn)
    return LUCY.get_task(rn_fullpath)


def write_to_json(dict_data, json_file_path):
    with open(json_file_path, 'w') as make_file:
        json.dump(dict_data, make_file)


def get_arnold_attr_dict(target_name):
    # get all arnold attr of all shape
    target_root_GRP = target_name
    all_shape = cmds.ls(target_root_GRP, dag=True, l=True, shapes=True)

    shape_arnold_attr_target_list = ['aiOpaque',
                                        'aiMatte',
                                        'aiSubdivType',
                                        'aiSubdivIterations',
                                        'aiDispHeight',
                                        'aiDispPadding',
                                        'aiDispZeroValue',
                                        'aiDispAutobump',
                                        'primaryVisibility',
                                        'castsShadows',
                                        'aiVisibleInDiffuseReflection',
                                        'aiVisibleInSpecularReflection',
                                        'aiVisibleInDiffuseTransmission',
                                        'aiVisibleInSpecularTransmission',
                                        'aiVisibleInVolume',
                                        'aiSelfShadows',
                                        'aiStepSize',
                                        'aiVolumePadding'
                                        ]

    export_attr_info_dict = {}
    info_dict_for_op = dict.fromkeys(shape_arnold_attr_target_list, [])

    check_except_type_list = ['nurbsCurve']
    for each_shape in all_shape:
        shape_type = cmds.objectType(each_shape)
        if shape_type not in check_except_type_list:
            for arnold_attr in shape_arnold_attr_target_list:

                try:
                    target_attr = '{0}.{1}'.format(each_shape, arnold_attr)
                    target_attr_value = cmds.getAttr(target_attr)
                    export_attr_info_dict[target_attr] = target_attr_value
                except Exception as e:
                    # like nurbsCurve...
                    print(e)
                    print('In this shape, there is no {0} attribute'.format(target_attr))

    return export_attr_info_dict


def get_arnold_attr_dict_v02(target_name):
    # get all arnold attr of all shape
    # target_root_GRP = 'ryan_GRP'
    target_root_GRP = target_name
    _assetname = target_root_GRP[0].split('_')[0]
    all_shape = cmds.ls(target_root_GRP, dag=True, shapes=True)

    # if you want to view other arnold attribute,
    # select one shape and execute 'cmds.listAttr(target) command'
    shape_arnold_attr_target_list = ['aiOpaque',
                                        'aiMatte',
                                        'aiSubdivType',
                                        'aiSubdivIterations',
                                        'aiDispHeight',
                                        'aiDispPadding',
                                        'aiDispZeroValue',
                                        'aiDispAutobump',
                                        'primaryVisibility',
                                        'castsShadows',
                                        'aiVisibleInDiffuseReflection',
                                        'aiVisibleInSpecularReflection',
                                        'aiVisibleInDiffuseTransmission',
                                        'aiVisibleInSpecularTransmission',
                                        'aiVisibleInVolume',
                                        'aiSelfShadows',
                                        'aiStepSize',
                                        'aiVolumePadding'
                                        ]
    default_val = [True, False, 0, 1, 1.0, 0.0, 0.0, False, True, True, True, True, True, True, True, True]
    
    info_dict_for_op = {}
    for _attrname in shape_arnold_attr_target_list:
        info_dict_for_op[_attrname] = {}
    # export_str_info_str = ''
    check_except_type_list = ['nurbsCurve']
    for each_shape in all_shape:
        shape_type = cmds.objectType(each_shape)
        if shape_type not in check_except_type_list:
            for _idx, arnold_attr in enumerate(shape_arnold_attr_target_list):

                try:
                    target_attr = '{0}.{1}'.format(each_shape, arnold_attr)
                    target_attr_value = cmds.getAttr(target_attr)
                    
                    if target_attr_value == default_val[_idx]:
                        continue
                    if target_attr_value not in info_dict_for_op[arnold_attr]:
                        info_dict_for_op[arnold_attr][target_attr_value] = [] 
                    info_dict_for_op[arnold_attr][target_attr_value].append(each_shape)
                    
                         
                except Exception as e:
                    # like nurbsCurve...
                    print(str(e))
                    print('In this shape, there is no {0} attribute'.format(target_attr))
                    
                    
                    
    
    
    #======================================================================
    #SHADING NETWORK : check Dismap
    #======================================================================
    for shadingGroup in neon.get_shading_groups_in_hierarchy(target_root_GRP[0]):
        
        dispName = neon.get_source(shadingGroup, 'displacementShader')
        

        #Create Shader Assign
        shd_setparam = []
        if not dispName == None:
            shd_setparam.append('disp_map = ' '\"' + dispName + '.displacement' + '\"')
    
    
    return info_dict_for_op







def execute_export(export_attr_info_dict, pub_path):
    
    json_dir_path = os.path.dirname(pub_path)
    if not os.path.exists(json_dir_path):
        os.makedirs(json_dir_path)


    # make json and write dict info
    write_to_json(export_attr_info_dict, pub_path)



    
