from importlib import reload
import exporter
reload (exporter)
from exporter import Exporter
from importlib import reload
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui


import cacheSubmit
reload (cacheSubmit)


import maya.cmds as cmds
import time


from maya_md import neon
from general_md_3x import LUCY


from maya_md import wm_stamp


# reload (wm_stamp)
import pprint, re, os, math, subprocess, shutil, time, socket
import maya.mel as mel

import ui_progressbar
# reload(ui_progressbar)

def set_infinity() -> None:
    default_offset_num = 10
    cmds.selectKey()
    minT = cmds.playbackOptions(q=True, min=True)
    maxT = cmds.playbackOptions(q=True, max=True)
    if not default_offset_num or not isinstance(default_offset_num, int):
        return
    getN = default_offset_num
    sel = cmds.ls(sl=True)
    for i in sel:
        for j in cmds.listAttr(str(i), k=True):
            hd = cmds.keyframe(str(i), q=True, at=str(j))
            if hd == None:
                return
            cmds.setKeyframe(str(i), at=str(j), t=(minT, maxT), i=True)
            if not minT - 1 in cmds.keyframe(str(i), q=True, at=str(j)):
                subA = cmds.getAttr(str(i) + "." + str(j), t=minT) - cmds.getAttr(str(i) + "." + str(j),t=minT + 1)
                cmds.setKeyframe(str(i), at=str(j), t=minT - getN, v=cmds.getAttr(str(i) + "." + str(j), t=minT) + getN * subA)
                cmds.keyTangent(str(i), at=str(j), t=(minT - getN, minT - getN), itt="linear", ott="linear")
            if not maxT + 1 in cmds.keyframe(str(i), q=True, at=str(j)):
                subB = cmds.getAttr(str(i) + "." + str(j), t=maxT) - cmds.getAttr(str(i) + "." + str(j),t=maxT - 1)
                cmds.setKeyframe(str(i), at=str(j), t=maxT + getN, v=cmds.getAttr(str(i) + "." + str(j), t=maxT) + getN * subB)
                cmds.keyTangent(str(i), at=str(j), t=(maxT + getN, maxT + getN), itt="linear", ott="linear")


def get_cam_grp_name() -> str:
    return LUCY.get_shot() + "_cam_grp"
def get_cam_shape_name() -> str:
    cam_grp_name = get_cam_grp_name()
    if cmds.objExists(cam_grp_name) == False:
        return ""
    search_res = cmds.ls(cam_grp_name, l=True, ni=True, dag=True, type="camera")
    if search_res == []:
        return ""
    return search_res[0]


def set_cam_attr() -> None:
    attr_dict = {
                    "nearClipPlane" : 0.1,
                    "farClipPlane"  : 10000000
                }

    cam_shape_name = get_cam_shape_name()
    if cam_shape_name == "":
        return
    for _attr_name, _attr_value in attr_dict.items():
        try:
            full_attrname = cam_shape_name + "." + _attr_name
            # print(1, full_attrname)
            # print(2, _attr_value)
            if isinstance(_attr_value, str) == True:
                cmds.setAttr(full_attrname, _attr_value, type="string")
            else:
                # print(333333333333)
                cmds.setAttr(full_attrname, _attr_value)
        except Exception as e:
            print(str(e))
            return
        


