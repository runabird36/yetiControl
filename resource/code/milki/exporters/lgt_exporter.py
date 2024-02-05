import exporter
# reload (exporter)
from exporter import Exporter

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui

import mtoa.ui.arnoldmenu

import cacheSubmit
# reload (cacheSubmit)

import maya.mel as mel
import maya.cmds as cmds
import time
# reload (wm_stamp)


from maya_md import neon
from general_md_3x import LUCY


from maya_md import wm_stamp



import pprint, re, os, math, subprocess, shutil, time
import maya.mel as mel

import ui_progressbar
# reload(ui_progressbar)

class AbcItem():
    def __init__(self):
        self.abc_export_target_path_dict ={}
        self.project = LUCY.get_project()
    def pre_do_item(self, m_sg_tk, targets, path_list):
        current_scene_ver = LUCY.get_dev_vernum()
        asset_num = 0
        # add anim version attribute
        for tar in targets:
            if '_groupAsset' in tar:
                self.set_abc_version_attr(tar, current_scene_ver, asset_num)
                target_rigs_list = cmds.listRelatives(tar, c=True)
                for rig in target_rigs_list:
                    rig_geo = '{0}|*:geo'.format(rig)
                    rig_geo_child = cmds.listRelatives(rig_geo, c=True)
                    target = rig_geo_child[0]

                    asset_num = target.split(':')[0]
                    self.set_abc_version_attr(target, current_scene_ver, asset_num)
            else:
                target = tar
                asset_num = target.split(':')[0]
                # asset_num = name_space.split('_')[1]

                self.set_abc_version_attr(target, current_scene_ver, asset_num)
        print('check targetLisk')
        # pprint.pprint(targets)
        for target in targets:

            abc_pub_path = path_list[0]
            abc_version_pub_path = path_list[1]

            if '_groupAsset' in target:
                file_attr = target
            elif 'cam_grp' in target:
                # change pub path only in cam pub case
                cur_step = LUCY.get_pipe_step()
                search_target = '/{0}/pub/abc/'.format(cur_step)
                change_to_name = '/cam/alembic/'
                if abc_pub_path.find(search_target) >0:
                    abc_pub_path = abc_pub_path.replace(search_target, change_to_name)
                if abc_version_pub_path.find(search_target) >0:
                    abc_version_pub_path = abc_version_pub_path.replace(search_target, change_to_name)
                dir_path_versions_abc=os.path.dirname(abc_version_pub_path)
                if not os.path.exists(dir_path_versions_abc) :
                    os.mkdir(dir_path_versions_abc)
                # set file name with cam
                file_attr = 'cam'
            else:
                asset_num = target.split(':')
                file_attr = asset_num[0]

            abc_regular_ex = re.compile('\.abc')
            file_postfix = '_{0}.abc'.format(file_attr)
            abc_pub_path_with_num = abc_regular_ex.sub(file_postfix, abc_pub_path)
            abc_version_pub_path_with_num = abc_regular_ex.sub(file_postfix, abc_version_pub_path)
            path = [abc_pub_path_with_num, abc_version_pub_path_with_num]
            self.abc_export_target_path_dict[target] = path
        return self.abc_export_target_path_dict

    def do_item(self, targets, options, task, user, path_list=None, additional_info=None, is_maya=False):
        '''
        parameter :
            export_target : [['SWT_0040_mmv_cam','cam'], ['hair_mesh_v03','mesh'], ['vampLordAwakenNew_001','mesh']]
        '''

        # setting progressbar
        backup_progressbar_window = ui_progressbar.Ui_ProgressbarUI()
        progress_title = 'Set Info & Baking Alembic......'
        backup_progressbar_window.progress_window.setWindowTitle(progress_title)
        backup_progressbar_window.blackhole_pb.setValue(0)


        cmds.select(targets)

        # alembic export target
        abc_ex_target_list = targets


        # start, end frame
        start_frame = neon.get_start_time()
        end_frame = neon.get_end_time()

        # options
        option_flag_dict = {'World space':'-worldSpace',
                            'Write Visibility':'-writeVisibility',
                            'Filter Euler Rotations':'-eulerFilter',
                            'Strip Namespaces':'-stripNamespaces',
                            'UV write':'-uvWrite'}

        option_list = options['Abc Export Options']
        option_flags_str = "-attr geo_tag"

        # anim version attribute option
        whole_user_defined_attr_list = cmds.listAttr(ud=True)
        if whole_user_defined_attr_list == None:
            pass
        elif 'Alembic_version' in whole_user_defined_attr_list:
            option_flags_str += " -attr Alembic_version"

        if whole_user_defined_attr_list == None:
            pass
        elif 'Asset_number' in whole_user_defined_attr_list:
            option_flags_str += " -attr Asset_number"

        for option in option_list:
            option_flags_str += " {0}".format(option_flag_dict[option])




        # pub path
        # and make folder if the folders don't exist
        abc_pub_path = path_list[0]
        dir_path_abc=os.path.dirname(abc_pub_path)
        if not os.path.exists(dir_path_abc) :
            os.mkdir(dir_path_abc)

        abc_version_pub_path = path_list[1]
        dir_path_versions_abc=os.path.dirname(abc_version_pub_path)
        if not os.path.exists(dir_path_versions_abc) :
            os.mkdir(dir_path_versions_abc)

        # step info
        step_info = options['Step'][-1]
        self.copySceneName = ''





        exportType = None
        try:
            exportType=options['Deadline Submit'][0]
        except:
            exportType = 'maya_abc'


        ma_path = path_list[2][0]
        dir_path_ma=os.path.dirname(ma_path)
        if not os.path.exists(dir_path_ma) :
            os.mkdir(dir_path_ma)

        ma_path_ver = path_list[2][1]
        dir_path_ma_ver=os.path.dirname(ma_path_ver)
        if not os.path.exists(dir_path_ma_ver) :
            os.mkdir(dir_path_ma_ver)

        path_to_sg = []
        if is_maya == True:
            # ma_path_abcver= ma_path.replace('.ma', '_abcVer.ma')
            # cmds.file(ma_path_abcver, type="mayaAscii",force = True, exportSelected=True,preserveReferences=True,shader=True, expressions=True)
            # cmds.file(ma_path_ver, type="mayaAscii",force = True, exportSelected=True,preserveReferences=True,shader=True, expressions=True)
            # path_to_sg.append(ma_path_abcver)
            pass


        if exportType == 'submit':

            mel_path = path_list[3]
            thumb = additional_info[0]
            desc = additional_info[1]

            dir_path_mel=os.path.dirname(mel_path)
            if not os.path.exists(dir_path_mel) :
                os.mkdir(dir_path_mel)





        cache_submit_cmd_info_dict = {}


        item_total_count = len(abc_ex_target_list)
        _count = 1
        before_percentage = 1


        for target in abc_ex_target_list:
            # update progressbar
            percentage = float(_count)/float(item_total_count)*100
            for i in range(int(before_percentage), int(percentage)+1):

                backup_progressbar_window.blackhole_pb.setValue(int(i))
                QtGui.QApplication.processEvents()
                time.sleep(0.03)
            before_percentage = percentage
            _count += 1

            bake_root = ''
            if '_groupAsset' in target:
                grp_target_rigs_list = cmds.listRelatives(target, c=True)
                for tar_rig in grp_target_rigs_list:
                    rig_geo = '{0}|*:geo'.format(tar_rig)
                    rig_geo_child = cmds.listRelatives(rig_geo, c=True)
                    bake_root += ' -root {0}'.format(rig_geo_child[0])
                option_flags_str = option_flags_str.replace(' -stripNamespaces', '')
            else:
                bake_root = ' -root {0}'.format(target)

            path_grp = self.abc_export_target_path_dict[target]

            if exportType == 'submit':
                # deadline bake range 1 : only pub path
                # deadline bake range 2 : pub path + pub version path
                for idx in range(1):
                    command_abc = "{0} -frameRange {1} {2} -s {3} {4} -file {5}".format(bake_root, start_frame, end_frame, step_info, option_flags_str, path_grp[idx])

                    cache_submit_cmd_info_dict[path_grp[idx]] = command_abc
                path_to_sg.append(path_grp[0])
            elif exportType == 'maya_abc':
                command_abc = "{0} -frameRange {1} {2} -s {3} {4} -file {5}".format(bake_root, start_frame, end_frame, step_info, option_flags_str, path_grp[0])

                cmds.AbcExport ( j = command_abc )
                shutil.copy2(path_grp[0], path_grp[1])
                path_to_sg.append(path_grp[0])

            if ' -stripNamespaces' not in option_flags_str:
                option_flags_str += ' -stripNamespaces'



        if exportType == 'submit':
            cacheSubmit.submit_to_farm(cache_submit_cmd_info_dict, mel_path, ma_path, task, user, thumb, desc)


        # return export path and export type list
        export_info = [path_to_sg , exportType]
        return export_info



    def set_abc_version_attr(self, target, cur_ver, asset_num):
        '''add anim dev version attribute in all transform'''

        all_transform = cmds.ls(target, dagObjects = True, sn = True, tr=True)

        for tr in all_transform:
            user_defined_attr_list=cmds.listAttr(tr, ud=True)
            if user_defined_attr_list == None or 'Alembic_version' not in user_defined_attr_list:
                cmds.addAttr(tr, longName='Alembic_version', dataType="string", readable=True)
            if user_defined_attr_list == None or 'Asset_number' not in user_defined_attr_list:
                cmds.addAttr(tr, longName='Asset_number', dataType="string", readable=True)
            cmds.setAttr('{0}.Alembic_version'.format(tr), cur_ver, type='string')
            cmds.setAttr('{0}.Asset_number'.format(tr), asset_num, type='string')


