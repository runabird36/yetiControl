
from dataclasses import dataclass
from typing import Generator
import PySide2.QtWidgets as QtGui
import maya.cmds as cmds
import maya.mel as mel
from source.YCPackages import (neon, yt_py)
from general_md_3x import LUCY
import shotgun_api3
import os, json, re, time, sys
from functools import partial
from pprint import pprint


from YTX2New_path_module import (HAIR_STEP_PROJECTS_LIST)

import YTX2New_info_model
import importlib
importlib.reload(YTX2New_info_model)

import YTX2New_toolkit as YT
importlib.reload(YT)

import YTX2New_ui_progressbar
importlib.reload(YTX2New_ui_progressbar)

from dialog import YTX2_select_view
importlib.reload(YTX2_select_view)

from dialog import YTX2_furcache_view
importlib.reload(YTX2_furcache_view)

from dialog import YTX2_assign_mode_dialog
importlib.reload(YTX2_assign_mode_dialog)

from customQT import core
importlib.reload(core)


@dataclass
class FurCacheInfo():
    glob_fullpath       :str
    only_fname          :str
    assetname           :str
    ns_number           :str
    yeti_name           :str


@dataclass
class pubInfo():
    pub_path            : str
    pub_json_path       : str
    pub_json_attr_path  : str
    desc                : str
    task_name           : str
    vernum              : str
    created_date        : str
    created_by          : str
    id                  : str
    

class pubInfoHub():
    '''
    {
        taskname : {
                        pub_versions : {
                                        pub_version_number : pubInfo,

                                    },
                        createdBy : str

                    }

    }
    '''
    __hub = {}

    @property
    def hub(self):
        return self.__hub

    def is_empty(self):
        if self.hub == {}:
            return True
        else:
            return False

    def add_task(self, task_name: str) -> None:
        if task_name in self.hub:
            return
        self.hub.update({task_name:{'pub_versions':{}}})

    def add_pubversion(self, task_name: str, pub_vernum: str, pub_info: pubInfo) -> None:
        if pub_vernum in self.hub[task_name]['pub_versions']:
            return
        variant_dict = self.hub[task_name]['pub_versions']
        variant_dict.update({pub_vernum:pub_info})

    



    def get_all_task(self) -> list:
        return list(self.hub.keys())

    def get_all_pubversions(self, task_name: str) -> list:
        return list(self.hub[task_name]['pub_versions'].keys())

    def get_pubinfo(self, task_name: str, pub_vernum: str) -> pubInfo:
        return self.hub[task_name]['pub_versions'][pub_vernum]

    def get_pub_user(self, task_name: str, pub_vernum: str) -> str:
        return self.get_pubinfo(task_name, pub_vernum).created_by
        
    
    





