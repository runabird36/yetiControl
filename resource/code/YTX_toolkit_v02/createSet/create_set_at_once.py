# -*- coding:utf-8 -*-

import maya.cmds as cmds


def cusmtom_rename(from_fullpath_name):
    target_name = from_fullpath_name.split('|')[-1]
    if target_name.endswith('_grp'):
        to_name = target_name.replace('_grp', '_set')
    elif target_name.endswith('_GRP'):
        to_name = target_name.replace('_GRP', '_set')
    else:
        to_name = target_name + '_set'
    return to_name


def is_curve_transform(transform_name):
    shape_name = cmds.listRelatives(transform_name, c=True)[0]
    if cmds.nodeType(shape_name) == 'nurbsCurve':
        return True
    else:
        return False


def find_curve_parent03(_grp_name):
    check_tar_list = cmds.listRelatives(_grp_name, c=True)
    check_tar = check_tar_list[0]
    if is_curve_transform(check_tar) == True:
        return [_grp_name]
    else:
        cv_grp_name_list = []
        for _tar in check_tar_list:
            cv_grp_name = find_curve_parent03(_tar)
            cv_grp_name_list.extend(cv_grp_name)
        return cv_grp_name_list


def _start_make_curve_set(selected_tar_list):
    all_cv_grp_list = []
    for _tar in selected_tar_list:
        cv_grp_list = find_curve_parent03(_tar)
        all_cv_grp_list.extend(cv_grp_list)
    for curve_grp in all_cv_grp_list:
        curve_list = cmds.listRelatives(curve_grp, f=True, c=True)
        cmds.select(curve_list)
        to_curve_grp_name = cusmtom_rename(curve_grp)
        if cmds.objExists(to_curve_grp_name) == True:
            try:
                cmds.delete(to_curve_grp_name)
            except Exception as e:
                print( str(e))
        cmds.sets(name=to_curve_grp_name)


def _run():
    sel_target_list = cmds.ls(sl=True)
    if sel_target_list == []:
        cmds.confirmDialog(title='Check', message='There is no selection!!')
    else:
        _start_make_curve_set(sel_target_list)
