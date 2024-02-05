# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import json
import traceback
if sys.version_info.major == 3:
    from importlib import reload

from maya_md import neon
from general_md_3x import LUCY
if sys.platform.count("win"):
    mxPath = "/usersetup/linux/module/win_md"
    if not mxPath in sys.path:
        sys.path.append(mxPath)
    import win_md.MaterialX as mx
else:
    import general_md_3x.MaterialX as mx
import maya.cmds as cmds
from maya_md import neon
import exporter
reload (exporter)
from exporter import Exporter
import tex_info_provider as tp
reload (tp)
import geom_info_creator as gm
reload (gm)
import op_creator as oc
reload (oc)
from tex_copier import TexCopier
import export_ldv_arnold_attr
reload(export_ldv_arnold_attr)
import export_ldv_arnold_tx
reload(export_ldv_arnold_tx)

mdPath = "/usersetup/linux/module"
if not mdPath in sys.path:
    sys.path.append(mdPath)
from general_md.GMaterialX import GMaterialX as gmx
reload(gmx)


class LdvExporter(Exporter):
    tex_info = {}
    asset_name = ""
    tc = None
    grp = ""
    cs_RULES_except_list = ['aiCellNoise', 'aiCurvature','aiFlakes','aiNoise','aiThinFilm','aiTriplanar','aiPhysicalSky','aiSky', 'ramp','fractal']
    _arnold_shape_attr_flag = False
    _make_tx_flag = False
    ldv_arnold_attr_info_dict = {}
    tex_pub_dir_path_for_tx = ''
    def __init__(self, m_sg_tk, p_dialog):
        print('reload ldv export')
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog
        self.tc = TexCopier()
        self.ldv_arnold_attr_info_dict = {}
        self.ldv_op_info_dict = {'COL':[], 'PARM':[]}
        self.tex_max_count_for_thumb = 100

    def pre_execute(self, targets, options):
        cmds.select(targets)
        print('===== LDV export options =====')
        print(options)
        print('==============================')
        if options["Publish Anim Shader"] == [] and options['Create Variation'] == ['']:
            self._pub_type = "LDV"
            self._change_sg_status = True
        elif options["Publish Anim Shader"] == [] and options['Create Variation'] != ['']:
            self._pub_type = "LDV_with_VERSION"
            self._variation_name = options['Create Variation'][0]
            self._change_sg_status = True
        else:
            self._pub_type = "ANI"
            self._change_sg_status = False
        print('===== Publish Type =====')
        print(self._pub_type)
        print('==============================')
        all_filenode_list = cmds.ls(textures=True)
        for filenode in all_filenode_list:
            if cmds.nodeType(filenode) in self.cs_RULES_except_list:
                continue
            try:
                cmds.setAttr('{0}.ignoreColorSpaceFileRules'.format(filenode), True)
            except Exception as e:
                print(e)
            try:
                cmds.setAttr('{0}.aiAutoTx'.format(filenode), False)
            except Exception as e:
                print(e)
        self.tc.clear_jobs()
        self.tex_info = {}
        self.tex_info = tp.get_info(targets)
        self.grp = targets
        self._set_basic_info()
        self.asset_name = targets[0].split('_')[0]
        # Default Shader Pub / Variation Shader Pub
        pub_paths = []
        if self._pub_type == "LDV" or self._pub_type == "LDV_with_VERSION":
            pub_paths.append(self.get_pub_paths('mtlx'))
        # Anim Shader Pub
        else:
            pub_paths.append(self.get_pub_paths('ma', 'anim'))
            pub_paths.append(self.get_pub_paths('mtlx', 'anim'))
        self.add_pub_files(pub_paths)
        # Anim Shader Pub
        if self._pub_type == 'ANI' or self._pub_type == 'LDV_with_VERSION':
            self.rename_mat_to_versioning()
        if options['Bake TX'] == []:
            self._make_tx_flag = False
        else:
            self._make_tx_flag = True
        if options['Arnold Attribute of GEOShape'] == []:
            self._arnold_shape_attr_flag = False
        else:
            self._arnold_shape_attr_flag = True
        if options['Pub & Copy Texture file'] == []:
            self._pub_tex_flag = False
        else:
            self._pub_tex_flag = True
        if self._make_tx_flag == True:
            pass
        else:
            pass
        self._arnold_shape_attr_flag = True
        # check need to update exporting arnold shape setting by mayapy.exe
        if self._arnold_shape_attr_flag == True:
            self.ldv_arnold_attr_info_dict = export_ldv_arnold_attr.get_arnold_attr_dict_v02(self.grp)
        #======================================================================
        #All COLLECTION
        #======================================================================
        end_names = []
        for shp in neon.get_all_shape_in_hierarchy(targets[0]):
            end_name = "*{0}*".format(shp.split("|")[-1])
            if '_GEOShapeDeform' in end_name:
                end_name = end_name.replace('_GEOShapeDeform','_GEOShape')
            end_names.append(end_name)
        all_path = " or ".join(end_names)
        self.ldv_op_info_dict['COL'].append({
                                            'Node_Name' : '{0}_all'.format(self.asset_name),
                                            'Selection_String' : all_path,
                                            'Op_Value' : '{0}All'.format(self.asset_name)
                                            })
        #======================================================================
        #SHADING NETWORK
        #======================================================================
        for shadingGroup in neon.get_shading_groups_in_hierarchy(targets[0]):
            shaderName = neon.get_source(shadingGroup, 'surfaceShader')
            dispName = neon.get_source(shadingGroup, 'displacementShader')
            full_paths = []
            for fp in neon.get_assign_full_paths(shadingGroup):
                end_name = "*{0}*".format(fp.split("|")[-1])
                if '_GEOShapeDeform' in end_name:
                    end_name = end_name.replace('_GEOShapeDeform','_GEOShape')

                full_paths.append(end_name)
            print(full_paths)
            selection_paths = " or ".join(full_paths)
            # Get collection info : shadername - shape list
            # Get dismap shader
            shdAssign = []
            if not dispName == None:
                self.ldv_op_info_dict['COL'].append({
                                            'Node_Name' : '{0}'.format(shaderName),
                                            'Selection_String' : selection_paths,
                                            'Op_Value' : shaderName
                                            })
                shdAssign.append('disp_map = ' '\"' + dispName + '.displacement' + '\"')
                self.ldv_op_info_dict['PARM'].append({'Node_Name' : '{0}_shdAssign'.format(shaderName),
                                                      'Selection_String' : '#' + shaderName,
                                                      'Op_Value' : shdAssign})


    def execute(self):
        cmds.select(self.grp)
        self.check_pub_condition()
        if self._arnold_shape_attr_flag == True:
            json_pub_full_path = self.get_arnold_attr_json_path()
            export_ldv_arnold_attr.execute_export(self.ldv_arnold_attr_info_dict, json_pub_full_path)
        if self.tex_info and self._pub_tex_flag == True:
            print('pub with starting copy textures')
            self.pub_tex()
            self.tc.all_complete.connect(self.post_excute)
            self.tc.start_copy()
        else:
            print('pub only material.(Case : without textures in maya scene)')
            self.post_excute()


    def post_excute(self):
        look = ''
        if self._make_tx_flag == True:
            print('Bake tx !!!')
            bake_target_path_list = []
            for tex_info_dict in self.tc.job_infos:
                pub_tex_full_path = tex_info_dict['dst']
                pub_tex_file_node = tex_info_dict['tex']
                if '\\' in pub_tex_full_path:
                    pub_tex_full_path = pub_tex_full_path.replace('\\','/')
                bake_target_path_list.append([pub_tex_full_path,pub_tex_file_node])
            export_ldv_arnold_tx.maketx_with_cmd(bake_target_path_list)
        try:
            cmds.select(clear=True)
            cmds.select(self.grp)
            pub_file = self.pub_mtx()
            self.pub_op_v02()
            self.restore_mat_list = []
            self.pub_to_sg([pub_file], change_status=self._change_sg_status)
        except Exception as e:
            traceback.print_exc()
            print(str(e))
        finally:
            self.restore_original(look)
            self.finish(pub_file)


    def check_dir(self, file_path):
        if isinstance(file_path, list):
            for _path in file_path:
                dir_path = os.path.dirname(_path)
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
        else:
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)


    def pub_mtx(self):
        pub_path_list = []
        if self._pub_type == "LDV" or self._pub_type == "LDV_with_VERSION":
            pub_path_list.append(self.get_pub_paths('mtlx'))
            if self._pub_type == "LDV":
                _look_name = "default"
            elif self._pub_type == "LDV_with_VERSION":  
                _look_name = self._variation_name
            self.check_dir(pub_path_list)
            
            # ======================Case 01 : export with original maya materialx exporter ================================
            # mtlx_pub_path = neon.export_materialX(self.grp, pub_path_list[0], lookName=_look_name)
            # print(mtlx_pub_path)
            # mtlx_pub_doc = gmx.read_docs(mtlx_pub_path)
            # print(mtlx_pub_doc)
            # ======================Case 02 : export shader and make materialX manually ================================
            mtlx_pub_path = pub_path_list[0]
            doc = gm.create(self.asset_name)
            mx.writeToXmlFile(doc, mtlx_pub_path)
            mtlx_pub_doc = gmx.read_docs(mtlx_pub_path)
            # ==================================================================================================
            gmx.add_star_in_shape(mtlx_pub_doc, _look_name)
            gmx.write_docs(mtlx_pub_doc, mtlx_pub_path)
        elif self._pub_type == "ANI":
            doc = gm.create(self.asset_name)
            pub_path_list.append(self.get_pub_paths('mtlx', 'anim'))
            for mtlx_path in pub_path_list:
                self.check_dir(mtlx_path)
                mx.writeToXmlFile(doc, mtlx_path)
        return pub_path_list[0]


    def get_mat(self, shd):
        mats = cmds.ls(cmds.listConnections(shd),materials=1)
        return mats[0] if len(mats) > 0 else None


    def pub_op(self):
        try:
            return oc.create(self.grp, self.asset_name)
        except:
            return None
        
        
    def pub_op_v02(self):
        _op_path = self.get_pub_paths('operator')
        _op_path = _op_path.replace('.operator', '.json')
        _op_dir_path = os.path.dirname(_op_path)
        if not os.path.exists(_op_dir_path):
            os.makedirs(_op_dir_path)
        with open(_op_path, 'w') as make_file:
            json.dump(self.ldv_op_info_dict, make_file)


    def pub_maya_files(self, look=None):
        cmds.select(cl=True)
        shading_grps = neon.get_shading_groups_in_hierarchy(self.grp)
        for sg in shading_grps:
            cmds.select(sg, noExpand = True, add=True)
            mat = self.get_mat(sg)
            if mat is None:
                continue
            cmds.select(mat, add=True)
        for tex in self.tex_info:
            cmds.select(tex, add=True)
        if look == None:
            pass
        else:
            cmds.select(look, add=True)
        pub_paths = []
        if self._pub_type == "LDV":
            pub_paths.append(self.get_pub_paths('ma'))
        elif self._pub_type == "LDV_with_VERSION":
            pub_paths.append(self.get_pub_paths('ma', self._variation_name))
        else:
            pub_paths.append(self.get_pub_paths('ma', 'anim'))
        for pub_path in pub_paths:
            self.check_dir(pub_path)
            try:
                cmds.file(pub_path, exportSelected = True, type = "mayaAscii", force = True)
            except:
                try:
                    self.clean_file_py()
                    cmds.file(pub_path, exportSelected = True, type = "mayaAscii", force = True)
                except:
                    error_msg = '===============================================\n\
                                       There are unkown nodes or something...\n\
                                        please \'Optimize Scene Size\'  \n\
                        [File]-[optimize scene size option]-[click unknown nodes option]-[optimize]\n\
                        !!!try clean up mel scrip manually\
                                        ==============================================='
                    # raise Exception(error_msg)
                    cmds.confirmDialog(backgroundColor=[0, 0, 0], title = 'ldv step error', message = error_msg)
        return pub_paths[0]


    def rename_mat_to_versioning(self):
        shading_grps = neon.get_shading_groups_in_hierarchy(self.grp)
        if self._pub_type == "LDV_with_VERSION":
            _postfix = self._variation_name
        elif self._pub_type == "ANI":
            _postfix = "anim"
        for sg in shading_grps:
            cmds.select(sg, noExpand = True, add=True)
            mat = self.get_mat(sg)
            if mat is None:
                continue
            try:
                cmds.rename(mat, mat+'_{0}'.format(_postfix))
                self.restore_mat_list.append([mat+'_{0}'.format(_postfix), mat])
            except Exception as e:
                print(str(e))


    def change_tex_path(self, tex_node, path, is_udim = False):
        attr_list = cmds.listAttr(tex_node)
        tex_attr= ''
        if 'fileTextureName' in attr_list:
            tex_attr = tex_node + '.' + 'fileTextureName'
        elif 'filename' in attr_list:
            tex_attr = tex_node + '.' + 'filename'
        if is_udim == True:
            path_splits = path.split('.')
            path_splits[-2] = '<UDIM>'
            path = '.'.join(path_splits)
        cmds.setAttr(tex_attr, path, type = "string")


    def restore_original(self, look=''):
        for tex, info in self.tex_info.items():
            origin_path = info['path']
            self.change_tex_path(tex, origin_path)
        if look != '' and look is not None:
            cmds.select(look)
            childs = neon.get_all_sources_of_shading(look)
            cmds.select(childs, add = True)
            cmds.delete(cmds.ls(sl=True))
        if self.restore_mat_list:
            for _renamed_mat in self.restore_mat_list:
                try:
                    renamed_name = _renamed_mat[0]
                    original_name = _renamed_mat[1]
                    cmds.rename(renamed_name, original_name)
                except Exception as e:
                    print(str(e))
        self._arnold_shape_attr_flag = False
        self.ldv_arnold_attr_info_dict = {}


    def read_json(self, write_json_path):
        with open(write_json_path, 'r') as f:
            json_data_from_file = json.load(f)
        return json_data_from_file