class AssItem():
    playblast_w = ''
    playblast_h = ''
    def __init__(self):
        self.ass_path_dict = {}
        mov_path = None
        wm_mov_path = None
        title_info_dic = {}

        self.re_ai_shape = re.compile(r'Shape$')
    def update_progress(self, total_count, count, b_percentage):
        # update progressbar
        before_percentage = b_percentage
        item_total_count = total_count
        _count = count
        percentage = float(_count)/float(item_total_count)*100
        for i in range(int(before_percentage), int(percentage)+1):

            self.backup_progressbar_window.blackhole_pb.setValue(int(i))
            QtGui.QApplication.processEvents()
            time.sleep(0.03)
        before_percentage = percentage
        _count += 1



        return [_count, before_percentage]

    def make_file_name(self, obj_name):
        name_component_list = obj_name.split(':')
        namespace_comp = name_component_list[0]
        assetGRP_comp = name_component_list[1]

        asset_num = namespace_comp.split('_')[1]

        return '{0}_v{1}'.format(assetGRP_comp, asset_num)

    def restore_asset_name(self, tar):
        file_name_component = tar.split('_')
        asset_name = file_name_component[0]
        grp_str = file_name_component[1]
        asset_num = file_name_component[2]
        return '{0}_{1}:{0}_GRP'.format(asset_name, asset_num)

    def get_masks(self, options):
        '''
            AI_NODE_UNDEFINED = 0x0000
            AI_NODE_OPTIONS = 0x0001
            AI_NODE_CAMERA = 0x0002
            AI_NODE_LIGHT = 0x0004
            AI_NODE_SHAPE = 0x0008
            AI_NODE_SHADER = 0x0010
            AI_NODE_OVERRIDE = 0x0020
            AI_NODE_DRIVER = 0x0040
            AI_NODE_FILTER = 0x0080
            AI_NODE_ALL = 0xFFFF
        '''
        '''
            option consists of a bit operation
            The number of digits in each bit indicates the option

            Args:
                options (list) : get ass export options

            return:
                int : get options data
        '''

        optionDict = {'option' : 0x0001
                      , 'camera' : 0x0002
                      , 'light' : 0x0004
                      , 'shape' : 0x0008
                      , 'shader' : 0x0010
                      , 'override' : 0x0020
                      , 'driver' : 0x0040
                      , 'filter' : 0x0080
                      }

        mask = 0
        for option in options:
            try:
                mask += optionDict[option]

            except:
                pass
        return mask


    def pre_do_item(self, m_sg_tk, targets, path_list):
        '''
        - make pub paht of each target
        '''
        self.m_sg_tk = m_sg_tk

        ass_pub_path = path_list[0]
        ass_pub_dir_path = os.path.dirname(ass_pub_path)


        # get export path from path_list
        # make folder tree if not exist
        for target in targets:
            shape_name = target
            if ':' in target:
                shape_name = self.make_file_name(target)
            sub_path = '/ass/{0}/pub_{0}.ass'.format(shape_name)
            ass_pub_full_path = ass_pub_dir_path.replace('/ass', sub_path)

            check_dir_path = os.path.dirname(ass_pub_full_path)
            if not os.path.exists(check_dir_path):
                os.makedirs(check_dir_path)

            self.ass_path_dict[target] = [ass_pub_full_path, shape_name]

        return self.ass_path_dict


    def do_item(self, targets, options, task, user, path_list =None, additional_info=None, is_maya=False):
        cmds.select(targets, deselect=True)

        # print 'targets : {0}'.format(targets)
        # pprint.pprint(options)
        # print 'task : {0}'.format(task)
        # print 'user : {0}'.format(user)
        # print 'path_list : {0}'.format(path_list)
        # print 'additional_info : {0}'.format(additional_info)

        # get mask info from optinos
        mask_info = self.get_masks(options['Ass Export Options'])
        options_str = '-shadowLinks 1;-mask {0};-lightLinks 1;-boundingBox'.format(str(mask_info))

        # if 'sequence' is checked, get frame info from options
        sequence_flag = False
        if options['Sequence']:
            sequence_flag = True
            s_frame = float(options['Start Frame'][0])
            e_frame = float(options['End Frame'][0])
            options_str = '{0};-startFrame {1};-endFrame {2};-frameStep 1.0'.format(options_str, str(s_frame), str(e_frame))
        

        # make mel cmd
        options_str_with_blank = options_str.replace(';', ' ')
        options_str = '\"{0}\"'.format(options_str)

        # setting progressbar
        self.backup_progressbar_window = ui_progressbar.Ui_ProgressbarUI()
        progress_title = 'Baking Ass......'
        self.backup_progressbar_window.progress_window.setWindowTitle(progress_title)
        self.backup_progressbar_window.blackhole_pb.setValue(0)

        item_total_count = len(self.ass_path_dict.keys())*2
        _count = 1
        before_percentage = 1

        path_to_sg = []
        # bake ass! create standardIn! and! load pub data!
        # grouping
        refresh_attr_list = []
        for tar_grp, tar_pub_info in self.ass_path_dict.items():
            #update progress bar
            _progress_info = self.update_progress( item_total_count, _count, before_percentage)
            _count = _progress_info[0]
            before_percentage = _progress_info[1]

            tar_pub_path = tar_pub_info[0]
            shape_name = tar_pub_info[1]
            tar_pub_path_with_quote = '\"{0}\"'.format(tar_pub_path)
            path_to_sg.append(tar_pub_path)
            mel_cmd = "file -force -options {0} -typ \"ASS Export\" -pr -es {1};arnoldExportAss -s -f {1} {2}".format(options_str,\
                                                                                                                    tar_pub_path_with_quote,\
                                                                                                                    options_str_with_blank)
            # bake ass file
            cmds.select(tar_grp, r=True)
            if sequence_flag == True:
                # cmds.file(tar_pub_path, f=True, options=options_str, type="ASS Export", pr=True, es=True)
                # outAss = cmds.arnoldExportAss( filename = tar_pub_path, mask = mask_info, lightLinks = 1, shadowLinks = 1, startFrame = s_frame, endFrame = e_frame, frameStep = 1 )[0]
                mel.eval(mel_cmd)
            elif sequence_flag == False:
                # cmds.file(tar_pub_path, f=True, options=options_str, type="ASS Export", pr=True, es=True)
                # outAss = cmds.arnoldExportAss( filename = tar_pub_path, mask = mask_info, lightLinks = 1, shadowLinks = 1, frameStep = 1 )[0]
                mel.eval(mel_cmd)
            cmds.select(tar_grp, deselect=True)

            #update progress bar
            _progress_info = self.update_progress( item_total_count, _count, before_percentage)
            _count = _progress_info[0]
            before_percentage = _progress_info[1]
            time.sleep(0.5)


            # create aiStandarIn and rename it
            ass_rename_tar = '{0}_ass'.format(shape_name)
            if cmds.objExists(ass_rename_tar) == False:
                created_tar = mtoa.ui.arnoldmenu.createStandIn()
                try:
                    if self.re_ai_shape.search(created_tar):
                        replaced_name = self.re_ai_shape.sub('', created_tar)
                    cmds.rename(replaced_name, ass_rename_tar)
                except:
                    created_tar = str(created_tar)
                    if self.re_ai_shape.search(created_tar):
                        replaced_name = self.re_ai_shape.sub('', created_tar)
                    cmds.rename(replaced_name, ass_rename_tar)

            # Load data
            # and if the data need to be sequence, set sequence attr True
            ass_path_attr = '{0}.dso'.format(ass_rename_tar)
            cmds.setAttr(ass_path_attr, tar_pub_path, type='string')
            refresh_attr_list.append(ass_path_attr)

            ass_sequence_attr = '{0}.useFrameExtension'.format(ass_rename_tar)
            if sequence_flag == True:
                cmds.setAttr(ass_sequence_attr, True)
            elif sequence_flag == False:
                cmds.setAttr(ass_sequence_attr, False)




            vis_attr = '{0}.visibility'.format(tar_grp)
            cmds.setAttr(vis_attr, False)

        cmds.select(deselect=True)
        cmds.select(refresh_attr_list, r=True)

        self.backup_progressbar_window.progress_window.accept()

        ma_path = path_list[2][0]
        dir_path_ma=os.path.dirname(ma_path)
        if not os.path.exists(dir_path_ma) :
            os.mkdir(dir_path_ma)

        ma_path_ver = path_list[2][1]
        dir_path_ma_ver=os.path.dirname(ma_path_ver)
        if not os.path.exists(dir_path_ma_ver) :
            os.mkdir(dir_path_ma_ver)

        if is_maya == True:
            ma_path_abcver= ma_path.replace('.mb', '_assVer.mb')
            cmds.file(ma_path_abcver, type="mayaBinary",force = True, exportSelected=True,preserveReferences=True,shader=True, expressions=True)
            cmds.file(ma_path_ver, type="mayaBinary",force = True, exportSelected=True,preserveReferences=True,shader=True, expressions=True)
            path_to_sg.append(ma_path_abcver)

        return path_to_sg