class AbcItem():
    def __init__(self, _parent=None):
        self._parent = _parent
        self.abc_export_target_path_dict ={}
        self.project = LUCY.get_project()
    def pre_do_item(self, m_sg_tk, targets, path_list):

        def get_only_vernum_folder(check_path: str) -> list:
            vernum_folder_list = []
            for foldername in os.listdir(check_path):
                if re.search(r"v\d+", foldername):
                    vernum_folder_list.append(foldername)
            return vernum_folder_list
        

        def get_next_ver(check_path, postfix=""): 
            if os.path.exists(check_path) is False:
                return "v001"
            # ver_list = os.listdir(check_path)
            ver_list = get_only_vernum_folder(check_path)
            ver_list.sort()
            # ver_list.sort(reverse=True)
            if ver_list == []:
                return "v001"
            last_ver = ver_list[-1]
            only_num = int(last_ver.replace("v", ""))
            only_num += 1
            next_lat_ver = "v" + str(only_num).zfill(3)
            return next_lat_ver
            


        cam_grp_name = get_cam_grp_name()
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
        
        for target in targets:

            abc_pub_path = path_list[0]

            if '_groupAsset' in target:
                file_attr = target
            elif cam_grp_name in target:
                # change pub path only in cam pub case
                cur_step = LUCY.get_pipe_step()
                cur_taskname = LUCY.get_task()
                cur_dev_vernum = LUCY.get_dev_vernum()
                search_target = '/{0}/{1}/pub/abc/'.format(cur_step, cur_taskname)
                change_to_name = '/camera/pub/abc/'.format(cur_dev_vernum)
                

                # if abc_pub_path.find(search_target) >0:
                # abc_pub_path = abc_pub_path.replace(search_target, change_to_name)
                abc_cam_pub_path = abc_pub_path.split(search_target)[0] + change_to_name
                # set file name with cam
                next_vernum = get_next_ver(abc_cam_pub_path)
                

                entity_dict = LUCY.get_entity()

                
                cam_basename = LUCY.get_abccam_pubfilename(_elements=entity_dict)
                # print(3333333333333, pub_dirpath)
                # print(cam_basename)
                abc_pub_path = abc_cam_pub_path + next_vernum + '/' + cam_basename
                
                file_attr = ''

                # self.set_cam_default_attr(target)
            else:
                asset_num = target.split(':')
                file_attr = asset_num[0]

            if file_attr != '':
                abc_regular_ex = re.compile('\.abc')
                file_postfix = '_{0}.abc'.format(file_attr)
                # print(33333333333, file_postfix_for_search)
                # abc_pub_path_with_num = abc_regular_ex.sub(file_postfix, abc_pub_path)
                abc_pub_path_with_num = self._parent.get_pub_paths('abc', file_attr)
            else:
                abc_pub_path_with_num = abc_pub_path
            
            self.abc_export_target_path_dict[target] = [abc_pub_path_with_num]
        return self.abc_export_target_path_dict

    def do_item(self, targets, options, task, user, path_list=None, additional_info=None):
        '''
        parameter :
            export_target : [['SWT_0040_mmv_cam','cam'], ['hair_mesh_v03','mesh'], ['vampLordAwakenNew_001','mesh']]
        '''

        # setting progressbar
        backup_progressbar_window = ui_progressbar.Ui_ProgressbarUI()
        progress_title = 'Set Info & Baking Alembic......'
        backup_progressbar_window.progress_window.setWindowTitle(progress_title)
        backup_progressbar_window.blackhole_pb.setValue(0)
        
        pprint.pprint(options)
        try:
            cmds.select(targets)
        except Exception as e:
            print(str(e))

        # alembic export target
        abc_ex_target_list = targets


        # start, end frame
        # start_frame = neon.get_start_time()
        # end_frame = neon.get_end_time()
        try:
            start_frame = options['Start Frame'][0]
            end_frame = options['End Frame'][0]
            
            if ("Bake with Handle" in options):
                handle_frame = options['Handle'][0]
                if options['Bake with Handle'] != []:
                    start_frame = str(float(start_frame) - float(handle_frame))
                    end_frame = str(float(end_frame) + float(handle_frame))
                else:
                    pass
        except Exception as e:
            print('Shot MDL case')
            start_frame = neon.get_start_time()
            end_frame = start_frame

        # options
        option_flag_dict = {'World space':'-worldSpace',
                            'Write Visibility':'-writeVisibility',
                            'Filter Euler Rotations':'-eulerFilter',
                            'Strip Namespaces':'-stripNamespaces',
                            'UV write':'-uvWrite'}

        option_list = options['Export Options']
        option_flags_str = "-attr geo_tag"
        cam_option_flags = ['nearClipPlane', 'farClipPlane', 'filmFit']
        shape_arnold_attr_target_list = ['aiOpaque',
                                    'aiMatte',
                                    'aiSubdivType',
                                    'aiSubdivIterations',
                                    'aiDispHeight',
                                    'aiDispPadding',
                                    'aiDispZeroValue',
                                    'aiDispAutobump']
        etc_attr_list = ['shakeEnabled', 'shake', 'notes', 'focalLength']
        cam_grp_name = LUCY.get_shot() + "_cam_grp"
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

        for _arnold_attr in shape_arnold_attr_target_list:
            option_flags_str += " -attr {0}".format(_arnold_attr)

        for _etc_attr in etc_attr_list:
            option_flags_str += " -attr {0}".format(_etc_attr)

        for option in option_list:
            option_flags_str += " {0}".format(option_flag_dict[option])




        # pub path
        # and make folder if the folders don't exist
        abc_pub_path = path_list[0]
        dir_path_abc=os.path.dirname(abc_pub_path)
        if not os.path.exists(dir_path_abc) :
            os.makedirs(dir_path_abc)

        # step info
        step_info = options['Step'][-1]
        self.copySceneName = ''





        exportType = None
        try:
            exportType=options['Deadline Submit'][0]
        except:
            exportType = 'maya_abc'

        



        if exportType == 'submit':
            mel_path = path_list[2]
            thumb = additional_info[0]
            desc = additional_info[1]

            dir_path_mel=os.path.dirname(mel_path)
            if not os.path.exists(dir_path_mel) :
                os.makedirs(dir_path_mel)



        path_to_sg = []
        # update date : 2019-10-10
        # contents :
        # - this is for 2019_05_taiyo project
        # - assembly large size assets in the layout scene
        # - Bring lyt maya scene data to another sequence step by reference
        # if scn.get_entity()['step'] == 'lyt':
        #     path_to_sg.append(ma_path)


        cache_submit_cmd_info_dict = {}


        item_total_count = len(abc_ex_target_list)
        _count = 1
        before_percentage = 1

        # pprint.pprint(self.abc_export_target_path_dict)
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
                target = self.check_multiple_target(target)
                bake_root = ' -root {0}'.format(target)


            if cmds.ls(target, dag=True, ni=True, type='camera'):
                cam_append_attr_str = ''
                for _attr_name in cam_option_flags:
                    cam_append_attr_str += ' -attr {0}'.format(_attr_name)
                option_flags_str += cam_append_attr_str

            tar_key = target
            if '|' in target:
                ''' long name case '''
                tar_key = target.split('|')[-1]
            _path = self.abc_export_target_path_dict[tar_key][0]

            _path_dir = os.path.dirname(_path)
            if not os.path.exists(_path_dir):
                os.makedirs(_path_dir)

            if exportType == 'submit':
                # deadline bake range 1 : only pub path
                # deadline bake range 2 : pub path + pub version path
                
                command_abc = "{0} -frameRange {1} {2} -s {3} {4} -file {5}".format(bake_root, start_frame, end_frame, step_info, option_flags_str, _path)

                cache_submit_cmd_info_dict[_path] = command_abc
                path_to_sg.append(_path)
            elif exportType == 'maya_abc':
                command_abc = "{0} -frameRange {1} {2} -s {3} {4} -file {5}".format(bake_root, start_frame, end_frame, step_info, option_flags_str, _path)

                cmds.AbcExport ( j = command_abc )
                path_to_sg.append(_path)
            print(22222222222222, command_abc)
            if ' -stripNamespaces' not in option_flags_str:
                option_flags_str += ' -stripNamespaces'

            if cam_grp_name in bake_root and "/camera/" in _path:
                cmds.select(cl=True)
                cmds.select(cam_grp_name)
                mb_pub_path = re.sub(r"\.abc$", ".mb", _path)
                cmds.file(mb_pub_path, type="mayaBinary",force = True, exportSelected=True,preserveReferences=True, expressions=True)
                path_to_sg.append(mb_pub_path)

            if cmds.ls(target, dag=True, ni=True, type='camera'):
                option_flags_str.replace(cam_append_attr_str, '')


        if exportType == 'submit':
            ma_path = path_list[1]
            dir_path_ma=os.path.dirname(ma_path)
            if not os.path.exists(dir_path_ma) :
                os.makedirs(dir_path_ma)


            cmds.file(ma_path, type="mayaBinary",force = True, ea=True,preserveReferences=True,shader=True, expressions=True)
            cacheSubmit.submit_to_farm(cache_submit_cmd_info_dict, mel_path, ma_path, task, user, thumb, desc)


        # return export path and export type list
        export_info = [path_to_sg , exportType]
        return export_info



    def set_abc_version_attr(self, target, cur_ver, asset_num):
        '''add anim dev version attribute in all transform'''

        all_transform = cmds.ls(target, dagObjects = True, l = True)

        for tr in all_transform:
            user_defined_attr_list=cmds.listAttr(tr, ud=True)
            if user_defined_attr_list == None or 'Alembic_version' not in user_defined_attr_list:
                cmds.addAttr(tr, longName='Alembic_version', shortName='Alembic_version',dataType="string", readable=True, writable=True, storable=True)
            if user_defined_attr_list == None or 'Asset_number' not in user_defined_attr_list:
                cmds.addAttr(tr, longName='Asset_number', shortName='Asset_number', dataType="string", readable=True, writable=True, storable=True)
            cmds.setAttr('{0}.Alembic_version'.format(tr), cur_ver, type='string')
            cmds.setAttr('{0}.Asset_number'.format(tr), asset_num, type='string')

    def check_multiple_target(self, target):
        target_list = cmds.ls(target, l=True)
        if len(target_list) >= 2:
            for _tar in target_list:
                if ':' in _tar and ':geo|' in _tar:
                    return _tar
                elif ':' not in _tar and '|geo|' in _tar:
                    return _tar
            return target_list[-1]
        else:
            return target


    def set_cam_default_attr(self, tar_cam):
        cam_shape_list = cmds.ls(tar_cam, ni=True, dag=True,type="camera")
        if cam_shape_list != []:
            cam_shape = cam_shape_list[0]


