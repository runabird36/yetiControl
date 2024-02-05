# -*- coding: utf-8 -*-

import os
import json
import maya.cmds as cmds
import maya.mel as mel
from general_md import shotgun_api3
from general_md import scn
from pprint import pprint


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


def _run():

    

    _asset_list = get_all_assetname()

    
    for _assetname in _asset_list:
        cur_asset_set_list = cmds.ls(_assetname+'_*', sl=True, ni=True, typ='objectSet')
        

        # Save guide rest pose
        try:
            cmds.select(deselect=True)

            cmds.select(cur_asset_set_list)

            mel.eval("pgYetiCommand -saveGuidesRestPosition;")
        except Exception as e:
            print(str(e))
    cmds.confirmDialog( title='Confirm', message=u'Save guide rest position 완료!')