def pub_tex(self):
        udim_finder = re.compile('1\d\d\d')
        udim_finder_2 = re.compile('1\d\d\d\.')
        udim_finder_underbar = re.compile(r'\_\.1\d\d\d\.\w+$')
        full_path = LUCY.get_full_path()
        path_split = full_path.split('/')
        ldv_idx = path_split.index('ldv')
        root = '/'.join(path_split[:ldv_idx])
        pub_dir = '{0}/tex/pub'.format(root)
        if not os.path.exists(pub_dir):
            os.makedirs(pub_dir)
        for tex, info in self.tex_info.items():
            is_udim = info['is_udim']
            src = info['path']
            if '<UDIM>' in src:
                src = src.replace('<UDIM>', '*')
            elif '<udim>' in src:
                src = src.replace('<udim>', '*')
            elif '####' in src:
                src = src.replace('####', '*')
            elif '<f>' in src:
                src = src.replace('<f>', '*')
            udim = udim_finder_2.search(src)
            if is_udim and not udim is None:
                src = src.replace(udim.group(), '*.')
            print('after : {0}'.format(src))
            src_files = []
            bucket = glob.glob(src)
            for src_file in bucket:
                if src_file in src_files:
                    continue
                file_name = os.path.basename(src_file)
                udim = udim_finder.search(file_name)
                pub_name = info['pub_name']
                if '####' in pub_name:
                    sharp_num = udim_finder.search(src_file)
                    sharp_num = sharp_num.group()
                    pub_name = pub_name.replace('####', sharp_num)
                if is_udim and not udim is None:
                    udim = udim.group()
                    pub_name = '{0}.{1}'.format(pub_name, udim)
                ext = file_name.split('.')[-1]
                pub_file = '{0}.{1}'.format(pub_name, ext)
                pub_path = '{0}/{1}'.format(pub_dir, pub_file)
                print('after 2: {0}'.format(pub_path))
                src_files.append(src_file)
                self.tc.add_job(src_file, pub_path, tex, is_udim)
