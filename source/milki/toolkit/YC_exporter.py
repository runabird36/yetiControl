
from importlib import reload
import maya.cmds as cmds
import maya.mel as mel

import os, pprint, time, json, re, sys


from source.YCPackages import (neon, yt_py)


from source.YC_core_module import (__PUB_PATH_TEMPLATE__,
                                    get_assetname,
                                    get_pub_paths)

















class CFXExporter():

    pub_paths = []

    def __init__(self):
        YCPackages_dir_path = os.environ['HGWEAVER_YETI_ROOT'] + "/" + "source" + "/" + "YCPackages"
        YCPackages_dir_path = YCPackages_dir_path.replace("\\", "/")
        self.grp_re_ex = re.compile('GRP$|GRP\d+$')
        self.geo_re_ex = re.compile('GEO$|GEO\d+$')
        self.geoshape_re_ex = re.compile('GEOShape$|GEOShape\d+$')
        
        mel.eval('source \"{0}/yeti_util.mel\"'.format(YCPackages_dir_path))
        
        self.mesh_attr_list = ['.yetiSubdivision', '.yetiSubdivisionIterations']
        self.grm_attr_list = ['.partRandomness', '.automaticParting', '.automaticPartingAngleThreshold', '.automaticPartingReferencePosition']
        self.set_attr_list = ['.mng']
        self.curves_attr_list = ['.baseAttraction', '.tipAttraction', '.innerRadius', '.outerRadius', '.guideModel', '.attractionProfile[0].attractionProfile_FloatValue', '.attractionProfile[0].attractionProfile_Position', '.attractionProfile[1].attractionProfile_FloatValue', '.attractionProfile[1].attractionProfile_Position']

    def get_attr_info_fromNode(self, _node_type, _tar_node):
        '''
        {
            node_type :
                        [
                            {node_name.attr_name : attr_value},
                            {node_name.attr_name : attr_value}
                            ...
                        ]

        }
        '''
        _check_attr_list = []
        if _node_type == 'mesh':
            _check_attr_list = self.mesh_attr_list
        elif _node_type == 'pgYetiGroom':
            _check_attr_list = self.grm_attr_list
        elif _node_type == 'objectSet':
            _check_attr_list = self.set_attr_list
        elif _node_type == 'nurbsCurve':
            # =============================================================================
            # Get attr info from first nurbsCurve of set!!!
            #  --> So if the multiple nurbsCurve groups are included in set,
            #      need to query attr info from first nurbsCurve of each groups
            # =============================================================================
            _check_attr_list = self.curves_attr_list
            hair_curve_list = cmds.sets(_tar_node, q=True)
            one_curve_shape = cmds.ls(hair_curve_list[0], dag=True, ni=True, shapes=True)[0]

        for _check_attr in _check_attr_list:
            try:
                if _node_type == 'nurbsCurve':
                    check_attr_fullname = one_curve_shape + _check_attr
                else:
                    check_attr_fullname = _tar_node+_check_attr
                if cmds.objExists(check_attr_fullname) == False:
                    continue
                _tar_value = cmds.getAttr(check_attr_fullname)

                self.pub_attr_dict[_node_type].append({'ATTR_FULLNAME':_tar_node+_check_attr,'ATTR_VALUE':_tar_value})
            except Exception as e:
                print(str(e))

    def get_curv_grps_from_curvSet(self, set_name):
        crv_grps_list = []
        hair_curve_list = cmds.sets(set_name, q=True)
        crv_grps_list = list(set(cmds.listRelatives(hair_curve_list, p=True)))
        return crv_grps_list

    def get_linked_material(self, yeti_node):
        ''' Get assigned material to yeti node : string '''

        _linked_shdg_list = cmds.listConnections(yeti_node, s=False, d=True)
        for _shdg in _linked_shdg_list:
            if _shdg in ['MayaNodeEditorSavedTabsInfo']:
                continue
            else:
                _shdg_linked_n_list = cmds.listConnections(_shdg, s=True, d=False)
                for _node in _shdg_linked_n_list:
                    _node_type = cmds.nodeType(_node)
                    if _node_type == 'transform':
                        continue
                    else:
                        target_material = _node
                        return target_material
                        break
                break
        return 'lambert1'

    def create_shape_info(self, tar_shape):
        ''' Create texture reference from selected shape '''
        ''' and make dictionary data '''

        _tar_GEOShape = tar_shape
        if cmds.objectType(tar_shape) == 'mesh' and self.geoshape_re_ex.search(tar_shape):
            tar_shape = cmds.listRelatives(tar_shape, p=True)[0]
        else:
            tar_shape = _tar_GEOShape



        cmds.select(tar_shape)
        existance_check_tar = '{0}_reference'.format(tar_shape)
        if not cmds.objExists(existance_check_tar):
            mel.eval('CreateTextureReferenceObject;')

        tar_attr = '{0}.referenceObject'.format(tar_shape)
        tex_ref_obj = cmds.listConnections(tar_attr, s=True, d=False)[0]


        return {'EACH_shape':_tar_GEOShape, 'EACH_texRef':tex_ref_obj}

    def rename_and_updateYTGraph(self, from_shape, to_shape, yeti_node):
        ''' If target shape name is changed because of bind skin ( ShapeDeformed postfix ) '''
        ''' Rename shape '''
        ''' Query import node in yeti graph '''
        ''' Change input geometry parameter '''
        cmds.rename(from_shape, to_shape)
        # remove_cmd = 'pgYetiRemoveGeometry(\"{0}\", \"{1}\")'.format(from_shape, yeti_node)
        # mel.eval(remove_cmd)
        # add_cmd = 'pgYetiAddGeometry(\"{0}\", \"{1}\")'.format(to_shape, yeti_node)
        # mel.eval(add_cmd)

        mel.eval('select {0}'.format(yeti_node))
        if sys.platform.count("win"):
            mel.eval('source "Z:/backstage/maya/milki/toolkits/yeti_util.mel"')
        else:
            mel.eval("source '/usersetup/linux/scripts/maya_sc/milki/toolkits/yeti_util.mel'")
        mel.eval('string $_import_node = get_import_node();')
        mel.eval('string $_import_geo_name = `pgYetiGraph -node $_import_node -param "geometry" -getParamValue`;')
        mel.eval('if($_import_geo_name != \"{0}\"){{pgYetiGraph -node $_import_node -param "geometry" -setParamValueString \"{0}\";}}'.format(to_shape))
        mel.eval('string $_to_shape = \"{0}\"'.format(to_shape))
        mel.eval('set_input_geo($_import_node, $_import_geo_name, $_to_shape)')

    def dirpath_check_makedirs(self, full_path):
        dir_path = os.path.dirname(full_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def export_groom_from_selectedY(self, _yeti_node, _grm_pub_path):
        ''' Use custom exporting mel function ( toolkits/yeti_util.mel ) '''
        ''' and export groom data from selected yeti node  '''
        cmds.select(_yeti_node)
        mel_cmd = 'G_pgYetiExportGroomFromSelected(\"{0}\");'.format(_grm_pub_path)
        mel.eval(mel_cmd)

    def check_and_get_yVariables(self, _y_node):
        var_info_dict = {"YETI_F_VAR":[], "YETI_VEC_VAR":[]}

        f_var_list = cmds.listAttr(_y_node, r=True, st="yetiVariableF_*")
        vec_var_list = cmds.listAttr(_y_node, r=True, st="yetiVariableV_*")

        if f_var_list:
            for _f_var in f_var_list:
                _temp_info_dict = {"y_type":"FLOAT" , "name":_f_var, "Y_value":None, "Y_min":None, "Y_max":None}
                if cmds.attributeQuery(_f_var, node=_y_node, minExists=True) is True:
                    _temp_info_dict["Y_min"] = cmds.attributeQuery(_f_var, node=_y_node, min=True)
                if cmds.attributeQuery(_f_var, node=_y_node, maxExists=True) is True:
                    _temp_info_dict["Y_max"] = cmds.attributeQuery(_f_var, node=_y_node, max=True)

                _temp_info_dict["Y_value"] = cmds.getAttr("{0}.{1}".format(_y_node, _f_var))

                var_info_dict["YETI_F_VAR"].append(_temp_info_dict)

        if vec_var_list:
            for _vec_var in vec_var_list[0::4]:
                _temp_info_dict = {"y_type":"VECTOR", "name":_vec_var, "detail":[
                                                                {"name":_vec_var+"X", "Y_value":None, "Y_min":None, "Y_max":None},
                                                                {"name":_vec_var+"Y", "Y_value":None, "Y_min":None, "Y_max":None},
                                                                {"name":_vec_var+"Z", "Y_value":None, "Y_min":None, "Y_max":None}
                                                                ]}
                for _element in _temp_info_dict.get("detail"):
                    _cur_vec_element = _element.get('name')
                    if cmds.attributeQuery(_cur_vec_element, node=_y_node, minExists=True) is True:
                        _element["Y_min"] = cmds.attributeQuery(_cur_vec_element, node=_y_node, min=True)
                    if cmds.attributeQuery(_cur_vec_element, node=_y_node, maxExists=True) is True:
                        _element["Y_max"] = cmds.attributeQuery(_cur_vec_element, node=_y_node, max=True)

                    _element["Y_value"] = cmds.getAttr("{0}.{1}".format(_y_node, _cur_vec_element))

                var_info_dict["YETI_VEC_VAR"].append(_temp_info_dict)

        return var_info_dict

    def pre_execute(self, targets :str, variant_name :str="default", vernum :str="v001", selected_dirpath :str="") -> list:
        
        self.target = targets
        cmds.select(self.target)
        self.export_json_info = {}
        cur_assetname = get_assetname()
        self.cur_vernum = vernum
        # Rule !!
        #    1. Query information and Export ,based on Yeti Node
        #    2. When Load, get target shape list for creating yeti node. and, load grm file in that yeti node
        #    3. No matter how the grm and shape are connected to a single yeti node or, are connected to each other, The information are written in one grm file


        # make json template
        #       [key]
        #       - yeti node
        #       [values : dict]
        #       - groom nodes ('GROOM')     : list []
        #       - shape names ('ALL_SHAPE') : list of dict that include shape and texture reference pair [ {  'EACH_shape' : string  ,  'EACH_texRef' : string  } , { : }, { : }...]
        #       - materials   ('MAT')       : string
        #       - pub_data    ('GRM_DATA')  : string  :  full path
        #
        #       [key : MA_DATA]             : [values : list : full path with version path]
        #       [key : JSON_DATA]           : [values : list : full path with version path]

        # query yeti node
        #   - query shape info from yeti node
        #       - make texture reference and rename and query info from each shape info
        #   - query groom info from yeti node
        #   - query mat info from yeti node
        self.pub_attr_dict = {'pgYetiGroom':[], 'objectSet':[], 'nurbsCurve':[], 'mesh':[]}
        all_yeti_list = cmds.ls(type='pgYetiMaya')
        for _y_node in all_yeti_list:
            _linked_node_list = cmds.listConnections(_y_node, d=False, s=True, sh=True)
            _shape_list = []
            _groom_list = []
            _shape_to_grm_info_list = []
            _SET_EXISTS = False
            _curve_info_list = []
            for _linked_node in _linked_node_list:
                _node_type = cmds.nodeType(_linked_node)
                if _node_type == 'mesh':
                    _shape_info_dict = self.create_shape_info(_linked_node)
                    _shape_list.append(_shape_info_dict)

                    self.get_attr_info_fromNode('mesh', _shape_info_dict.get('EACH_shape'))

                    # linked_grm_list = cmds.listConnections(_linked_node, d=True, s=False, t='pgYetiGroom')
                    # _shape_to_grm_info_list.append({'EACH_shape':_linked_node, 'EACH_grm_list':linked_grm_list})
                elif _node_type == 'pgYetiGroom':
                    _groom_list.append(_linked_node)

                    _linked_shape_attr = cmds.connectionInfo(_linked_node+'.inputGeometry', sfd=True)
                    _linked_shape = _linked_shape_attr.split('.')[0]
                    _shape_to_grm_info_list.append({'EACH_linked_GRM':_linked_node, 'EACH_linked_SHAPE':_linked_shape})

                    self.get_attr_info_fromNode('pgYetiGroom', _linked_node)

                elif _node_type == 'objectSet':
                    _SET_EXISTS = True
                    # hair_curve_list = cmds.sets(_linked_node, q=True)
                    # curves_grp = cmds.listRelatives(hair_curve_list[0], p=True)[0]

                    curves_grp_list = self.get_curv_grps_from_curvSet(_linked_node)
                    _curve_info_list.append({'EACH_SET':_linked_node, 'EACH_SET_LIST':curves_grp_list})

                    self.get_attr_info_fromNode('objectSet', _linked_node)
                    # one_curve_shape = cmds.ls(hair_curve_list[0], dag=True, ni=True, shapes=True)
                    self.get_attr_info_fromNode('nurbsCurve', _linked_node)


            linked_material = self.get_linked_material(_y_node)

            linked_imageSearchPath = cmds.getAttr(_y_node+'.imageSearchPath')

            linked_render_density = cmds.getAttr(_y_node+'.renderDensity')

            linked_yeti_variable_dict = self.check_and_get_yVariables(_y_node)

            self.export_json_info[_y_node] = {'ALL_SHAPE':_shape_list, 'GROOM':_groom_list, 'MAT':linked_material,
                                            'ISPATH':linked_imageSearchPath, 'SHAPE2GRM':_shape_to_grm_info_list, 'RDENSTIY':linked_render_density,
                                            'IS_CURVE_VER':_SET_EXISTS, 'SET_WITH_CURVES':_curve_info_list, "YETI_VAR":linked_yeti_variable_dict}






        # make pub path
        #       - one ma file
        #       - one grm file ( multiple groom nodes in one grm file )
        #       - one json file
        self.ma_pub_path_list   = [get_pub_paths(selected_dirpath, cur_assetname,'mb')]
        self.json_pub_path_list = [get_pub_paths(selected_dirpath, cur_assetname, 'json')]
        grm_pub_fullpath        = get_pub_paths(selected_dirpath, cur_assetname, 'grm')
        grm_dir_path            = os.path.dirname(grm_pub_fullpath)
        


        self.dirpath_check_makedirs(self.ma_pub_path_list[0])
        self.dirpath_check_makedirs(self.json_pub_path_list[0])
        self.dirpath_check_makedirs(grm_pub_fullpath)


        self.export_json_info['MA_DATA'] = self.ma_pub_path_list
        self.export_json_info['JSON_DATA'] = self.json_pub_path_list

        ver_from_notes = neon.get_version_info_from_geo()
        pub_ver, dev_ver = neon.get_ver_info(ver_from_notes)
        self.export_json_info['MDL_PUB_VER'] = pub_ver
        self.export_json_info['MDL_DEV_VER'] = dev_ver

        total_pub_grmpath_list = []
        for _y_node, _info_dict in self.export_json_info.items():
            
            if _y_node in ['MA_DATA', 'JSON_DATA', 'MDL_PUB_VER', 'MDL_DEV_VER']:
                continue
            grm_pub_path = '{0}/pub_{1}.grm'.format(grm_dir_path, _y_node)
            grm_pub_ver_path = '{0}/pub_{1}_{2}.grm'.format(grm_dir_path, _y_node, vernum)

            self.export_json_info[_y_node]['GRM_DATA'] = [grm_pub_path, grm_pub_ver_path]
            total_pub_grmpath_list.extend([grm_pub_ver_path])


        
        # self.ma_pub_path_list.pop()
        _main_ma_path = self.ma_pub_path_list[0]
        _basemesh_ma_path = _main_ma_path.replace('.mb', '_basemesh.mb')
        self.ma_pub_path_list.append(_basemesh_ma_path)


        return self.ma_pub_path_list + total_pub_grmpath_list
        
        # self.add_pub_files(all_path)

    def execute(self):
        # self.check_pub_condition()
        cmds.select(self.target)


        # select
        # export grm
        # make list of selected target for exporting ma
        ma_export_tar_list = []
        tar_basemesh_list = []
        tar_curveset_list = []
        tar_texref_list = []
        tar_mat_list = []
        for _y_node, _info_dict in self.export_json_info.items():
            if _y_node in ['MA_DATA', 'JSON_DATA', 'MDL_PUB_VER', 'MDL_DEV_VER']:
                continue

            grm_pub_path = self.export_json_info[_y_node]['GRM_DATA']
            self.export_groom_from_selectedY(_y_node, grm_pub_path[0])


            shape_info_list = self.export_json_info[_y_node]['ALL_SHAPE']
            for _shape_info_dict in shape_info_list:
                tar_basemesh_name = _shape_info_dict['EACH_shape']
                tex_ref_shape = _shape_info_dict['EACH_texRef']
                tar_basemesh_list.append(tar_basemesh_name)
                tar_texref_list.append(tex_ref_shape)

            if self.export_json_info[_y_node]['IS_CURVE_VER'] == True:
                curveset_info_list = self.export_json_info[_y_node]['SET_WITH_CURVES']
                for _curve_grp_info in curveset_info_list:
                    _curve_grp = _curve_grp_info.get('EACH_SET_LIST')
                    tar_curveset_list.extend(_curve_grp)

            assigned_mat = self.export_json_info[_y_node]['MAT']
            tar_mat_list.append(assigned_mat)
        

        ma_export_tar_list = tar_texref_list + tar_mat_list
        ma_basemesh_curve_tar_list = tar_basemesh_list + tar_curveset_list
        





        # export ma
        ma_pub_plist = self.export_json_info['MA_DATA']
        m_pub_path = ma_pub_plist[0]
        m_pub_basemesh_path = ma_pub_plist[1]

        cmds.select(clear=True)
        time.sleep(1)
        cmds.select(ma_export_tar_list)
        cmds.file(m_pub_path, exportSelected = True, type = "mayaBinary", force = True)

        # delete texture reference
        cmds.delete(tar_texref_list)

        cmds.select(clear=True)
        time.sleep(1)
        cmds.select(ma_basemesh_curve_tar_list)
        cmds.file(m_pub_basemesh_path, exportSelected = True, type = "mayaBinary", force = True)




        # export json
        json_pub_plist = self.export_json_info['JSON_DATA']
        j_pub_path = json_pub_plist[0]
        with open(j_pub_path, 'w') as make_file:
            json.dump(self.export_json_info, make_file)

        attr_json_pub_path = j_pub_path.replace('.json', '_attr.json')
        with open(attr_json_pub_path, 'w') as make_file:
            json.dump(self.pub_attr_dict, make_file)










        pub_targets = [m_pub_path]
        
        # self.pub_to_sg(pub_targets, cur_dev_ver=self.cur_vernum)
        # self.finish(m_pub_path)







    