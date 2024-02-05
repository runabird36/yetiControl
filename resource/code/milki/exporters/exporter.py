from tabnanny import check
import basic_item
# reload (basic_item)
from basic_item import BasicItem
import threading
import os
from general_md_3x import LUCY
import re
import sys
import shutil
import maya.mel as mel
import maya.cmds as cmds


class Exporter(BasicItem):
    

    # pub_templates = {
    #                 'top' : '{root}/pub/{ext}/pub_{file_name}.{ext}',
    #                 'version': '{root}/pub/{ext}/versions/pub_{file_name}_{version}.{ext}',
    #                 'top_with_postfix' : '{root}/pub/{ext}/pub_{file_name}_{postfix}.{ext}',
    #                 'version_with_postfix': '{root}/pub/{ext}/versions/pub_{file_name}_{version}_{postfix}.{ext}'
    #                 }

    pub_templates = {
                    'top' : '{root}/pub/{ext}/{version}/{file_name}',
                    }

    m_sg_tk = None
    progress_dialog = None
    tar_task = None
    finish_func = None

    def __init__(self):
        BasicItem.__dict__['__init__'](self)
        self.set_type("Exporter")



    
    



    def _get_entity_name(self):
        if LUCY.is_assets():
            return LUCY.get_assetname()
        else:
            return LUCY.get_shot()

    def _set_task_info(self):
        prj = LUCY.get_project()
        entity_name = self._get_entity_name()
        step = LUCY.get_pipe_step()
        scene_type = LUCY.get_category()
        self.m_sg_tk.task_queried.connect(self._set_my_task)

        t = threading.Thread(target=self.m_sg_tk.get_task, args = (prj, entity_name, step, scene_type))
        t.start()

    def _set_my_task(self, task):
        import pprint
        print(task)
        msg = ''
        if len(task) > 0:
            msg = "Task: {0}".format(task['content'])
            self.tar_task = task
            self.panel.set_info_label(msg)
        else:
            msg = "WARNING: Can not find task to publish"
            self.panel.set_info_label(msg, negative = True)

    def _set_basic_info(self):
        if self.panel is None:
            return
        self.panel.pub_info_label.setText("Searching Task...")
        self._set_task_info()

    def add_pub_files(self, file_paths):
        for file_path in file_paths:
            self.add_pub_file(file_path)

    def add_pub_file(self, file_path):
        return self.panel.add_pub_file_item(file_path)

    def start_make_tex_thumb(self):
        self.panel.start_make_tex_thumb()

    def remove_version(self, file_name):
        version_finder = re.compile('v\d+')
        ver = version_finder.search(file_name)
        ver_idx = ver.start() - 1

        return file_name[:ver_idx]

    def get_mov_common_path(self):
        file_name = LUCY.get_file_name()
        entity_with_step = self.remove_version(file_name)
        _temp = entity_with_step.split('_')
        _temp.pop()
        _entity = '_'.join(_temp)
        return '{0}/{1}/{2}_{3}_{4}.mov'.format(LUCY.get_mov_dir(), LUCY.get_dev_vernum(),
                                                _entity, LUCY.get_task(), LUCY.get_dev_vernum())

    def get_arnold_attr_json_path(self):
        
        cur_filepath = LUCY.get_full_path()
        dev_idx = cur_filepath.index('/dev')
        path_root = cur_filepath[:dev_idx]
        

        
        element_dict = {}
        element_dict['root'] = path_root
        element_dict['version'] = LUCY.get_dev_vernum()
        element_dict['assetname'] = LUCY.get_assetname()
        
        return '{root}/pub/json/{version}/{assetname}_arnold_attr_{version}.json'.format(**element_dict)

    def get_pub_paths(self, ext:str, postfix:str='') -> str:

        def get_only_vernum_folder(check_path: str) -> list:
            vernum_folder_list = []
            for foldername in os.listdir(check_path):
                if re.search(r"v\d+", foldername):
                    vernum_folder_list.append(foldername)
            return vernum_folder_list

        def get_lastver_by_folder(ver_list :list) -> str:
            return ver_list[-1]

        def get_lastver_by_filename(root_path, ver_list, postfix):
            last_ver = ""
            ver_list.sort(reverse=True)
            for vernum in ver_list:
                check_ver_path = root_path+'/'+vernum
                if os.path.isdir(check_ver_path) == False:
                    continue
                for pub_filename in os.listdir(check_ver_path):
                    if postfix == "" and re.search(r"v\d{3}\.[a-zA-Z]+$", pub_filename):
                        last_ver = vernum
                        return last_ver
                    elif postfix != "" and postfix in pub_filename:
                        last_ver = vernum
                        return last_ver
        
            return "v000"

        def get_next_ver(check_path, postfix=""): 
            print(check_path)
            if os.path.exists(check_path) is False:
                return "v001"
            # ver_list = os.listdir(check_path)
            ver_list = get_only_vernum_folder(check_path)
            
            ver_list.sort()
            # ver_list.sort(reverse=True)
            if ver_list == []:
                return "v001"
            

            if LUCY.get_pipe_step() in ["lighting"]:
                last_ver     = get_lastver_by_folder(ver_list)
            else:
                if postfix == "":
                    last_ver = get_lastver_by_filename(check_path, ver_list, "")
                else:
                    last_ver = get_lastver_by_filename(check_path, ver_list, postfix)

            # print(check_path)
            # print(last_ver)
                

            only_num = int(last_ver.replace("v", ""))
            only_num += 1
            next_lat_ver = "v" + str(only_num).zfill(3)
            return next_lat_ver

        def add_postfix(from_name, ext, postfix):
            if "_" in postfix and ext not in ["abc"]:
                postfix = postfix.replace("_", "")
            return re.sub("\."+ext, "_"+postfix+"."+ext, from_name)

        
        if ext in ['mov']:
            return [self.get_mov_common_path(), '']

        path_dic = {}
        full_path = LUCY.get_full_path()
        path_split = full_path.split('/')
        
        dev_idx = path_split.index('dev')
        path_dic['root'] = '/'.join(path_split[:dev_idx])
        
        ver_checkpath = path_dic['root'] + "/" + "pub" + "/" + ext 
        
        vernum = get_next_ver(ver_checkpath, postfix)
        print(111111111111111111)
        print(vernum)
        path_dic['version'] = vernum
        path_dic['ext'] = ext
        entity_dict = LUCY.get_entity()
        entity_dict.update({'pubversion_code':vernum})
        entity_dict.update({'ext_code':ext})
        path_dic['file_name'] = LUCY.get_basic_pubfilename(_elements=entity_dict)

        if postfix == '':
            return self.pub_templates['top'].format(**path_dic)
        else:
            filename_with_postfix = add_postfix(path_dic['file_name'], path_dic['ext'], postfix)
            path_dic.update({'file_name':filename_with_postfix})
            return self.pub_templates['top'].format(**path_dic)

    def check_pub_condition(self):
        if self.tar_task is None:
            raise Exception("Can not find any task to publish")
            return

        thumb = self.panel.get_thumb()
        desc = self.panel.get_desc()
        if thumb is None or desc is None:
            raise Exception("Please enter screen shot or any description")

    def pub_to_sg(self, paths, change_status=True, cur_dev_ver=""):
        thumb = self.panel.get_thumb()
        desc = self.panel.get_desc()
        is_prepub = self.panel.get_prepub_status()

        cur_step = LUCY.get_pipe_step()

        prj_info_dict, pub_id_list = self.m_sg_tk.create_new_sg_pubfiles(paths, thumb, desc,
                                                                        change_sg_status=change_status,
                                                                        scene_ver=cur_dev_ver,
                                                                        pipe_step=cur_step)
        if is_prepub is True:
            self.m_sg_tk.set_prepub_status()

        prj_name = prj_info_dict.get('name')
        # pub_id = int(pub_id)
        print('Start to copy thumb image')
        try:
            self.copy_thumb_to_server(thumb, prj_name, pub_id_list)
        except Exception as e:
            print(str(e))

    def copy_thumb_to_server(self, local_thumb_path, prj_name, pub_id_list):
        if sys.platform.count("win"):
            server_path_template = 'Z:/linux/shotgrid_DB/sg_thumbnails/projects/{0}/publishFiles/{1}.png'
        else:
            server_path_template = "/usersetup/linux/shotgrid_DB/sg_thumbnails/projects/{0}/publishFiles/{1}.png"
        for pub_id in pub_id_list:
            server_thumb_path = server_path_template.format(prj_name, pub_id)

            try:
                dir_server_thumb_path = os.path.dirname(server_thumb_path)
                if not os.path.exists(dir_server_thumb_path) :
                    os.makedirs(dir_server_thumb_path)

                shutil.copy2(local_thumb_path, server_thumb_path)
                print('Success : copy thumb image !!!')
            except Exception as e:
                print(str(e))
                print('Fail : copy thumb image !!!')

    def set_finish_func(self, func):
        self.finish_func = func

    def finish(self, pub_path):
        self.finish_func(pub_path)

    def pre_execute(self, targets, options):
        raise NotImplementedError("pre_execute must be implemented")

    def execute(self):
        raise NotImplementedError("execute must be implemented")

    def clean_file(self):
        mel_cmd = '{\n'+\
                    '\tstring $unknownNodes[] = `lsType unknown`;\n'+\
                    '\tfor($node in $unknownNodes){\n'+\
                        '\t\tif($node=="<done>")\n'+\
                            '\t\t\tbreak;\n'+\
                        '\t\tif(`objExists $node`)\n'+\
                        '\t\t{\n'+\
                            '\t\t\tint $lockState[] = `lockNode -q -l $node`;\n'+\
                            '\t\t\tif($lockState[0]==1)\n'+\
                            '\t\t\tlockNode -l off $node;\n'+\
                            '\t\t\tdelete $node;\n'+\
                        '\t\t}\n'+\
                    '\t}\n'+\
                '}'
        mel.eval(mel_cmd)
        
    def clean_file_py(self) -> None:
        import maya.cmds as cmds
        un_nodes = cmds.ls(type="unknown")
        un_plugins = cmds.unknownPlugin(q=True, l=True)
        
        print(un_nodes)
        print(un_plugins)
        del_count = 0
        if un_plugins:
            for cur_plugin in un_plugins:
                try:
                    cmds.unknownPlugin(cur_plugin, r=True)
                    del_count += 1
                except:
                    pass
        _msg = "채크 완료\n삭제 노드 개수 : {0}".format(str(del_count))
        print(_msg, file=sys.stdout)
        
    def set_arnold_render_setting(self) -> None:
        plugin_name = "mtoa"
        res = cmds.pluginInfo(plugin_name, query=True, loaded=True)
        if res == False:
            cmds.loadPlugin(f"{plugin_name}.so")
        
        cur_renderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")
        if cur_renderer != 'arnold':
            return
        
        check_preferred_renderer = cmds.preferredRenderer( query=True )
        if check_preferred_renderer == None:
            return
    
        cmds.preferredRenderer( makeCurrent=True )
        
        cmds.setAttr( "defaultArnoldRenderOptions.motion_blur_enable",      1 )
        cmds.setAttr( "defaultArnoldRenderOptions.mb_camera_enable",        1 )
        cmds.setAttr( "defaultArnoldRenderOptions.mb_object_deform_enable", 1 )
        cmds.setAttr( "defaultArnoldRenderOptions.motion_steps",            2 )
        cmds.setAttr( "defaultArnoldRenderOptions.range_type",              1 )
        cmds.setAttr( "defaultArnoldRenderOptions.motion_frames",           0.5 )
        
        
        


    
    
