

import maya.mel as mel
import maya.cmds as cmds


def set_display_setting(shortcut_number :str) -> None:
    if shortcut_number == "1":
        mel.eval("displaySmoothness -divisionsU 0 -divisionsV 0 -pointsWire 4 -pointsShaded 1 -polygonObject 1;")
    elif shortcut_number == "3":
        mel.eval("displaySmoothness -divisionsU 3 -divisionsV 3 -pointsWire 16 -pointsShaded 4 -polygonObject 3;")



def sel_all_loc():
    rig_loc_list = cmds.ls('*_*:*_rig|*_*:loc')
    plus_loc_list = []
    for _rig in rig_loc_list:
        try:
            find_res = cmds.listRelatives(_rig, c=True)
            if find_res == None:
                continue
            asset_GRP = find_res[0]
            plus_loc_list.append(asset_GRP)
        except:
            continue
    cmds.select(cl=True)
    cmds.select(plus_loc_list)

def sel_all_geo():
    rig_list = cmds.ls('*_*:*_rig|*_*:geo')
    plus_list = []
    for _rig in rig_list:
        try:
            asset_GRP = cmds.listRelatives(_rig,c=True)[0]
            plus_list.append(asset_GRP)
        except:
            continue
    cmds.select(cl=True)
    cmds.select(plus_list)