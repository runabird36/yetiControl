import maya.cmds as cmds
import os, re
import collections

import checker
# reload (checker)
from checker import Checker

import pickle, pprint

from maya_md import neon
from general_md_3x import LUCY





class CFXGeoChecker(Checker):

    warn_count = 0
    clear_items = []
    def __init__(self):
        Checker.__init__(self)
        self.set_title("CFX Geo Check")
        self.rig_check_flag = False

    def get_hichy_shapes(self, hichy_path, step='mdl'):
        try:
            with open(hichy_path, "rb") as p:
                _all_shape = pickle.load(p)
        except Exception as e:
            print(str(e))
            error_msg = 'There is no {0} hichy file!!!(hichy)'.format(step)
            self.add_warnning('', error_msg, "error", '')
            self.warn_count += 1
        return _all_shape

    def compare_shapes(self, from_shape_list, to_shape_list):
        unmatched_hichy_from_geo = set(from_shape_list) - set(to_shape_list)
        unmatched_hichy_to_geo = set(to_shape_list) - set(from_shape_list)
        return list(unmatched_hichy_to_geo)

    def execute(self, targets):



        # get cfx full path
        #           - sample data : X:/projects/2020_02_pipelineFX/assets/prop/ssong/cfx/dev/scenes/maya/ssong_cfx_v01.mb
        cfx_full_path = LUCY.get_full_path()
        parent_path = cfx_full_path.split('/cfx/')[0]






        # make mdl hichy path from cfx full path
        #            - smaple data : X:\projects\2020_02_pipelineFX\assets\prop\ssong\mdl\pub\hichy\pub_ssong_mdl.hichy
        # make rig hichy path from cfx full path
        # and check existance of hichy file
        #            - sample data : X:\projects\2020_02_pipelineFX\assets\prop\ssong\rig\pub\hichy\pub_ssong_rig.hichy
        asset_name = LUCY.get_assetname()
        mdl_hichy_path = '{0}/mdl/pub/hichy/pub_{1}_mdl.hichy'.format(parent_path, asset_name)
        rig_hichy_path = '{0}/rig/pub/hichy/pub_{1}_rig.hichy'.format(parent_path, asset_name)
        # rig_hichy_dir_path = os.path.dirname(rig_hichy_path)
        if os.path.exists(rig_hichy_path):
            self.rig_check_flag = True
        else:
            self.rig_check_flag = False
            # self.add_warnning(targets[0], 'rig pub data does not exist or does not published!!!check please!!!', 'error')
            # self.warn_count += 1
            return






        # get all transform and shape (ls -dagObjects -long)
        cfx_all_shape = cmds.ls(targets[0], dagObjects = True, long = True)
        mdl_all_shape = []
        rig_all_shape = []

        mdl_all_shape = self.get_hichy_shapes(mdl_hichy_path, 'mdl')
        if self.rig_check_flag == True:
            rig_all_shape = self.get_hichy_shapes(rig_hichy_path, 'rig')
            print('RIG Shape list')
            pprint.pprint(rig_all_shape)

        if len(mdl_all_shape) == 0:
            error_msg = 'There is no mdl team shapes info, need to check mdl pub data(hichy)'
            self.add_warnning('', error_msg, "error", '')
            self.warn_count += 1

        if self.rig_check_flag == True and len(rig_all_shape) == 0:
            error_msg = 'There is no rig team shapes info, need to check mdl pub data(hichy)'
            self.add_warnning('', error_msg, "error", '')
            self.warn_count += 1





        # compare three groups
        if self.rig_check_flag == False:
            unmatched_info_mdl_list = self.compare_shapes(mdl_all_shape, cfx_all_shape)
        if self.rig_check_flag == True:
            unmatched_info_rig_list = self.compare_shapes(rig_all_shape, cfx_all_shape)





        if self.rig_check_flag == False and unmatched_info_mdl_list:
            for mesh in unmatched_info_mdl_list:
                unmatch_shape = mesh.split('|')[-1]
                error_msg = "MDL :geo is not latest mesh".format(unmatch_shape)

                self.add_warnning(unmatch_shape, error_msg, "error", unmatch_shape)
                self.warn_count += 1
        else:
            print('Geo check clear!')
            self.clear_items.extend(cfx_all_shape)

        if self.rig_check_flag == True and unmatched_info_rig_list:
            for mesh in unmatched_info_rig_list:
                unmatch_shape = mesh.split('|')[-1]
                error_msg = "RIG :geo is not latest mesh".format(unmatch_shape)

                self.add_warnning(unmatch_shape, error_msg, "error", unmatch_shape)
                self.warn_count += 1
        else:
            print('Geo check clear!')
            self.clear_items.extend(cfx_all_shape)

        self.clear_items = list(set(self.clear_items))

    def is_all_clear(self):
        return self.warn_count == 0


    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        self.add_item(msg, "Clear", "clear")

    def virtual_clear(self):
        self.warn_count = 0