class CFXloadYeti():

    _sg = None
    _model = {}

    def __init__(self):
        self.cur_assetname  = ""
        self._sg            = self.connect_sg()
        self.data_model     = pubInfoHub()
        self.__PIPESTEP__   = "characterfx"
        

    def connect_sg(self):
        print('connect sg')
        SERVER_PATH = 'https://giantstep.shotgunstudio.com'
        SCRIPT_NAME = 'basic_api'
        SCRIPT_KEY  = 'b6dbe937304b44ce2b470d9f817e01941e9412029494bf48896b0617db4c9a1e'

        try:
            proxied_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy='proxy1.giantstep.net:9098')
        except:
            proxied_sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY, http_proxy='')
        return proxied_sg

    def get_target(self) -> str:

        def check_bar_exist(sel_tar) -> str:
            _asset = sel_tar
            if '|' in _asset:
                checked_asset = _asset.split('|')[-1]
            else:
                checked_asset = _asset
            return checked_asset



        sel_list = cmds.ls(sl=True)
        if sel_list == []:
            return ""
        sel_tar = sel_list[0]
        

        mesh_address = sel_tar.split('|')
        for idx, element in enumerate(mesh_address):
            if element == '':
                mesh_address.pop(idx)
        target_mesh = mesh_address.pop()
        if ':' in sel_tar:
            target_mesh = target_mesh.split(':')[1]
        asset_name = target_mesh.split('_')[0]

        
        return check_bar_exist(asset_name)


    # def _get_path_info(self, prj_info_dict, asset_name):
    #     ''' This for getting ma path and json path info '''

    #     files = []
    #     filters = [['project', 'is', prj_info_dict],
    #                 {
    #                     'filter_operator' : 'all',
    #                     'filters': [['code', 'contains',  'pub_'+asset_name], ['code', 'contains', 'cfx']]
    #                  }

    #                   ]
    #     field = ['code', 'path','created_at']

    #     try:
    #         files =  self._sg.find('PublishedFile', filters, field)
    #     except Exception as e:
    #         print(e)
    #         files =[]
    #     print('get cfx file')

    #     cfx_mbs = []
    #     print(files)
    #     for file in files:
    #         fileName =  file['path']['name']
    #         if not 'publish' in fileName and not 'pub' in fileName:
    #             files.remove(file)
    #             continue

    #         ext = os.path.splitext(fileName)[1]
    #         if not ext in ['.mb', '.ma']:
    #             continue
    #         cfx_mbs.append(file)


    #     print(cfx_mbs)
    #     cfx_pub_path = cfx_mbs[0]['path']['url']
    #     cfx_pub_dir = os.path.dirname(cfx_pub_path)

    #     cfx_pub_json_dir = cfx_pub_dir.replace('/cfx/pub/mb', '/cfx/pub/json')
    #     json_full_path = '{0}/pub_{1}_cfx.json'.format(cfx_pub_json_dir, asset_name)

    #     if 'file:///' in cfx_pub_path:
    #         cfx_pub_path = cfx_pub_path.replace('file:///','')

    #     if 'file:///' in json_full_path:
    #         json_full_path = json_full_path.replace('file:///','')
    #         attr_json_full_path = json_full_path.replace('_cfx.json', '_cfx_attr.json')

    #     return [cfx_pub_path, json_full_path, attr_json_full_path]



    def read_json(self, write_json_path):
        with open(write_json_path, 'r') as f:
            json_data_from_file = json.load(f)
        return json_data_from_file




    




    def _simple_import(self, filePath):
        cmds.file(filePath, i = True, namespace = ":", loadReferenceDepth="all", preserveReferences=True, iv = True)


    def get_total_count(self, data_model):
        _count = 0
        for asset_name in data_model:
            magic_name = '{0}_GRP*'.format(asset_name)
            all_asset_tar_list = cmds.ls(magic_name, l=True, typ='transform')

            _count += len(all_asset_tar_list)

        return _count



    # def get_b2TVC_json(self, assetname):
    #     template = 'X:/projects/2020_08_ncB2/assets/char/{0}/cfx/pub/json/pub_{0}_cfx.json'
    #     template_02 = 'X:/projects/2020_08_ncB2/assets/char/{0}/cfx/pub/json/pub_{0}_cfx_attr.json'
    #     return template.format(assetname), template_02.format(assetname)


    


    def check_shapes_data(self, selected_pubinfo: pubInfo) -> set:
        '''
        return one status string from ["error" , "warnning" , "clear"]
        '''
        def get_only_integer(vernum: str) -> int:
            if vernum == "":
                return -999
            return int(re.sub("v", "", vernum))

        status_msg  = ""
        status      = ""
        mdl_pubver_of_cfx = self.read_json(selected_pubinfo.pub_json_path).get("MDL_PUB_VER")
        if mdl_pubver_of_cfx == None:
            status_msg  = "Error : pub josn 파일에서, characterfx 단계에 사용된 modeling 펍 버전을 확인할 수 없습니다.\n"+\
                            "{0} 파일이 있는지 확인 부탁드립니다".format(selected_pubinfo.pub_json_path)
            status      = "error"
            self.ldv_select_view.change_trafficlight(status, status_msg)
            return

        note_contents = neon.get_version_info_from_geo(self.cur_assetname)
        mdl_pubver, mdl_devver = neon.get_ver_info(note_contents)
        print(note_contents)
        print("mdl version by cfx pub       : ", mdl_pubver_of_cfx, get_only_integer(mdl_pubver_of_cfx))
        print("mdl version by anim cache    : ", mdl_pubver, get_only_integer(mdl_pubver))
        print(mdl_pubver == "")
        if mdl_pubver == "" or note_contents == "" or  self.cur_assetname == "":
            status_msg = "Error : 캐쉬에 적혀있는 모델링 펍 버전이 안적혀있거나, 어싸인이 적용되어야하는 어셋이 선택되지 않았습니다."
            status      = "error"
            self.ldv_select_view.change_trafficlight(status, status_msg)
            return


        if get_only_integer(mdl_pubver_of_cfx) == get_only_integer(mdl_pubver):
            status_msg = "조건이 충족되었습니다.\n(사용된 모델링 버전들 일치)\n\n"+\
                        "캐쉬에 사용된 모델링의 basemesh의 scale값이 변경되지 않았는지만 조심하십쇼"
            status      = "clear"

        else:
            status_msg = "Warnning : 캐쉬에 사용된 모델링 버전과, characterfx에 쓰인 모델링 버전이 일치하지 않습니다."
            status      = "warnning"

        self.ldv_select_view.change_trafficlight(status, status_msg)
        return
        
        
        
        




    def query_pubs(self, project, assetname):
        files = []
        filters = [['project.Project.name', 'is', project],
                    {
                        'filter_operator' : 'all',
                        'filters': [
                                    ['code', 'contains',  assetname],
                                    ['sg_published_pipe_step', 'is', self.__PIPESTEP__]
                                   ]
                     }

                      ]
        field = ['code', 'path','created_at', 'task', 'description', 'created_by', 'task.Tasks.task_assignees']

        try:
            files =  self._sg.find('PublishedFile', filters, field)
        except Exception as e:
            print(e)
            files =[]
        # pprint(files)
        return files

    def modify_info(self, sg_info_dict: dict) -> set:
        def make_json_paths(maya_path: str) ->  set:
            maya_dirpath = os.path.dirname(maya_path)
            temp_path = re.sub("/pub/mb/", "/pub/json/", maya_path)
            json_full_path = re.sub(".mb$", ".json", temp_path)
            attr_json_full_path = re.sub(".mb$", "_attr.json", temp_path)
            return json_full_path, attr_json_full_path

        temp_path           = sg_info_dict['path']['url']
        pub_path            = re.sub("^file:////", "/", temp_path)
        pub_json_path, pub_json_attr_path = make_json_paths(pub_path)
        desc                = sg_info_dict['description']
        task_name           = sg_info_dict['task']['name']
        vernum              = LUCY.get_dev_3digit_vernum(input_path=pub_path)
        created_at          = sg_info_dict['created_at'].strftime("%Y.%m.%d")
        created_by          = sg_info_dict['created_by']['name']
        id                  = str(sg_info_dict['id'])
        return pub_path, pub_json_path, pub_json_attr_path, desc, task_name, vernum, created_at, created_by, id

    
    def sg_2_pubInfo(self, pub_sg_list: list) -> Generator:
        for pub_info_dict in pub_sg_list:
            pub_path, pub_json_path, pub_json_attr_path, desc, task_name, vernum, created_at, created_by, id = self.modify_info(pub_info_dict)
            yield pubInfo(pub_path, pub_json_path, pub_json_attr_path, desc, task_name, vernum, created_at, created_by, id)


    def get_yeti_node_name(self, main_data):
        y_list = []
        for key_info in main_data:
            if key_info in ['MDL_PUB_VER', 'MDL_DEV_VER','JSON_DATA', 'MA_DATA', '']:
                continue
            y_list.append(key_info)
        return y_list



    def do_assign(self, selected_pubinfo: pubInfo, **kwargs):

        

        

        print('Set main data model from pub json file')
        all_mesh_attr_list = []
        asset_name = self.cur_assetname
        if '|' in asset_name:
            asset_name = asset_name.split('|')[-1]


        ma_pub_path         = selected_pubinfo.pub_path
        json_pub_path       = selected_pubinfo.pub_json_path
        attr_json_full_path = selected_pubinfo.pub_json_attr_path
        

        _json_data = self.read_json(json_pub_path)
        mesh_info_dict_list = self.read_json(attr_json_full_path).get('mesh')
        if mesh_info_dict_list is not None:
            all_mesh_attr_list.extend(mesh_info_dict_list)

        self._model[asset_name] = _json_data






        start_time = neon.get_start_time()
        cmds.currentTime(int(start_time))


        # init progressbar
        total_asset_count = self.get_total_count(self._model)

        yeti_progressbar_window = YTX2New_ui_progressbar.Ui_ProgressbarUI()
        progress_title = 'Yeti hair 어싸인중...'
        yeti_progressbar_window.setWindowTitle(progress_title)
        yeti_progressbar_window.blackhole_pb.setValue(0)


        before_percentage = 1
        cur_count = 0


        for asset_name, cfx_data in list(self._model.items()):

            grouping_info = {'ASSET_NAME':'', 'TOP_ASSET_TAR':'', 'YETI_LIST':[], 'GRM_LIST':[], 'TEXREF_LIST':[]}
            grouping_info['ASSET_NAME'] = asset_name

            y_info_hub = []
            # Step 1. Delete before data
            #         and make custom yeti data list
            yeti_info_list = self.get_yeti_node_name(cfx_data)
            for cur_yeti in yeti_info_list:
                cur_yeti_info_dict = cfx_data.get(cur_yeti)
                shape_info_list = cur_yeti_info_dict.get("ALL_SHAPE")
                groom_info_list = cur_yeti_info_dict.get("GROOM")
                material_data = cur_yeti_info_dict.get("MAT")
                grm_path = cur_yeti_info_dict.get("GRM_DATA")[0]

                is_curve_type = cur_yeti_info_dict.get('IS_CURVE_VER')
                if is_curve_type == True:
                    set_and_curves_list = cur_yeti_info_dict.get('SET_WITH_CURVES')
                else:
                    set_and_curves_list = []

                image_search_path = cur_yeti_info_dict.get('ISPATH')
                render_denstiy = cur_yeti_info_dict.get('RDENSTIY')

                shape_and_grm_list = cur_yeti_info_dict.get('SHAPE2GRM')


                cur_yeti_var_data_dict = cur_yeti_info_dict.get('YETI_VAR')
                if cur_yeti_var_data_dict is None:
                    float_var_list = []
                    vector_var_list = []
                else:
                    float_var_list = cur_yeti_var_data_dict.get('YETI_F_VAR')
                    if float_var_list is None:
                        float_var_list = []

                    vector_var_list = cur_yeti_var_data_dict.get('YETI_VEC_VAR')
                    if vector_var_list is None:
                        vector_var_list = []



                _y_data = YTX2New_info_model.YetiData(cur_yeti, groom_info_list, shape_info_list, material_data, grm_path,
                                                    is_curve_type, set_and_curves_list, image_search_path, shape_and_grm_list, render_denstiy,
                                                    float_var_list, vector_var_list)
                print('='*100)
                print(_y_data)
                _y_data.disconnect_and_delete_all()
                y_info_hub.append(_y_data)



            # Step 2. Import ma file
            ma_path = cfx_data.get("MA_DATA")[0]
            self._simple_import(ma_path)



            # Step 3. Query all assetname_GRP
            magic_name = '{0}_GRP*'.format(asset_name)
            all_asset_tar_list = cmds.ls(magic_name, l=True, typ='transform')
            


            # Step 4. Assign yeti data model to all assetname_GRP
            for _assetname_GRP in all_asset_tar_list:

                cur_count += 1

                res = YT.do_assign(_assetname_GRP, y_info_hub)
                if res == False:
                    del yeti_progressbar_window
                    return

                percentage = float(cur_count)/float(total_asset_count)*100
                yeti_progressbar_window.ATX_fname_lb.setText('전체 {0}개 중, {1} 번째\n현재 Asset : {2}'.format(str(total_asset_count), str(cur_count), _assetname_GRP))
                for i in range(int(before_percentage), int(percentage)+1):
                    yeti_progressbar_window.blackhole_pb.setValue(int(i))
                    QtGui.QApplication.processEvents()
                    time.sleep(0.02)
                before_percentage = percentage



        for _mesh_info in all_mesh_attr_list:
            _mesh_attr_fullname = _mesh_info.get('ATTR_FULLNAME')
            _mesh_attr_value = _mesh_info.get('ATTR_VALUE')

            _shape_name = _mesh_attr_fullname.split('.')[0]
            _shape_attr_name = _mesh_attr_fullname.split('.')[1]


            all_shape_list = cmds.ls(_shape_name, l=True)

            for _cur_shape in all_shape_list:
                real_attr_fullname = '{0}.{1}'.format(_cur_shape, _shape_attr_name)
                print(real_attr_fullname, '--->', _mesh_attr_value)
                print('='*50)
                try:
                    if _mesh_attr_value == None:
                        continue
                    cmds.setAttr(real_attr_fullname, _mesh_attr_value)
                except Exception as e:
                    print(str(e))

        del yeti_progressbar_window


        confirm_dialog = core.get_confirm_dialog("YTX2", "어셋 이름 : {0}\n어싸인 완료!".format(self.cur_assetname), "clear", ["ok"])


    def do_furCache_assign(self, *args, **kwargs) -> None:
        def make_yetishape_name(fur_cache_info :FurCacheInfo) -> str:
            return '{ASSETNAME}_{YETI_NAME}_YETIShape'.format(
                                                                ASSETNAME=fur_cache_info.assetname,
                                                                YETI_NAME=fur_cache_info.yeti_name
                                                            )

        # Step 01. rearrange .fur files in dictionary of FurCacheInfo
        sg_pub_info = args[0]

        fur_dir     = args[1][0]
        file_list   = os.listdir(fur_dir)
        
        file_info_hub   = {}

        for _fname in file_list:
            if os.path.isdir(_fname) == True:
                continue
            if os.path.splitext(_fname)[-1] != ".fur":
                continue
            
            only_fname = re.sub(r"\d+\.[a-zA-Z]+$", "", _fname)
            if only_fname in file_info_hub:
                continue



            asset_ns   = re.search(r"^\w+\_\d{3}", only_fname).group()
            assetname  = asset_ns.split('_')[0]
            yeti_name  = only_fname.replace(asset_ns, "")
            yeti_name  = re.sub(r"(\.|\_)", "", yeti_name)
            glob_path  = fur_dir + "/" + re.sub(r"\d+\.fur", "%04d.fur", _fname)

            file_info_hub[only_fname] = FurCacheInfo(glob_path, only_fname, assetname, asset_ns, yeti_name)



        # Step 02. get .ma asset pub filepath and .json asset pub filepath 
        #          (Among publishedFiles, get the latest one)
        pub_path, pub_json_path, pub_json_attr_path, desc, task_name, vernum, created_at, created_by, id  = self.modify_info(sg_pub_info)
        yeti_json_info = self.read_json(pub_json_path)
        
        

        # Step 03. create reference with maya pub file for material
        self._simple_import(pub_path)

        # Step 04.
        #       - Query all assetname_GRP
        #       - create group hierarchy
        magic_name = '{0}_GRP*'.format(self.cur_assetname)
        all_asset_tar_list = cmds.ls(magic_name, l=True, typ='transform')
        all_targets = {}
        for cur_assetname in all_asset_tar_list:
            cur_top_node, ns_num = YT.create_yeti_group_sim_ver(cur_assetname)
            asset_ns_name = self.cur_assetname + "_" + ns_num
            all_targets[asset_ns_name] = cur_top_node

        
        # Step 05.
        #       - find right basemesh
        #       - create yeti node 
        #       - set .fur path / image search path
        #       - assign material
        for fname_prefix, fur_cache_info in list(file_info_hub.items()):
            cur_ns_name     = fur_cache_info.ns_number
            only_ns_number  = cur_ns_name.split('_')[-1]
            
            key_yetishape = make_yetishape_name(fur_cache_info)
            if key_yetishape not in yeti_json_info:
                continue


            # Fur cache full path
            fur_fullpath = fur_cache_info.glob_fullpath
            # This variable have yeti info (image searche path / basemesh ...)
            yeti_node_in_json   = yeti_json_info.get(key_yetishape)
            img_search_path     = yeti_node_in_json.get("ISPATH")
            hair_mat            = yeti_node_in_json.get("MAT")
            render_density      = yeti_node_in_json.get("RDENSTIY")



            # Find right basemesh part
            y_input_shape_list = []
            shape_texRef_pair_list = yeti_node_in_json.get("ALL_SHAPE")
            for shape_texRef_info in shape_texRef_pair_list:
                tar_shape_info = shape_texRef_info.get("EACH_shape")
                cur_top_node = all_targets[cur_ns_name]
                tar_basemesh = YT.find_exactTar_under_curTopNode(cur_top_node, tar_shape_info)
                if tar_basemesh == '':
                    print('='*50)
                    print('Error : There is no hair base mesh!!!!!!!!!!!!!')
                    print('--------> {0}'.format(tar_shape_info))
                    print('='*50)
                    continue
                y_input_shape_list.append(tar_basemesh)
                

            # Create yeti node part
            _y_node_name = key_yetishape.split('Shape')[0] + '_{0}'.format(only_ns_number)
            created_yeti = yt_py.create_yeti_node(_y_node_name)
            created_yeti = YT.grouping_tar(cur_top_node, created_yeti, 'YETI')

            for tar_shape in y_input_shape_list:
                yt_py.add_basemesh_to_yeti(created_yeti, tar_shape)



            
            cache_file_attr     = created_yeti + ".cacheFileName"
            file_mode_attr      = created_yeti + ".fileMode"
            override_attr       = created_yeti + ".overrideCacheWithInputs"
            img_search_path_attr= created_yeti + ".imageSearchPath"
            render_density_attr = created_yeti + ".renderDensity"
            display_width_attr  = created_yeti + ".viewportWidth"




            if img_search_path != None:
                if '\\' in img_search_path:
                    img_search_path = img_search_path.replace('\\', '/')
                cmds.setAttr(img_search_path_attr, img_search_path, typ="string")

            
            cmds.setAttr(cache_file_attr, fur_fullpath, typ="string")
            cmds.setAttr(file_mode_attr, 1)
            

            

            cmds.setAttr(display_width_attr, 1)
            cmds.setAttr(render_density_attr, render_density)

            
            cmds.select(created_yeti)
            cmds.hyperShade(assign=hair_mat)

        return

        




    def run(self):
        def _maya_main_window():
            '''
            Get the maya main window as a QMainWindow instance
            '''
            import maya.cmds as cmds
            import maya.OpenMayaUI as mui
            from shiboken2 import wrapInstance
            ptr = mui.MQtUtil.mainWindow()
            if ptr is not None:
                    return wrapInstance(int(ptr),QtGui.QWidget)



        print('project info data')
        _maya_view = _maya_main_window()
        # prj_name = LUCY.get_project()
        # if prj_name in HAIR_STEP_PROJECTS_LIST:
        #     self.__PIPESTEP__ = "hair"
        
        self.mode_select_view = YTX2_assign_mode_dialog.YFBSelModeDialog(_maya_view)

        assign_mode = None
        if self.mode_select_view.exec_():
            assign_mode = self.mode_select_view.get_res()
        else:
            return
        if assign_mode == None:
            confirm_dialog = core.get_confirm_dialog("YTX2", "Assign mode가 선택되지 않았습니다.", "warnning", ["ok"])
            return

        
        print('asset name')
        asset_name = self.get_target()
        if asset_name == "":
            confirm_dialog = core.get_confirm_dialog("YTX2", "어셋이 선택되지 않았습니다.", "warnning", ["ok"])
            return
        
        self.cur_assetname = asset_name



        pub_cfx_files_list = self.query_pubs(prj_name, asset_name)
        pub_cfx_files_list.sort(key=lambda x : x.get("created_at"))
        
        if pub_cfx_files_list == []:
            confirm_dialog = core.get_confirm_dialog("YTX2", "샷건에서 정보를 가져올 수 없습니다.", "warnning", ["ok"])
            return
        for pub_info in self.sg_2_pubInfo(pub_cfx_files_list):
            self.data_model.add_task(pub_info.task_name)
            self.data_model.add_pubversion(pub_info.task_name, pub_info.vernum, pub_info)
        
        
        
        
        
        
        
        if assign_mode == ".grm (Asset)":
            self.ldv_select_view = YTX2_select_view.Ui_SelectPubDialog(_maya_view, self.data_model)
            self.ldv_select_view.close_signal.connect(partial(self.do_assign, MAYA_VIEW=_maya_view))
            self.ldv_select_view.check_modeling.connect(self.check_shapes_data)
            self.ldv_select_view.show()
        elif assign_mode == ".fur (Shot)":
            the_lastes_pubinfo = pub_cfx_files_list[-1]

            self.fur_cache_view = YTX2_furcache_view.Ui_YTX2_fur_mw()
            self.fur_cache_view.close_signal.connect(partial(self.do_furCache_assign, the_lastes_pubinfo))
            self.fur_cache_view.show()
        return






