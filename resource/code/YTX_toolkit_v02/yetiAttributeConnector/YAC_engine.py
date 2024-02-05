# -*- coding:utf-8 -*-

import maya.cmds as cmds


def _run():
    to_geo = cmds.ls(sl=True, dag=True, ni=True, typ='mesh')
    tar_grm_list = cmds.ls(sl=True, dag=True, ni=True, typ='pgYetiGroom')
    if to_geo == []:
        print('Error : There is no \"From Mesh\" selection')
        return
    if tar_grm_list == []:
        print('Error : There  is no \"Groom node\" selection')
        return
    to_geo = to_geo[0]
    to_geo_attr = to_geo + ".worldMesh[0]"
    print(to_geo)
    print(str(tar_grm_list) + ", length : " + str(len(tar_grm_list)) )
    if len(tar_grm_list) != 0:
        for _grm in tar_grm_list:
            try:
                tar_grm_attr = _grm + ".inputGeometry"
                cmds.connectAttr(to_geo_attr,tar_grm_attr, f=True)
            except Exception as e:
                print(str(e))
    else:
        print('There is no selection')