class PlayblastItem():
    playblast_w = ''
    playblast_h = ''
    def __init__(self):
        self.abc_export_target_path_dict ={}
        mov_path = None
        wm_mov_path = None
        title_info_dic = {}
        self.playblast_w = ''
        self.playblast_h = ''

    def turn_off_head_up_display(self):
        mel.eval('setAnimationDetailsVisibility(0);')
        mel.eval('setCameraNamesVisibility(0);')
        mel.eval('setCapsLockVisibility(0);')
        mel.eval('setCurrentContainerVisibility(0);')
        mel.eval('setCurrentFrameVisibility(0);')
        # mel.eval('ToggleEvaluationManagerHUDVisibility;')
        mel.eval('setFocalLengthVisibility(0);')
        mel.eval('setFrameRateVisibility(0);')
        mel.eval('setHikDetailsVisibility(0);')
        mel.eval('ToggleMaterialLoadingDetailsHUDVisibility(0);')
        mel.eval('setObjectDetailsVisibility(0);')
        # mel.eval('toggleAxis -o (!`toggleAxis -q -o`);')
        # mel.eval('if (!`exists originAxesMenuUpdate`) {eval "source buildDisplayMenu";} originAxesMenuUpdate;')
        mel.eval('setParticleCountVisibility(0);')
        mel.eval('setPolyCountVisibility(0);')
        mel.eval('setSceneTimecodeVisibility(0);')
        mel.eval('setSelectDetailsVisibility(0);')
        mel.eval('setSymmetryVisibility(0);')
        mel.eval('setViewAxisVisibility(0);')
        mel.eval('setViewportRendererVisibility(0);')

    def pre_do_item(self, m_sg_tk, targets, path_list):
        self.m_sg_tk = m_sg_tk
        # renderWidth = cmds.getAttr("defaultResolution.width")
        # renderHeight = cmds.getAttr("defaultResolution.height")
        #===========================================================================
        # Date and Time
        #===========================================================================
        file_path = LUCY.get_full_path()
        current_file_date = time.ctime(os.path.getctime(file_path))
        full_date = str(current_file_date)
        full_date_list = full_date.split(' ')
        while '' in full_date_list: full_date_list.remove('')

        final_date = "{0}.{1}.{2}".format(full_date_list[4], full_date_list[1], full_date_list[2])
        today_time = full_date_list[3]
        time_data_list = today_time.split(":")
        final_time = "{0}h {1}m {2}s".format(time_data_list[0],time_data_list[1],time_data_list[2])




        #===========================================================================
        # sound for playblast
        #===========================================================================
        sound_node_name_list = cmds.ls(type = 'audio')
        if len(sound_node_name_list) == 0:
            self.sound_name = None
        else:
            self.sound_name = sound_node_name_list.pop()



        #===========================================================================
        # prj_name
        #===========================================================================


        
        prj_name = LUCY.get_project()



        #===========================================================================
        # frame range info : start_time, end_time
        #===========================================================================
        start_time = neon.get_start_time()
        end_time = neon.get_end_time()

        #===========================================================================
        # user_name
        #===========================================================================

        sg_user_name=m_sg_tk.get_user()

        sg_env_command = 'setX SG_USER_NAME {0}'.format(sg_user_name)
        result = subprocess.Popen(sg_env_command, shell = True, stdout=subprocess.PIPE)
        result.communicate()
        user_name = os.getenv('SG_USER_NAME')

        #===========================================================================
        # current_file_name
        #===========================================================================
        full_path = LUCY.get_full_path()
        path_split = full_path.split('/')
        file_name_idx = -1
        current_file_name = path_split[file_name_idx]
        file_name_with_format = current_file_name.split('.')
        file_name_except_format = 0
        current_file_name = file_name_with_format[file_name_except_format]

        #===========================================================================
        # fps
        #===========================================================================
        fps = str(mel.eval('float $fps = `currentTimeUnitToFPS`'))

        #===========================================================================
        # resolution( get from render setting : image size)
        #===========================================================================
        default_w = 1920
        default_h = 1080

        image_w = cmds.getAttr("defaultResolution.width")
        image_h = cmds.getAttr("defaultResolution.height")
        if default_w != image_w:
            self.playblast_w = image_w
        else:
            self.playblast_w = default_w

        if default_h != image_h:
            self.playblast_h = image_h
        else:
            self.playblast_h = default_h



        #===========================================================================
        # Camera info : cam_name, focal_length, crop_factor
        #===========================================================================
        current_panel = cmds.getPanel(wf=True)
        if current_panel.find('modelPanel')<0:
            current_panel = 'modelPanel4'
        panel_num = current_panel.replace('modelPanel','')
        try:
            if int(panel_num) < 3:
                current_panel = 'modelPanel4'
        except Exception as e:
            current_panel = 'modelPanel4'
            print(str(e))

        camName = cmds.modelPanel(current_panel, query=True, camera=True)

        # print('current Panel Name : {0}'.format(current_panel))
        # print('current Panel Num  : {0}'.format(panel_num))
        # print('current Camera name: {0}'.format(camName))


        cam_name = camName
        if not cam_name == 'persp':
            focal_length = cmds.getAttr(cam_name + '.focalLength')

            h = float(cmds.getAttr(cam_name + '.horizontalFilmAperture'))
            v = float(cmds.getAttr(cam_name + '.verticalFilmAperture'))
            fullFrame = math.sqrt(math.pow(2,1.417) + math.pow(2,0.945))
            hyp = math.sqrt(math.pow(2,h) + math.pow(2,v))
            crop_factor = round(fullFrame / hyp,2)

            if ":" in cam_name:
                cam_name = cam_name.replace(":", "\:")



        else:
            focal_length = 'None'
            crop_factor = 'None'
            cam_name = 'persp'





        # make path : two path for versions folder and one for pub folder
        mov_path_idx = 0
        self.pub_mov_path = path_list[mov_path_idx]
        

        self.pub_mov_path_with_wm = self.pub_mov_path.replace('.mov', '_watermark.mov')
        
        dir_path_mov=os.path.dirname(self.pub_mov_path_with_wm)
        if not os.path.exists(dir_path_mov) :
            os.makedirs(dir_path_mov)

        
        title_info_dic = {'prj_name': prj_name, 'start_frame': start_time, 'total_frame':end_time, \
                                        'user_name':user_name, 'current_file_name':current_file_name, 'fps':fps, \
                                        'cam_name':cam_name, 'focal_lenth':focal_length, 'crop_factor':crop_factor, 'final_date':final_date, 'final_time':final_time, 'playblast_w':self.playblast_w, 'playblast_h': self.playblast_h}

        self.add_wm_stamp = wm_stamp.stamp()
        try:
            self.add_wm_stamp.set_path(self.pub_mov_path, self.pub_mov_path_with_wm)
        except wm_stamp.raise_path_error as e:
            print(e)






        self.add_wm_stamp.set_info_text_cmd(title_info_dic, 15)
        # self.add_wm_stamp.set_transparent_box_cmd(177, 'white', 0.8)

        # this for listing up pub files in export pannel ui
        path = [self.pub_mov_path_with_wm]
        self.abc_export_target_path_dict[targets[0]] = path
        return self.abc_export_target_path_dict


    def do_item(self, targets, options, task, user, path_list =None, additional_info=None):
        cmds.select(targets, deselect=True)
        #Run Playblast.
        self.turn_off_head_up_display()
        try:
            cmds.playblast(fp=4, fo=True, clearCache=1, showOrnaments=1, sound=self.sound_name, sequenceTime=0, format='qt', percent=100, filename=self.pub_mov_path, viewer=1, quality=100, widthHeight=(self.playblast_w, self.playblast_h), compression="MS-YUV")
        except Exception as e:
            print(e)
            print('Maybe there is no installed Qucik Time! You need to install it!!!!!')
            # cmds.playblast(fp=4, fo=True, clearCache=1, showOrnaments=1, sound=self.sound_name, sequenceTime=0, format='avi', percent=100, filename=self.pub_version_mov_path_with_ver, viewer=1, quality=100, widthHeight=(1920, 1080))
        try:
            self.add_wm_stamp.create()
        except:
            import traceback
            traceback.print_exc()
        

        desc = additional_info[1]
        self.m_sg_tk.upload_version(self.pub_mov_path_with_wm, desc)

        path_to_sg = [[self.pub_mov_path_with_wm], 'playblast']
        return path_to_sg



