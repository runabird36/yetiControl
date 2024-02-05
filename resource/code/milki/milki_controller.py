# -*- coding: utf-8 -*-

import os
import re
import subprocess
import traceback
import sys


if sys.version_info.major == 3:
    from importlib import reload
if sys.platform.count("win"):
    pathLs = ['Z:/backstage3X/maya/versionUpManager', "Z:/backstage3X/maya/arnoldRenderAttrSetup"]
    for pth in pathLs:
        if not pth in sys.path:
            sys.path.append(pth)
    


import maya_md.versionUpManager as vm
from maya_md import neon
reload(vm)
import maya.cmds as cmds
from general_md_3x import LUCY
import PySide2.QtCore as QtCore


import item_docker
reload (item_docker)
import item_supply
reload (item_supply)
from item_supply import ItemSupply
import milki_sg_tk
reload (milki_sg_tk)
from milki_sg_tk import MilkiSgTk
import milki_widget
reload (milki_widget)
from milki_widget import MilkiWidget


def tracefunc(frame, event, arg, indent=[0]):
      if event == "call":
          indent[0] += 2
          print("-" * indent[0] + "> call function", frame.f_code.co_filename, frame.f_code.co_name)
      elif event == "return":
          print("<" + "-" * indent[0], "exit function", frame.f_code.co_filename, frame.f_code.co_name)
          indent[0] -= 2
      return tracefunc


def suspend_viewport():
    cmds.refresh(suspend=True)

def refresh_viewport():
    cmds.refresh(suspend=False)

