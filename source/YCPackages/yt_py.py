

import maya.mel as mel
import maya.cmds as cmds
import os

_main_path = os.path.dirname(os.path.abspath(__file__))
_main_path = _main_path.replace("\\", "/")
_mel_path = _main_path + '/yt_mel.mel'

mel.eval('source "{0}"'.format(_mel_path))



# def listAttr(tar_yeti_node, tar_node):
#     return mel.eval('listAttr(\"{0}\", \"{1}\");'.format(tar_yeti_node, tar_node))



def update_set_name(y_node, from_set, to_set):

    mel.eval('updateSetName(\"{0}\", \"{1}\", \"{2}\")'.format(
                                                            y_node,
                                                            from_set,
                                                            to_set))


def create_yeti_node(node_name):
    return mel.eval('create_yeti_without_addmesh_v02(\"{0}\")'.format(node_name))



def add_basemesh_to_yeti(tar_yeti_node, tar_basemesh):
    mel.eval('pgYetiAddGeometry( \"{0}\", \"{1}\" );'.format(tar_basemesh,
                                                            tar_yeti_node))



def add_set_to_yeti(tar_yeti_node, tar_setname):
    mel.eval("pgYetiAddGuideSet(\"{0}\", \"{1}\")".format(tar_setname, tar_yeti_node))




def import_groom_from_yeti(tar_grm, tar_basemesh, tar_yeti):
    return mel.eval("import_groomFile_from_yNode_v03(\"{0}\", \"{1}\", \"{2}\")".format(tar_grm,
                                                                                        tar_basemesh,
                                                                                        tar_yeti))
