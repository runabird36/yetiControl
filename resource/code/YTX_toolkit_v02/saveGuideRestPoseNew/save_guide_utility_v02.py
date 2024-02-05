# -*- coding: utf-8 -*-

import os, sys
import json
from re import sub
try:
    import maya.cmds as cmds
    import maya.mel as mel
    from general_md import shotgun_api3
    from general_md_3x import LUCY
    from pprint import pprint
    from maya_sc.yetiScripts.YTX_toolkit_v02.YTX2New.YTX2New_path_module import (HAIR_STEP_PROJECTS_LIST)
except:
    sys.path.append("/usersetup/linux/module")
    from general_md import shotgun_api3




YETI_PIPESTEP = ""



def connect_sg():
    SERVER_PATH = 'https://giantstep.shotgunstudio.com'
    SCRIPT_NAME = 'basic_api'
    SCRIPT_KEY = 'b6dbe937304b44ce2b470d9f817e01941e9412029494bf48896b0617db4c9a1e'
    try:
        proxied_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy='proxy1.giantstep.net:9098')
    except:
        proxied_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
    return proxied_sg


def _get_prj_info(_sg, prj_name):
    filters = [['sg_status', 'is', 'Active']]
    filters.append(['name','is',prj_name])
    field = ['type', 'id','name']
    prj_info_dict =  _sg.find('Project', filters, field)
    return prj_info_dict[0]


def _get_path_info(_sg, project, asset_name):
    ''' This for getting ma path and json path info '''
    global YETI_PIPESTEP

    files = []
    filters = [['project.Project.name', 'is', project],
                    {
                        'filter_operator' : 'all',
                        'filters': [
                                    ['code', 'contains',  asset_name],
                                    ['code', 'not_contains',  "_basemesh"],
                                    ['sg_published_pipe_step', 'is', YETI_PIPESTEP]
                                   ]
                     }

                      ]
    field = ['code', 'path','created_at']
    try:
        files =  _sg.find('PublishedFile', filters, field)
    except Exception as e:
        print(e)
        files =[]
    
    files.sort(key=lambda x : x.get("created_at"))
    cfx_mbs = []
    for file in files:
        fileName =  file['path']['name']
        # if not 'publish' in fileName and not 'pub' in fileName:
        #     files.remove(file)
        #     continue
        ext = os.path.splitext(fileName)[1]
        if not ext in ['.mb', '.ma']:
            continue
        cfx_mbs.append(file)
    
    cfx_pub_path = cfx_mbs[-1]['path']['url']
    cfx_pub_dir = os.path.dirname(cfx_pub_path)
    cfx_pub_basename = os.path.basename(cfx_pub_path)
    cfx_pub_json_dir = cfx_pub_dir.replace('/pub/mb', '/pub/json')
    json_basename = sub(r"\.mb", "_attr.json", cfx_pub_basename)
    json_full_path = '{0}/{1}'.format(cfx_pub_json_dir, json_basename)
    if 'file:////' in cfx_pub_path:
        cfx_pub_path = cfx_pub_path.replace('file:////','/')
    if 'file:////' in json_full_path:
        json_full_path = json_full_path.replace('file:////','/')
    print(cfx_pub_path, '\n', json_full_path)
    return [cfx_pub_path, json_full_path]


def read_json(write_json_path):
        with open(write_json_path, 'r') as f:
            json_data_from_file = json.load(f)
        return json_data_from_file


def get_all_assetname():
    _check_list = cmds.ls(sl=True)
    _asset_list = []
    for _check in _check_list:
        _check = _check.split('_')[0]
        if _check in _asset_list:
            continue
        else:
            _asset_list.append(_check)
    return list(set(_asset_list))


def curve_attr_setting(curve_shapes_list, converted_curve_info_dict):
        for _attr_fullname, _attr_value in converted_curve_info_dict.items():
            try:
                cmds.setAttr(_attr_fullname, _attr_value)
            except Exception as e:
                print(str(e) + _attr_fullname)


