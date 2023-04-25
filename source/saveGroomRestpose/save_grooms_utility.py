# -*- coding: utf-8 -*-

import os
import json
import traceback
import PySide2.QtWidgets as QtGui
import maya.cmds as cmds
import maya.mel as mel

from source.saveGroomRestpose import select_dialog

def get_topnode(_groom):
    _long_name = cmds.ls(_groom, l=True)[0]
    for _component in _long_name.split('|'):
        if _component.endswith('_yetiGRP'):
            return _component
    return ''


def read_json(write_json_path):
        with open(write_json_path, 'r') as f:
            json_data_from_file = json.load(f)
        return json_data_from_file


def get_linked_basemesh():
    top_level_node = ''
    texref_address = ''
    real_groom_list = []
    real_basemesh_list = []
    selected_groom_list = cmds.ls(sl=True, l=True)
    for _groom in selected_groom_list:
        if texref_address == '':
            top_level_node = get_topnode(_groom)
            texref_address = '*|' + top_level_node + '|texref'
        if cmds.nodeType(_groom) != 'pgYetiGroom':
            _groom = cmds.listRelatives(_groom, ad=True, f=True, ni=True)[0]
        _input_geo_attr = _groom + '.inputGeometry'
        _linked_worldmesh_attr = cmds.connectionInfo(_input_geo_attr, sfd=True)
        _linked_basemesh = _linked_worldmesh_attr.split('.')[0]
        real_groom_list.append(_groom)
        real_basemesh_list.append(_linked_basemesh)
    real_basemesh_list = list(set(real_basemesh_list))
    return real_groom_list, real_basemesh_list, top_level_node, texref_address


def create_anim_texRef(basemesh_list):
    created_texRef_list = []
    for _basemesh in basemesh_list:
        linked_old_texRef_attr = cmds.connectionInfo(_basemesh+'.referenceObject', sfd=True)
        cmds.disconnectAttr(linked_old_texRef_attr, _basemesh+'.referenceObject')
        transform_name = cmds.listRelatives(_basemesh, p=True, f=True)[0]
        cmds.select(transform_name)
        mel.eval('CreateTextureReferenceObject;')
        created_anim_texref = cmds.ls(sl=True, l=True)[0]
        created_texRef_list.append(created_anim_texref)
    return created_texRef_list


def save_groom_restPose(groom_list):
    cmds.select(groom_list)
    mel.eval('pgYetiSaveGroomRestPoseOnSelected;')


def setting_grm_attr(groom_list, convertred_grm_info_dict):
    grm_attr_list = ['.partRandomness', '.automaticParting', '.automaticPartingAngleThreshold', '.automaticPartingReferencePosition']
    for _grm_longname in groom_list:
        for _tar_attr in grm_attr_list:
            _grm = _grm_longname.split('|')[-1]
            tar_attr_key = _grm + _tar_attr
            tar_attr_value = convertred_grm_info_dict[tar_attr_key]
            tar_attr_fullname = _grm_longname + _tar_attr
            try:
                cmds.setAttr(tar_attr_fullname, tar_attr_value)
            except Exception as e:
                print(str(e))


def clean_groupping(top_level_node, texref_address, anim_texref_list):
    if cmds.objExists(texref_address) == False:
        cmds.group(em=True, p=top_level_node, n='texref')
    if cmds.listRelatives(texref_address, c=True) != []:
        try:
            old_texref_list = cmds.listRelatives(texref_address, c=True)
            cmds.delete(old_texref_list)
        except Exception as e:
            print(str(e))
    try:
        cmds.parent(anim_texref_list, texref_address)
        cmds.setAttr(texref_address+'.visibility', False)
        return True
    except Exception as e:
        print(str(e))
        return False



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

    grm_attr_list = ['.partRandomness', '.automaticParting', '.automaticPartingAngleThreshold', '.automaticPartingReferencePosition']
    
    main_view = select_dialog.SelectView(_maya_main_window())
    if main_view.exec_():
        attr_json_path = main_view.get_dropped_path()
    else:
        return
    
    
    
    
    _assetname = cmds.ls(sl=True)[0]
    _assetname = _assetname.split('_')[0]
    
    
    grm_info_dict = read_json(attr_json_path).get('pgYetiGroom')


    # convert dict list to dict
    convertred_grm_info_dict = {}
    for _grm_info in grm_info_dict:
        _grm_attr_fullname = _grm_info.get('ATTR_FULLNAME')
        _grm_attr_value = _grm_info.get('ATTR_VALUE')
        convertred_grm_info_dict[_grm_attr_fullname] = _grm_attr_value


    try:
        groom_list, basemesh_list, top_level_node, texref_address = get_linked_basemesh()
        created_anim_texref_list = create_anim_texRef(basemesh_list)
        save_groom_restPose(groom_list)

        setting_grm_attr(groom_list, convertred_grm_info_dict)

        clean_groupping(top_level_node, texref_address, created_anim_texref_list)
    except Exception as e:
        traceback.print_exc()
        print(str(e))
    cmds.setAttr(top_level_node+'|grm.visibility', False)

    cmds.confirmDialog( title='Confirm', message=u'Save groom rest position 완료!')
