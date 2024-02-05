# -*- coding:utf-8 -*-

import os
import maya.cmds as cmds
import maya.mel as mel


def get_selected_yeti_node():
    return cmds.ls(sl=True, dag=True, ni=True, typ='pgYetiMaya')


def get_texnode_list_from_yeti(_yeti):
    return mel.eval("get_texnode_list(\"{0}\")".format(_yeti))


def get_tex_file_name_from_texnode(_yeti, _texnode):
    return mel.eval("get_filename_from_texnode(\"{0}\",\"{1}\")".format(_yeti, _texnode))


def get_ISPpath(_yeti):
    return str(cmds.getAttr(_yeti+'.imageSearchPath'))


def set_ISPpath(_yeti, _dirpath):
    try:
        cmds.setAttr(_yeti+'.imageSearchPath', _dirpath, typ='string')
    except Exception as e:
        print(str(e))


def set_tex_filename_in_texnode(_yeti, _texnode, _filename):
    try:
        mel.eval("set_filename_in_texnode(\"{0}\",\"{1}\", \"{2}\")".format(_yeti, _texnode, _filename))
    except Exception as e:
        print(str(e))


def make_script_path(_from_path):
    _mid_path = os.path.realpath(_from_path)
    return _mid_path.replace('\\', '/')




def does_exist(_path):
    _path = make_script_path(_path)

    if '<udim>' in _path.lower():
        try:
            _filename = os.path.basename(_path).split('.')[0]
            _dir_path = os.path.dirname(_path)

            for _check_tar in os.listdir(_dir_path):
                if _filename in _check_tar:
                    return True
        except:
            return False
    else:
        return os.path.exists(_path)
