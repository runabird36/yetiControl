# -*- coding: utf-8 -*-

import os
import json
from re import sub
import traceback
from pprint import pprint
import maya.cmds as cmds
import maya.mel as mel
from general_md import shotgun_api3
from general_md_3x import LUCY
from maya_sc.yetiScripts.YTX_toolkit_v02.YTX2New.YTX2New_path_module import (HAIR_STEP_PROJECTS_LIST)



YETI_PIPESTEP = ""




def get_topnode(_groom):
    _long_name = cmds.ls(_groom, l=True)[0]
    for _component in _long_name.split('|'):
        if _component.endswith('_yetiGRP'):
            return _component
    return ''


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
            if tar_attr_key not in convertred_grm_info_dict:
                continue
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
    global YETI_PIPESTEP
    grm_attr_list = ['.partRandomness', '.automaticParting', '.automaticPartingAngleThreshold', '.automaticPartingReferencePosition']
    _sg = connect_sg()
    prj_name = LUCY.get_project()
    # prj_info_dict = _get_prj_info(_sg, prj_name)
    do_with_restposition = cmds.confirmDialog( title='Confirm', message='Rest position과\n함께 적용하시겠습니까?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

    # YETI_PIPESTEP = "hair"
    # if prj_name in HAIR_STEP_PROJECTS_LIST:
    # else:
    #     YETI_PIPESTEP = "characterfx"


    _assetname = cmds.ls(sl=True)[0]
    _assetname = _assetname.split('_')[0]
    ma_pub_path, attr_json_path = _get_path_info(_sg, prj_name,_assetname)
    #
    # attr_json_path = json_pub_path.replace('cfx.json', 'cfx_attr.json')
    # json_pub_path, attr_json_path = get_b2TVC_json(_assetname)
    
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

        if do_with_restposition == "Yes":
            
            save_groom_restPose(groom_list)
        setting_grm_attr(groom_list, convertred_grm_info_dict)
        print(22222222222)
        clean_groupping(top_level_node, texref_address, created_anim_texref_list)
    except Exception as e:
        traceback.print_exc()
        print(str(e))
    cmds.setAttr(top_level_node+'|grm.visibility', False)

    cmds.confirmDialog( title='Confirm', message=u'Save groom rest position 완료!')