class MayaItem():
    def __init__(self):
        self.ma_export_path_dict ={}
        self.project = LUCY.get_project()
    def pre_do_item(self, m_sg_tk, targets, path_list):
        # print('Maya Item : pre-do-item')
        # print(targets)

        self.ma_export_path_dict['ma_ver'] = path_list

        return self.ma_export_path_dict

    def do_item(self, targets, options, task, user, path_list=None, additional_info=None):
        '''
        parameter :
            export_target : [['SWT_0040_mmv_cam','cam'], ['hair_mesh_v03','mesh'], ['vampLordAwakenNew_001','mesh']]
        '''


        '''
        ['X:/projects/2020_02_pipelineEDU/sequence/EDU/EDU_0030/mdl/pub/abc/pub_EDU_0030_mdl.abc',
        'X:/projects/2020_02_pipelineEDU/sequence/EDU/EDU_0030/mdl/pub/abc/versions/pub_EDU_0030_mdl_v01.abc',
            ['X:/projects/2020_02_pipelineEDU/sequence/EDU/EDU_0030/mdl/pub/ma/pub_EDU_0030_mdl.ma', 'X:/projects/2020_02_pipelineEDU/sequence/EDU/EDU_0030/mdl/pub/ma/versions/pub_EDU_0030_mdl_v01.ma'],
        'X:/projects/2020_02_pipelineEDU/sequence/EDU/EDU_0030/mdl/pub/mel/pub_EDU_0030_mdl.mel',
            ['X:/projects/2020_02_pipelineEDU/sequence/EDU/EDU_0030/mdl/pub/ma/pub_EDU_0030_mdl.ma', 'X:/projects/2020_02_pipelineEDU/sequence/EDU/EDU_0030/mdl/pub/ma/versions/pub_EDU_0030_mdl_v01.ma']
        ]
        because the path_list is like this, we have to check it is list.
        (only ma path is list)
        '''
        # get ma list data from path_list
        
        for _path in path_list:
            if isinstance(_path ,list):
                ma_path = _path[0]
                for _p in _path:
                    if _p.endswith(".mb") == True:
                        ma_path = _p
            else:
                if _path.endswith(".mb") == True:
                    ma_path = _path




        if ma_path == None:
            ma_path = path_list[-1]
        dir_path_ma=os.path.dirname(ma_path)
        if not os.path.exists(dir_path_ma) :
            os.makedirs(dir_path_ma)

        cmds.select(cl=True)
        cmds.select(targets)
        cmds.file(ma_path, type="mayaBinary",force = True, es=True,preserveReferences=True,shader=True, expressions=True)
        


        path_to_sg = [ma_path]
        exportType = 'ma'



        # return export path and export type list
        export_info = [path_to_sg , exportType]
        return export_info