def _run():
    global YETI_PIPESTEP
    set_attr_list = ['.mng']
    curves_attr_list = ['.baseAttraction', '.tipAttraction', '.innerRadius', '.outerRadius', '.guideModel', '.attractionProfile[0].attractionProfile_FloatValue', '.attractionProfile[0].attractionProfile_Position', '.attractionProfile[1].attractionProfile_FloatValue', '.attractionProfile[1].attractionProfile_Position']


    do_with_restposition = cmds.confirmDialog( title='Confirm', message='Rest position과\n함께 적용하시겠습니까?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )


    _sg = connect_sg()
    prj_name = LUCY.get_project()
    
    
    YETI_PIPESTEP = "hair"
    # if prj_name in HAIR_STEP_PROJECTS_LIST:
    # else:
    #     YETI_PIPESTEP = "characterfx"


    _asset_list = get_all_assetname()

    total_dict = {}
    convertred_set_info_dict = {}
    converted_curve_info_dict = {}
    for _assetname in _asset_list:
        ma_pub_path, attr_json_path = _get_path_info(_sg, prj_name,_assetname)
        # attr_json_path = json_pub_path.replace('cfx.json', 'cfx_attr.json')
        attr_info_dict = read_json(attr_json_path)
        # pprint(attr_info_dict)
        set_info_dict = attr_info_dict.get('objectSet')
        curve_info_dict = attr_info_dict.get('nurbsCurve')
        mesh_info_dict = attr_info_dict.get('mesh')
        # convert dict list to dict
        cur_asset_set_list = cmds.ls(_assetname+'_*', sl=True, ni=True, typ='objectSet')
        # set objectSet attribute
        for _set_info in set_info_dict:
            _set_attr_fullname = _set_info.get('ATTR_FULLNAME')
            _set_attr_value = _set_info.get('ATTR_VALUE')

            key_set_name = _set_attr_fullname.split('.')[0]
            tar_attr_name = _set_attr_fullname.split('.')[1]



            for real_set_name in cur_asset_set_list:

                if key_set_name in real_set_name:
                    real_attr_fullname = '{0}.{1}'.format(real_set_name, tar_attr_name)
                    try:
                        if _set_attr_value == None:
                            _set_attr_value = 1
                        cmds.setAttr(real_attr_fullname, _set_attr_value)
                    except Exception as e:
                        print(str(e))
        # set curve shape attribute
        sorted_info = {}
        for _curve_info in curve_info_dict:
            _curve_attr_fullname = _curve_info.get('ATTR_FULLNAME')

            _tmp_set_name = _curve_attr_fullname.split('.')[0]


            if _tmp_set_name in sorted_info:
                sorted_info[_tmp_set_name].append(_curve_info)
            else:
                sorted_info[_tmp_set_name] = [_curve_info]


        for key_set_name, attr_info_list in sorted_info.items():
            curve_list_of_set = cmds.sets(key_set_name+'*', q=True)
            cv_shapes_list = cmds.ls(curve_list_of_set, dag=True, ni=True, shapes=True)
            for _attr_info_dict in attr_info_list:
                attr_fullname = _attr_info_dict.get('ATTR_FULLNAME')
                _tmp = attr_fullname.split('.')
                _tmp.pop(0)
                attr_name = '.'.join(_tmp)
                attr_value = _attr_info_dict.get('ATTR_VALUE')

                for _cv_shapes in cv_shapes_list:
                    real_cv_attr_fullname = '{0}.{1}'.format(_cv_shapes, attr_name)
                    try:
                        if attr_value == None:
                            attr_value = 1
                        cmds.setAttr(real_cv_attr_fullname, attr_value)
                    except Exception as e:
                        print(str(e))

        # ========================================================================================
        # set mesh shape attribute
        # ========================================================================================
        for _mesh_info in mesh_info_dict:
            _mesh_attr_fullname = _mesh_info.get('ATTR_FULLNAME')
            _mesh_attr_value = _mesh_info.get('ATTR_VALUE')

            _shape_name = _mesh_attr_fullname.split('.')[0]
            _shape_attr_name = _mesh_attr_fullname.split('.')[1]


            all_shape_list = cmds.ls(_shape_name, l=True)

            for _cur_shape in all_shape_list:
                real_attr_fullname = '{0}.{1}'.format(_cur_shape, _shape_attr_name)
                print(real_attr_fullname, '--->', _mesh_attr_value)
                print('='*50)
                try:
                    if _mesh_attr_value == None:
                        continue
                    cmds.setAttr(real_attr_fullname, _mesh_attr_value)
                except Exception as e:
                    print(str(e))


        # Save guide rest pose
        print(222222222222)
        if do_with_restposition == "Yes":
            print(1111111111111)
            try:
                cmds.select(deselect=True)

                cmds.select(cur_asset_set_list)

                mel.eval("pgYetiCommand -saveGuidesRestPosition;")
            except Exception as e:
                print(str(e))
    cmds.confirmDialog( title='Confirm', message=u'Save guide rest position 완료!')



