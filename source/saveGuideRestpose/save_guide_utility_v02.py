# -*- coding: utf-8 -*-
from importlib import reload
import os
import json
import maya.cmds as cmds
import maya.mel as mel

import PySide2.QtWidgets as QtGui
from pprint import pprint
from source.saveGuideRestpose import select_dialog
reload(select_dialog)







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
    def _maya_main_window():
        '''
        Get the maya main window as a QMainWindow instance
        '''
        import maya.cmds as cmds
        import maya.OpenMayaUI as mui
        from shiboken2 import wrapInstance
        ptr = mui.MQtUtil.mainWindow()
        if ptr is not None:
                return wrapInstance(int(ptr),QtGui.QWidget)



    set_attr_list = ['.mng']
    curves_attr_list = ['.baseAttraction', '.tipAttraction', '.innerRadius', '.outerRadius', '.guideModel', '.attractionProfile[0].attractionProfile_FloatValue', '.attractionProfile[0].attractionProfile_Position', '.attractionProfile[1].attractionProfile_FloatValue', '.attractionProfile[1].attractionProfile_Position']



    main_view = select_dialog.SelectView(_maya_main_window())
    if main_view.exec_():
        json_pub_path = main_view.get_dropped_path()
    else:
        return

    

    # prj_info_dict = _get_prj_info(_sg, prj_name)

    _asset_list = get_all_assetname()
    if _asset_list == []:
        cmds.confirmDialog( title='Info', message=u'There is no selected asset')
        return
    _assetname = _asset_list[0]
    total_dict = {}
    convertred_set_info_dict = {}
    converted_curve_info_dict = {}

    attr_json_path = json_pub_path.replace('cfx.json', 'cfx_attr.json')
    set_info_dict = read_json(attr_json_path).get('objectSet')
    curve_info_dict = read_json(attr_json_path).get('nurbsCurve')
    mesh_info_dict = read_json(attr_json_path).get('mesh')
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
    try:
        cmds.select(deselect=True)

        cmds.select(cur_asset_set_list)

        mel.eval("pgYetiCommand -saveGuidesRestPosition;")
    except Exception as e:
        print(str(e))
    cmds.confirmDialog( title='Confirm', message=u'Save guide rest position 완료!')