class MilkiController(QtCore.QObject):
    dk = None
    app_name = None
    milki_widget = None
    supply = None
    targets = []
    options = {}
    cnt = 1


    def __init__(self, app_name):
        QtCore.QObject.__init__(self)
        self.app_name = app_name
        self.milki_widget = MilkiWidget(self, app_name)
        self.milki_widget.setup()
        progress_dialog = self.milki_widget.get_progress_dialog()
        try:
            m_sg_tk = MilkiSgTk()
        except:
            traceback.print_exc()
        self.supply = ItemSupply(m_sg_tk, progress_dialog, self.app_name)
        self.dk = item_docker.Docker()
        self.targets = self.get_targets()


    def setting_items(self):
        step = LUCY.get_pipe_step()
        if step is None:
            return
        print(step)
        items = self.supply.get_items(step)
        print(items)
        self.dk.docking_items(items)
        c_item = self.dk.get_current_item()
        titles = self.dk.get_titles()
        item_titles = self.milki_widget.put_titles(titles)
        for title in item_titles:
            title.item_clicked.connect(self.swap_item)
        if c_item.get_title() == "Select Target":
            c_item.set_items(self.targets)
            self.swap_item(0)
            return
        self.milki_widget.swap_center_item(c_item)
        self.milki_widget.change_progress(self.cal_rate())
        self.continue_step()


    def start_view(self):
        self.milki_widget.show()


    def continue_step(self):
        c_item = self.dk.get_current_item()
        c_item_type = c_item.get_type()
        c_item_title = c_item.get_title()
        item_title = self.milki_widget.get_item_title(self.cnt)
        if item_title :
            item_title.toggle(True)
        if c_item_type == 'Checker':
            print('Item Type : Checker')
            current_scene_step = LUCY.get_pipe_step()
            c_item.get_panel().clear_all_items()
            try:
                if (current_scene_step == 'modeling') and (len(self.options["History"]) == 0) and (c_item_title == "Name Check"):
                    c_item.virtual_clear()
                if (current_scene_step == 'modeling') and (len(self.options["History"]) == 0) and (c_item_title == "History Check"):
                    c_item.virtual_clear()
                elif (current_scene_step == 'modeling') and (len(self.options["UVset"]) == 0) and (c_item_title == "UVset Check"):
                    print('Progress in : MDL UVset Check')
                    c_item.virtual_clear()
                elif (current_scene_step == 'modeling') and (len(self.options["Name"]) == 0) and (c_item_title == "Name Check"):
                    c_item.virtual_clear()
                else:
                    c_item.execute(self.targets)
                if c_item_title == "Frame range Check":
                    c_item.virtual_clear()
                if c_item_title == "Rig latest Check":
                    c_item.virtual_clear()
                # The reason of this part :
                #         - Freeze checker is checker and one of select option
                #         - and Freeze checker and then uv checker --> checker and checker
                #         - but before going to history checker and freezer checker step, there are mdl option and name checker
                #         - Thus checker and checker process is not same case of history checker and freeze checker
                if not c_item.is_all_clear():
                    print('888888')
                    return
            except Exception as e:
                traceback.print_exc()
                print(str(e))
                self.milki_widget.show_error_popup_dialog(str(e))
                return
        elif c_item_type == 'Selector':
            if c_item_title == "Select Target":
                infos = c_item.get_select_infos()
                print(infos)
                self.targets = infos['export targets']
                print('========= Before check =========')
                print(self.targets)
                self.targets = list(set(self.targets))
                print('========= After duplicated check =========')
                print(self.targets)
            else:
                if self.options == {}:
                    self.options = c_item.get_select_infos()
                else:
                    self.options.update(c_item.get_select_infos())
        elif c_item_type == 'Exporter':
            try:
                suspend_viewport()
                c_item.set_finish_func(self.complete)
                c_item.execute()
            except Exception as e:
                traceback.print_exc()
                self.milki_widget.show_error_popup_dialog(str(e))
                return
        self.cnt += 1
        next_item = self.dk.get_next_item()
        if next_item is None:
            return
        if item_title :
            item_title.toggle(False)
        self.milki_widget.swap_center_item(next_item)
        next_title = self.milki_widget.get_item_title(self.cnt)
        if next_title :
            next_title.toggle(True)
        self.milki_widget.change_progress(self.cal_rate())
        # this part for mdl part
        if next_item.get_type() == 'Checker':
            print('101010')
            print(c_item.get_title())
            if LUCY.get_pipe_step() == 'modeling':
                if c_item.get_title() == "MDL Option":
                    if len(self.options["History"]) == 0:
                        print('666666')
                        self.swap_item(self.cnt)
                        return
                elif c_item.get_title() == "Transform History Check":
                    if len(self.options["Name"]) == 0:
                        print('555555')
                        self.swap_item(self.cnt)
                        return
                elif c_item.get_title() == "Name Check":
                    if len(self.options["Freeze"]) == 0:
                        print('777777')
                        self.swap_item(self.cnt)
                        return
                elif c_item.get_title() == "Freeze transform Check":
                    if len(self.options["UVset"]) == 0:
                        print('111111')
                        self.swap_item(self.cnt)
                        return
            try:
                print('222222')
                next_item.execute(self.targets)
                if not next_item.is_all_clear():
                     return
                self.continue_step()
            except Exception as e:
                traceback.print_exc()
                print(str(e))
                self.milki_widget.show_error_popup_dialog(str(e))
                return
        elif next_item.get_type() == 'Exporter':
            try:
                next_item.pre_execute(self.targets, self.options)
                return
            except Exception as e:
                traceback.print_exc()
                print(str(e))
                self.milki_widget.show_error_popup_dialog(str(e))
                return
        else:
            return


    def swap_item(self, item_num):
        item_title = self.milki_widget.get_item_title(self.cnt)
        item_title.toggle(False)
        self.cnt = item_num + 1
        next_title = self.milki_widget.get_item_title(self.cnt)
        next_title.toggle(True)
        self.milki_widget.change_progress(self.cal_rate())
        item = self.dk.get_item(item_num)
        print('=======')
        print(item.get_title())
        self.milki_widget.swap_center_item(item)
        if item.get_type() == 'Checker':
            if item.is_all_clear() == True:
                print('856584')
                item.show_all_clear_items()
            elif item.get_title() == 'UVset Check' and len(self.options["UVset"]) == 0:
                print('446846')
                self.continue_step()
            elif item.get_title() == 'History Check' and len(self.options["History"]) == 0:
                print('998889')
                self.continue_step()
            elif item.get_title() == 'Name Check' and len(self.options["Name"]) == 0:
                print('988984')
                self.continue_step()
            elif item.get_title() == 'Freeze Check' and len(self.options["Freeze"]) == 0:
                print('998887')
                self.continue_step()
            else:
                print('555555')
                item.execute(self.targets)
        elif item.get_type() == 'Exporter':
            try:
                item.pre_execute(self.targets, self.options)
                return
            except Exception as e:
                traceback.print_exc()
                print(str(e))
                self.milki_widget.show_error_popup_dialog(str(e))
                return


    def complete(self, pub_path):
        refresh_viewport()
        result=self.milki_widget.show_complete_popup_dialog('complete')
        if result == 'Open pub folder':
            pub_dir = os.path.dirname(pub_path)
            if sys.platform.count("linux"):
                subprocess.Popen(['nautilus', '{0}'.format(pub_dir)])
            else:
                subprocess.Popen('explorer {0}'.format(pub_dir.replace('/', '\\')))
            self.complete(pub_path)
        elif result == 'Version Up':
            vm.versionUp()
            self.complete(pub_path)
        else:
            self.milki_widget.hide()
            self.milki_widget.close()
            return


    def get_targets(self):
        
        entity = LUCY.get_entity()
        targets = []
        selected_roots= []
        for sel in cmds.ls(selection=True, long = True):
            if '|' in sel:
                selected_roots.append(sel.split('|')[-1])
            else:
                selected_roots.append(sel)
        self._IS_SHOT_MDL = False
        if LUCY.get_pipe_step() == 'modeling' and LUCY.get_category() == 'sequence':
            self._IS_SHOT_MDL = True
        self._IS_ASSET_ANI = False
        if LUCY.get_pipe_step() == 'animation' and LUCY.get_category()== 'assets':
            self._IS_ASSET_ANI = True
        if LUCY.get_category()== 'assets':
            self._IS_ASSET_ANI = True
        if (LUCY.get_pipe_step() in ['animation', 'matchmove', 'layout', 'simulation'] or self._IS_SHOT_MDL == True or self._IS_ASSET_ANI == False) and LUCY.get_pipe_step() not in ["lighting"]:
            targets.extend(selected_roots)


        if self._IS_SHOT_MDL == True:
            self.select_all_export_targets(entity, targets)
        # elif LUCY.get_category() == 'sequence' and LUCY.get_pipe_step() in ['simulation']:
        #     self.select_all_sim_cache_targets(entity, targets)
        elif LUCY.get_category() == 'assets' and LUCY.get_pipe_step() in ['lighting']:
            self.select_lgt_targets(entity, targets)
        elif LUCY.get_category()== 'assets':
            self.select_asset(entity, targets)
        elif LUCY.get_category() == 'sequence':
            self.select_all_export_targets(entity, targets)
        targets = list(set(targets))
        targets.sort()
        print(11111111111, targets)
        cmds.select(targets)
        return targets


    def select_asset(self, entity, targets):
        asset_name = entity['assetname_code']
        step = entity['pipestep_code']
        _cur_type = LUCY.get_category()
        
        asset_prefix_step = '{0}_{1}'.format(asset_name, step)
        if step in ["rigging", "cloth"]:
            asset_prefix_step = '{0}_rig'.format(asset_name)
        asset_prefix_GRP = '{0}_{1}'.format(asset_name, 'GRP')
        # just_assetname = asset_name
        # check_target_list = [asset_prefix_GRP, asset_prefix_step, asset_prefix_step_hi]
        check_target_group = [asset_prefix_GRP, asset_prefix_step]
        for check_target in check_target_group:
            print(1)
            print(check_target)
            if step in ['modeling','lookdev', 'characterfx', 'hair'] and check_target == asset_prefix_GRP:
                root_duplicated_list = cmds.ls(asset_prefix_GRP)
                root_assetName_count = len(root_duplicated_list)
                if root_assetName_count != 1:
                    error_msg = ''
                    if root_assetName_count == 0:
                        error_msg = '============\nThere is no assetName_GRP!!!\nCheck please!!\n============'
                    else:
                        error_msg = '============\nThere are more than one assetName_GRP!!!\nMake only one assetName_GRP\n============'
                    # raise Exception(error_msg)
                    cmds.confirmDialog(backgroundColor=[0, 0, 0], title = 'asset pub error!!!', message = error_msg)
                    break
            if step in ["rigging", "cloth"] and check_target == asset_prefix_GRP:
                continue
            if step == 'animation' and _cur_type == 'asset':
                _queried_asset_rig = cmds.ls('*_rig')[0]
                _queired_assetname = _queried_asset_rig.split('_')[0]
                if LUCY.get_assetname() != _queired_assetname:
                    # check_target = '{0}_GRP'.format(_queired_assetname)
                    check_target = '{0}_rig'.format(_queired_assetname)
                pass
                # if check_target == asset_prefix_GRP:
                #     continue
                # elif check_target == asset_prefix_step:
                #     check_target = '{0}_rig|geo|{0}_GRP'.format(asset_name)
            if step == 'lookdev' and check_target == asset_prefix_GRP:
                # is_target_created_by_ref = cmds.referenceQuery(check_target, isNodeReferenced=True)
                is_target_created_by_ref = True
                if is_target_created_by_ref is False:
                    error_msg = '===============================================\n\
                                 The taks was worked with imported Modeling data(assetName_GRP)\n\
                                 you need to work with create by reference\n\
                                 ==============================================='
                    # raise Exception(error_msg)
                    cmds.confirmDialog(backgroundColor=[0, 0, 0], title = 'ldv step error', message = error_msg)
                    break
            try:
                print(check_target)
                top_node_check_tar = check_target
                cmds.select(check_target)
                targets.append(check_target)
                break
            except:
                traceback.print_exc()
                continue
        if self.is_top_node(top_node_check_tar) == False and self._IS_ASSET_ANI == False:
            error_msg = u'outliner 상에, 펍 대상이 최상위가 아닙니다.(parent 존재)\n정리 후 다시 Milki를 실행해주십쇼'
            cmds.confirmDialog(backgroundColor=[0, 0, 0], title = 'asset pub error!!!', message = error_msg)
            for idx in range(len(targets)):
                targets.pop()


    def select_all_export_targets(self, entity, targets):
        full_targets = []
        all_ref_list = neon.get_all_RNs()
        print(all_ref_list)
        for ref in all_ref_list:
            # if scn.get_step() == 'ani' and scn.get_type() == 'Asset':
            #     if ref.find('_mdl')>0:
            #         if ref.endswith('RN'):
            #             regular_ex = re.compile(r'\BRN\b')
            #             ref = regular_ex.sub('', ref)
            if ref.find('_mdl')>0:
                if ref.endswith('RN'):
                    regular_ex = re.compile(r'\BRN\b')
                    ref = regular_ex.sub('', ref)
                    print(ref)
                ref = ref.split(':')
                ref_num = ref[0]
                asset_name = ref_num.split('_')
                asset_name = asset_name[0]
                # make assetName_GRP name
                target_GRP = '{0}:{1}_GRP'.format(ref_num, asset_name)
                target_mdl_hi = '{0}:{1}_mdl_hi'.format(ref_num, asset_name)
                full_targets.append(target_GRP)
        check_duplicated_roots=set(full_targets)
        full_targets = list(check_duplicated_roots)
        pop_list = []
        for tar in targets:
            # print(tar)
            if '_groupAsset' in tar:
                print('enter')
                target_rigs_list = cmds.listRelatives(tar, c=True)
                for rig in target_rigs_list:
                    rig_geo = '{0}|*:geo'.format(rig)
                    rig_geo_child = cmds.listRelatives(rig_geo, c=True)
                    pop_list.append(rig_geo_child[0])
        # print('before')
        # print(targets)
        # Get cam
        # if scn.get_project() == '2019_06_apollo':
        # get all camera list except 'perspective cam'
        cam_target_list = cmds.listCameras(p=True)
        cam_target_list.remove('persp')
        # if there is 'cam_GRP', rename it to 'cam_grp'
        # _group_check_tar_list = ['cam_GRP']
        # for _tar in cam_target_list:
        #     if cmds.objExists(_tar) == True:
        #         cmds.rename(_tar, 'cam_grp')
        
        
        if LUCY.is_sequence() == True and LUCY.get_pipe_step() not in ['shotsculpt']:
            
            cur_shotnum = LUCY.get_shot()
            search_tar = "{0}_*_cam".format(cur_shotnum)
            search_res = cmds.ls(search_tar, dag=True, ni=True, type='camera')
            if search_res:
                search_res = cmds.listRelatives(search_res, p=True)
                targets.extend(search_res)
                # for _res in search_res:
                #     cam_long_name = cmds.ls(_res, l=True)[0]

                #     cam_grp_name = LUCY.get_shot() + "_cam_grp"
                #     if cam_grp_name in cam_long_name:
                #         targets.append(cam_grp_name)


        
        print(targets)
        
        # Rig loc check
        if LUCY.is_sequence() == True and LUCY.get_pipe_step() in ["animation", "layout", "previz"]:
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
            full_targets.extend(plus_loc_list)
            full_targets = list(set(full_targets))
            for target in full_targets:
                if target in pop_list:
                    continue
                try:
                    cmds.select(target, add = True)
                    targets.append(target)
                except Exception as e:
                    traceback.print_exc()
                    print(e)
        
        print(targets)
        
        # Last check
        rig_list = cmds.ls('*_*:*_rig|*_*:geo')
        plus_list = []
        print(rig_list)
        for _rig in rig_list:
            try:
                asset_GRP = cmds.listRelatives(_rig,c=True)[0]
                plus_list.append(asset_GRP)
            except:
                continue
        full_targets.extend(plus_list)
        full_targets = list(set(full_targets))
        for target in full_targets:
            if target in pop_list:
                continue
            try:
                cmds.select(target, add = True)
                targets.append(target)
            except Exception as e:
                traceback.print_exc()
                print(e)

        print(targets)
    def select_all_sim_cache_targets(self, entity, targets):
        all_yetishape_list = cmds.ls(ni=True, l=True, typ='pgYetiMaya')
        pub_tar_yeti_list = []
        for _cur_yeti in all_yetishape_list:
            for _word_component in _cur_yeti.split('|'):
                if _word_component.endswith('_yetiGRP') and '|yeti|' in _cur_yeti:
                    pub_tar_yeti_list.append(_cur_yeti)
                    break
        targets.extend(pub_tar_yeti_list)

    def select_lgt_targets(self, entity :dict, targets :list):
        asset_name   = entity['assetname_code']
        assembly_tar = cmds.ls(f"{asset_name}_assemblyGRP", ni=True, l=True, type="transform")
        light_tar    = cmds.ls(f"{asset_name}_lgtGRP", ni=True, l=True, type="transform")
        light_tar_02 = cmds.ls(f"{asset_name}_lgt_GRP", ni=True, l=True, type="transform")
        
        targets.extend(assembly_tar)
        targets.extend(light_tar)
        targets.extend(light_tar_02)

    def is_top_node(self, tar_name):
        try:
            check_res = cmds.listRelatives(tar_name, p=True)
        except:
            return False
        print(check_res)
        # if not top node, cmds.listRelatives return list which has one more than elements
        if check_res == None:
            return True
        else:
            return False


    def cal_rate(self):
        len_of_items = self.dk.get_len_of_items()
        return (float(self.cnt) / float(len_of_items)) * 100
