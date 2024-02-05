import maya.cmds as cmds
import maya.mel as mel
import os, glob
import sys

import checker
#reload (checker)
from checker import Checker

from maya_md import neon
from general_md_3x import LUCY
import re


class CFXTexChekcer(Checker):
    warn_count = -1
    clear_items = []

    def __init__(self):
        Checker.__init__(self)
        self.set_title("CFX Tex Check")
        self.warnings = []
        self.shape_re_ex = re.compile('Shape$|Shape\w+$')
        if sys.platform.count("win"):
            mel.eval('source "Z:/backstage/maya/milki/toolkits/yeti_util.mel"')
        else:
            mel.eval("source \"/usersetup/linux/scripts/maya_sc/milki/toolkits/yeti_util.mel\"")


    def execute(self, targets):
        print('Execute name checker')
        self.warn_count = 0

        asset_name = LUCY.get_assetname()

        all_yetiND_list = cmds.ls(type='pgYetiMaya')


        whole_info_dict = {}
        for _y_node in all_yetiND_list:
            tex_node_and_tex_list = mel.eval("get_mask_path_list(\"{0}\");".format(_y_node))
            tex_node_list = tex_node_and_tex_list[0::2]
            tex_fname_list = tex_node_and_tex_list[1::2]
            whole_info_dict[_y_node] = zip(tex_node_list, tex_fname_list)


        for _y_node, _tex_graph_info in whole_info_dict.items():
            tex_dirpath = cmds.getAttr(_y_node+'.imageSearchPath')

            for _tex_node, _tex_fname in _tex_graph_info:
                _fullpath = '{0}/{1}'.format(tex_dirpath, _tex_fname)
                if os.path.isfile(_tex_fname) == True:
                    self.add_item(_y_node, 'Yeti Node : {0} / Tex Node : {1} : The node has full file path'.format(_y_node, _tex_node), "error", _y_node)
                    self.warn_count += 1
                elif '<udim>' in _fullpath.lower():
                    if '<udim>' in _fullpath:
                        _fullpath_with_magic_star = _fullpath.replace('<udim>', '*')
                    elif '<UDIM>' in _fullpath:
                        _fullpath_with_magic_star = _fullpath.replace('<UDIM>', '*')
                    else:
                        _fullpath_with_magic_star = _fullpath

                    if glob.glob(_fullpath_with_magic_star) == []:
                        self.add_item(_y_node, 'Yeti Node : {0} / Tex Node : {1} : Tex File does not exists : {2}'.format(_y_node, _tex_node, _tex_fname), "error", _y_node)
                        self.warn_count += 1

                elif os.path.exists(_fullpath) == False:
                    self.add_item(_y_node, 'Yeti Node : {0} / Tex Node : {1} : Tex File does not exists : {2}'.format(_y_node, _tex_node, _tex_fname), "error", _y_node)
                    self.warn_count += 1
                else:
                    self.clear_items.append(_tex_node)






        self.clear_items = list(set(self.clear_items))




    def is_all_clear(self):
        return self.warn_count == 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        self.add_item(msg, "Clear", "clear")


    def virtual_clear(self):
        self.warn_count = 0