class LgtExporter(Exporter):
    def __init__(self, m_sg_tk, p_dialog):
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog
        self.options = None
        self.targets = None
        self.export_order_dict = {'ass' : AssItem(), 'alembic cache': AbcItem()}
        print('Exporter created')


    def pre_execute(self, targets, options):
        # get targets and options from milki_controller
        # if want to change or check target

        self.targets = targets

        self.options = options
        self._set_basic_info()
        pprint.pprint(targets)
        pprint.pprint(options)


        # get export order in list
        ex_order = self.options['Export Order']
        # pre_execute function purpose : to make export list by pre_do_item function
        # pre_do_item function is declared in AbcItem class and PlayblastItem class
        # pre_do_item fucntion resturn all path of all roots which are in outliner
        # self.get_pub_paths function is declared in exporter class(parent)
        for item in ex_order:
            if item == 'alembic cache':
                path_list = self.get_pub_paths('abc')
                self.abc_pub_path = path_list[0]
            elif item == 'ass':
                path_list = self.get_pub_paths('ass')
            elif item == 'maya':
                ma_path_list = self.get_pub_paths('mb')
                self.add_pub_files(ma_path_list)
                continue

            export_item = self.export_order_dict[item]
            all_path=export_item.pre_do_item(self.m_sg_tk,self.targets, path_list)
            
            pprint.pprint(all_path)
            for path in all_path:
                if item == 'ass':
                    print(all_path[path])
                    full_path = all_path[path][0]
                    if '.' in full_path and '/' in full_path:
                        self.add_pub_files([full_path])
                elif item == 'maya':
                    continue
                else:
                    self.add_pub_files(all_path[path])


    def execute(self):
        _is_maya = False

        thumb = self.panel.get_thumb()
        desc = self.panel.get_desc()
        additional_info = [thumb, desc]
        self.check_pub_condition()
        cmds.select(self.targets)

        # execute function purpose : to do playblast and do alembic export
        ex_order = self.options['Export Order']
        if 'maya' in ex_order:
            _is_maya = True
        for item in ex_order:
            if item == 'alembic cache':
                path_list = self.get_pub_paths('abc')
                ma_path_list = self.get_pub_paths('mb')
                ma_path = ma_path_list
                path_list.append(ma_path)
                mel_path_list = self.get_pub_paths('mel')
                mel_path = mel_path_list[0]
                path_list.append(mel_path)
            elif item == 'ass':
                path_list = self.get_pub_paths('ass')
                ma_path_list = self.get_pub_paths('mb')
                path_list.append(ma_path_list)
            elif item == 'maya':
                continue
            export_item = self.export_order_dict[item]
            user = self.m_sg_tk.get_user()
            export_info = export_item.do_item(self.targets, self.options, self.tar_task, user, path_list, additional_info, _is_maya)

            # alarm shotgun : only maya alembic cache bake case
            cur_scene_ver = LUCY.get_dev_vernum()
            if item == 'ass':
                self.pub_to_sg(export_info, cur_dev_ver=cur_scene_ver)
                continue

            elif item == 'alembic cache':
                path_to_sg = export_info[0]
                export_type = export_info[1]
                if export_type == 'maya_abc':
                    self.pub_to_sg(path_to_sg, cur_dev_ver=cur_scene_ver)
                elif export_type == 'submit':
                    self.pub_to_sg(path_to_sg, cur_dev_ver=cur_scene_ver)
                    continue



        self.finish(path_list[0])
