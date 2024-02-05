# -*- coding:utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
import re

geoshape_re_ex = re.compile('GEOShape$|GEOShape\d+$')


def create_shape_info(tar_shape):
    ''' Create texture reference from selected shape '''
    ''' and make dictionary data '''
    _tar_GEOShape = tar_shape
    if cmds.objectType(tar_shape) == 'mesh' and geoshape_re_ex.search(tar_shape):
        tar_shape = cmds.listRelatives(tar_shape, p=True)[0]
    else:
        tar_shape = _tar_GEOShape
    cmds.select(tar_shape)
    existance_check_tar = '{0}_reference'.format(tar_shape)
    if not cmds.objExists(existance_check_tar):
        mel.eval('CreateTextureReferenceObject;')
    else:
        try:
            cmds.delete(existance_check_tar)
            mel.eval('CreateTextureReferenceObject;')
        except Exception as e:
            print( str(e))
    return existance_check_tar


def _run():
    all_yeti_list = cmds.ls(sl=True, dag=True, ni=True, type='pgYetiMaya')
    if all_yeti_list == []:
        print('There is no selected Yeti node!')
        return
    _texref_list = []
    for _y_node in all_yeti_list:
        _linked_node_list = cmds.listConnections(_y_node, d=False, s=True, sh=True)
        _shape_list = []
        _groom_list = []
        _shape_to_grm_info_list = []
        _SET_EXISTS = False
        for _linked_node in _linked_node_list:
            _node_type = cmds.nodeType(_linked_node)
            if _node_type == 'mesh':
                texref_shape = create_shape_info(_linked_node)
                _texref_list.append(texref_shape)
    if cmds.objExists('texref') == False:
        cmds.group(em=True, n='texref')
    else:
        all_children = cmds.listRelatives('texref', c=True)
        cmds.delete(all_children)
    cmds.parent(_texref_list, 'texref')