class AnimExporter(Exporter):
    def __init__(self, m_sg_tk, p_dialog):
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog
        self.options = None
        self.targets = None
        self.export_order_dict = {'playblast' : PlayblastItem(), 'alembic cache': AbcItem(self), 'maya':MayaItem()}
        


    def pre_execute(self, targets, options):
        # get targets and options from milki_controller
        # if want to change or check target
        
        self.targets = targets

        self.options = options
        self._set_basic_info()
        # get export order in list
        ex_order = self.options['Export Order']
        # pre_execute function purpose : to make export list by pre_do_item function
        # pre_do_item function is declared in AbcItem class and PlayblastItem class
        # pre_do_item fucntion resturn all path of all roots which are in outliner
        # self.get_pub_paths function is declared in exporter class(parent)

        set_infinity()
        # set_cam_attr()
        

        for item in ex_order:
            # if item == 'alembic cache' or item == 'maya':
            #     ma_path_list = self.get_pub_paths('ma')
            #     self.add_pub_files(ma_path_list)
            path_list = []
            if item == 'alembic cache':
                path_list.append(self.get_pub_paths('abc'))
                self.abc_pub_path = path_list[0]
            elif item == 'playblast':
                path_list.append(self.get_pub_paths('mov'))
            elif item == 'maya':
                path_list.append(self.get_pub_paths('mb'))
            export_item = self.export_order_dict[item]
            all_path=export_item.pre_do_item(self.m_sg_tk,self.targets, path_list)
            
            for path in all_path:
                self.add_pub_files(all_path[path])
        pprint.pprint(path_list)

    def execute(self):
        thumb = self.panel.get_thumb()
        desc = self.panel.get_desc()
        additional_info = [thumb, desc]
        self.check_pub_condition()
        try:
            cmds.select(self.targets)
        except Exception as e:
            print(str(e))
        # execute function purpose : to do playblast and do alembic export
        ex_order = self.options['Export Order']
        path_list = []
        for item in ex_order:
            if item == 'alembic cache':
                path_list.append(self.get_pub_paths('abc'))
                path_list.append(self.get_pub_paths('mb'))
                path_list.append(self.get_pub_paths('mel'))
            elif item == 'maya':
                path_list.append(self.get_pub_paths('mb'))
            elif item == 'playblast':
                path_list = self.get_pub_paths('mov')
            export_item = self.export_order_dict[item]
            user = self.m_sg_tk.get_user()
            export_info = export_item.do_item(self.targets, self.options, self.tar_task, user, path_list, additional_info)
            
            # alarm shotgun : only maya alembic cache bake case
            cur_scene_ver = LUCY.get_dev_vernum()
            if item == 'playblast':
                path_to_sg = export_info[0]
                # export_type = export_info[1]
                self.pub_to_sg(path_to_sg, cur_dev_ver=cur_scene_ver)
                continue
            elif item == 'alembic cache':
                path_to_sg = export_info[0]
                export_type = export_info[1]
                if export_type == 'maya_abc':
                    self.pub_to_sg(path_to_sg, cur_dev_ver=cur_scene_ver)
                elif export_type == 'submit':
                    self.pub_to_sg(path_to_sg, cur_dev_ver=cur_scene_ver)
                    continue
            elif item == 'maya':
                path_to_sg = export_info[0]
                # export_type = export_info[1]
                self.pub_to_sg(path_to_sg, cur_dev_ver=cur_scene_ver)


        self.finish(path_list[0])
