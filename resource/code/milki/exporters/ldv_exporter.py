# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    from importlib import reload
if sys.platform.count("win"):
    import neon
    import win_md.MaterialX as mx
else:
    from maya_md import neon
    import general_md_3x.MaterialX as mx
from general_md_3x import LUCY

import os
import re
import glob
import json
import traceback
import maya.cmds as cmds
import maya.mel as mel

import exporter
reload(exporter)
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
        self.tex_max_count_for_thumb = 100

    def pre_execute(self, targets, options):
        cmds.select(targets)
        print('===== LDV export options =====')
        print(options)
        print('==============================')
        # if options["Publish Anim Shader"] == [] and options['Create Variation'] == ['']:
        #     self._pub_type = "LDV"
        #     self._change_sg_status = True
        # elif options["Publish Anim Shader"] == [] and options['Create Variation'] != ['']:
        #     self._pub_type = "LDV_with_VERSION"
        #     self._variation_name = options['Create Variation'][0]
        #     self._change_sg_status = True
        # else:
        #     self._pub_type = "ANI"
        #     self._change_sg_status = False
        arnold_system_attr = "defaultArnoldRenderOptions.exportAllShadingGroups"
        if cmds.getAttr(arnold_system_attr) == False:
            cmds.setAttr(arnold_system_attr, True)
            
        if options['Create Variation'] == ['']:
            self._pub_type = "LDV"
            self._change_sg_status = True
        elif options['Create Variation'] != ['']:
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
        self.tex_info = {}
        self.tc.clear_jobs()
        self.grp = targets
        self._set_basic_info()
        self.asset_name = targets[0].split('_')[0]
        self.tex_info = tp.get_info(targets)
        self.create_tex_pub_info()
        pub_paths = []
        if self._pub_type == "LDV":
            pub_paths.append(self.get_pub_paths('mb'))
            pub_paths.append(self.get_pub_paths('mtlx'))
        elif self._pub_type == "LDV_with_VERSION":
            pub_paths.append(self.get_pub_paths('mb', self._variation_name))
            pub_paths.append(self.get_pub_paths('mtlx', self._variation_name))
        else:
            pub_paths.append(self.get_pub_paths('mb', 'anim'))
            pub_paths.append(self.get_pub_paths('mtlx', 'anim'))
        self.add_pub_files(pub_paths)
        if self._pub_type == 'ANI':
            self.rename_mat_to_versioning("anim")
        elif self._pub_type == 'LDV_with_VERSION':
            self.rename_mat_to_versioning(self._variation_name)



        texs = []
        _tex_count = 0
        for tex, info in self.tex_info.items():
            _tex_count += 1
            tex_name = ''
            pub_name = info['pub_name']
            file_path = info["path"]
            ext = file_path.split('.')[-1]
            if info['is_udim'] == True:
                tex_name = '{0}.<UDIM>.{1}'.format(pub_name, ext)
            else:
                tex_name = '{0}.{1}'.format(pub_name, ext)

            if _tex_count >= self.tex_max_count_for_thumb:
                continue
            list_item = self.add_pub_file(file_path)
            list_item.set_label_text(tex_name)
        self.start_make_tex_thumb()
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
        if self._arnold_shape_attr_flag == True:
            self.ldv_arnold_attr_info_dict = export_ldv_arnold_attr.get_arnold_attr_dict(self.grp)
            
            
        else:
            pass


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


    def execute(self):
        cmds.select(self.grp)
        self.check_pub_condition()
        if self._arnold_shape_attr_flag == True:
            if self._pub_type == "LDV":
                json_path = self.get_pub_paths('json')
                
            elif self._pub_type == "LDV_with_VERSION":
                json_path = self.get_pub_paths('json', self._variation_name)
            elif self._pub_type == "ANI":
                json_path = self.get_pub_paths('json', "anim")

                
            
            export_ldv_arnold_attr.execute_export(self.ldv_arnold_attr_info_dict, json_path)
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
            cmds.select(self.grp)
            self.pub_mtx()
            look = self.pub_op()
            print('if look is not None, the operator nodes are created successfully. but if it is None, operator does not exist and the unkown nodes exist...')
            print(look)
            pub_files = self.pub_files(look)

            cur_scene_ver = LUCY.get_dev_vernum()
            self.pub_to_sg(pub_files, change_status=self._change_sg_status, cur_dev_ver=cur_scene_ver)
        except Exception as e:
            traceback.print_exc()
            print(str(e))
        finally:
            self.restore_original(look)
            self.finish(pub_files[0])


    def rm_asset(self, name):
        idx = 0
        if self.asset_name in name:
            idx = name.index(self.asset_name) + len(self.asset_name) + 1
        return name[idx:]


    def extract_mat_names(self, roots):
        mats = []
        for root in roots:
            root = self.rm_asset(root)
            if len(root.split('_')) > 1:
                root = root.split('_')[0]
            mats.append(root)
        return mats


    def conv2_short_names(self, binds):
        shorts = []
        for bind in binds:
            first = bind[0]
            last = ''
            for ch in bind:
                if ch.isupper():
                    last = ch.lower()
            if last == '':
                shorts.append(bind)
                continue
            shorts.append(first+last)
        return shorts

    def create_tex_pub_info(self):
        '''
         - make pub texture file basename
            - pub name = pub + dev texture file basename
        '''
        udim_finder = re.compile('\.1\d\d\d\.')
        udim_finder_underbar = re.compile('1\d\d\d\.')
        file_dic = {}
        for tex, info in self.tex_info.items():
            is_udim = info['is_udim']
            file_name = os.path.basename(info['path'])
            if is_udim == True and udim_finder.search(file_name):
                file_name = udim_finder.sub('.', file_name)
            elif is_udim == True and udim_finder_underbar.search(file_name):
                file_name = udim_finder_underbar.sub('.', file_name)
            elif is_udim == True and '.<UDIM>.' in file_name:
                file_name = file_name.replace('.<UDIM>.','.')
            elif is_udim == True and '.<udim>.' in file_name:
                file_name = file_name.replace('.<udim>.','.')
            elif is_udim == True and '<UDIM>.' in file_name:
                file_name = file_name.replace('<UDIM>.','.')
            elif is_udim == True and '<udim>.' in file_name:
                file_name = file_name.replace('<udim>.','.')
            elif is_udim == True and '.<f>.' in file_name:
                file_name = file_name.replace('.<f>.','.')
            elif is_udim == True and '<f>.' in file_name:
                file_name = file_name.replace('<f>.','.')
            file_name, ext = os.path.splitext(file_name)
            pub_tex = 'pub_{0}'.format(file_name)
            info['pub_name'] = pub_tex


    def get_last_ver(self, _root):
        root_dir = '{0}/tex/pub/versions'.format(_root)
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        if os.listdir(root_dir) == []:
            return 'v01'
        re_ex_ver = re.compile(r'v\d+')
        only_ver_name_folder = []
        for _folder in os.listdir(root_dir):
            _check_path = '{0}/{1}'.format(root_dir, _folder)
            if os.path.isdir(_check_path):
                if re_ex_ver.match(_folder):
                    only_ver_name_folder.append(_folder)
        cur_last_num = only_ver_name_folder[-1]
        only_up_num = int(cur_last_num.replace('v', '')) + 1
        only_up_num = str(only_up_num).zfill(2)
        nex_num = 'v{0}'.format(only_up_num)
        return nex_num


    def pub_tex(self):
        udim_finder = re.compile('1\d\d\d')
        udim_finder_2 = re.compile('1\d\d\d\.')
        udim_finder_underbar = re.compile(r'\_\.1\d\d\d\.\w+$')
        full_path = LUCY.get_full_path()
        path_split = full_path.split('/')
        ldv_idx = path_split.index('lookdev')
        root = '/'.join(path_split[:ldv_idx])
        pub_dir = '{0}/texture/pub'.format(root)
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


    def check_dir(self, file_path):
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


    def pub_mtx(self):
        doc = gm.create(self.asset_name)
        pub_path_list = []
        if self._pub_type == "LDV":
            pub_path_list.append(self.get_pub_paths('mtlx'))
        elif self._pub_type == "LDV_with_VERSION":
            pub_path_list.append(self.get_pub_paths('mtlx', self._variation_name))
        else:
            pub_path_list.append(self.get_pub_paths('mtlx', 'anim'))
        for mtlx_path in pub_path_list:
            self.check_dir(mtlx_path)
            mx.writeToXmlFile(doc, mtlx_path)


    def get_mat(self, shd):
        mats = cmds.ls(cmds.listConnections(shd),materials=1)
        return mats[0] if len(mats) > 0 else None


    def pub_op(self):
        try:
            return oc.create(self.grp, self.asset_name)
        except:
            return None


    def pub_files(self, look=None):
        
        
        
        cmds.select(cl=True)
        ass_tars = []
        shading_grps = neon.get_shading_groups_in_hierarchy(self.grp)
        for sg in shading_grps:
            cmds.select(sg, noExpand = True, add=True)
            mat = self.get_mat(sg)
            if mat is None:
                continue
            cmds.select(mat, noExpand = True, add=True)
        for tex in self.tex_info:
            cmds.select(tex, noExpand = True, add=True)
        
        if look == None:
            pass
        else:
            cmds.select(look, noExpand = True, add=True)
        _is_face_assign_ = gm.is_face_assign(self.grp)
        if _is_face_assign_ == False:
            meshes_shd_gpr_pair_dict = {}
            all_shd_grp = neon.get_shading_groups_in_hierarchy(self.grp)
            for shd_grp in all_shd_grp:
                if shd_grp == 'MayaNodeEditorSavedTabsInfo':
                    shd_grp = 'initialShadingGroup'
                meshes_with_shd_grp = cmds.listConnections (shd_grp, source=True, destination=False, shapes=True, t='mesh')
                # print meshes_with_shd_grp
                meshes_shd_gpr_pair_dict[shd_grp] = meshes_with_shd_grp
            all_shape = cmds.ls(self.grp, dagObjects = True, long = True, shapes = True)
            cmds.sets(all_shape, e=True, forceElement='initialShadingGroup')
        
        
        

        pub_paths = []
        if self._pub_type == "LDV":
            ass_pub_path    = self.get_pub_paths("ass")
            pub_paths.append(self.get_pub_paths('mb'))
        elif self._pub_type == "LDV_with_VERSION":
            ass_pub_path    = self.get_pub_paths("ass", self._variation_name)
            pub_paths.append(self.get_pub_paths('mb', self._variation_name))
        else:
            ass_pub_path    = self.get_pub_paths("ass", 'anim')
            pub_paths.append(self.get_pub_paths('mb', 'anim'))


        ass_tars        = cmds.ls(sl=True)
        # ass_opt_list    = ['option', 'shape', 'shader', 'override', 'driver', 'filter', 'colorManager', 'operators']
        ass_opt_list    = ['option', 'shader', 'override', 'driver', 'filter', 'colorManager', 'operators']
        # ass_opt_list    = ['option', 'shader', 'driver', 'filter', 'colorManager', 'operators']
        # ass_opt_list    = ['shader', 'operators']
        neon.export_ass_v02(ass_pub_path, ass_tars, ass_opt_list)
        

        cmds.select(cl=True)
        cmds.select(ass_tars, add=True, ne=True)
        # for i in ass_tars:
        #     print(77777777777777777777777)
        #     print(i)

        for pub_path in pub_paths:
            self.check_dir(pub_path)
            try:
                # mel.eval(f"file -op \"v=0;\" -typ \"mayaBinary\" -pr -es \"{pub_path}\";")
                cmds.file(pub_path, exportSelected = True, type = "mayaBinary", force = True, options='v=0',preserveReferences=True)
                # cmds.file(pub_path, op="v=0;", pr=True, exportSelected = True, type = "mayaBinary", force = True)
            except:
                try:
                    self.clean_file_py()
                    # mel.eval(f"file -op \"v=0;\" -typ \"mayaBinary\" -pr -es \"{pub_path}\";")
                    cmds.file(pub_path, exportSelected = True, type = "mayaBinary", force = True, options='v=0',preserveReferences=True)
                    # cmds.file(pub_path, op="v=0;", pr=True, exportSelected = True, type = "mayaBinary", force = True)
                except:
                    error_msg = '===============================================\n\
                                       There are unkown nodes or something...\n\
                                        please \'Optimize Scene Size\'  \n\
                        [File]-[optimize scene size option]-[click unknown nodes option]-[optimize]\n\
                        !!!try clean up mel scrip manually\
                                        ==============================================='
                    # raise Exception(error_msg)
                    cmds.confirmDialog(backgroundColor=[0, 0, 0], title = 'ldv step error', message = error_msg)

        if _is_face_assign_ == False:
            for shd_grp in meshes_shd_gpr_pair_dict:
                meshes_list=meshes_shd_gpr_pair_dict[shd_grp]
                shd_grp_type = cmds.objectType(shd_grp)
                if shd_grp_type in ['MASH_Distribute','polyPlanarProj','polyRetopo', 'polyNormalizeUV', 'polyBevel']:
                    continue
                if meshes_list == None:
                    continue
                else:
                    cmds.sets(meshes_list, e=True, forceElement=shd_grp)

        return [pub_paths[0], ass_pub_path]




    def rename_mat_to_versioning(self, _postfix_name=''):
        self.restore_mat_list = []
        shading_grps = neon.get_shading_groups_in_hierarchy(self.grp)
        if self._pub_type == "LDV_with_VERSION":
            _postfix = _postfix_name
        elif self._pub_type == "ANI":
            _postfix = "anim"
        for sg in shading_grps:
            cmds.select(sg, noExpand = True, add=True)
            mat = self.get_mat(sg)
            if mat is None:
                continue
            try:
                if mat.endswith('_{0}'.format(_postfix)):
                    continue
                
                self.restore_mat_list.append([mat+'_{0}'.format(_postfix), mat])
                cmds.rename(mat, mat+'_{0}'.format(_postfix))
            except Exception as e:
                print(str(e))


    def restore_original(self, look=''):
        for tex, info in self.tex_info.items():
            origin_path = info['path']
            self.change_tex_path(tex, origin_path)
        if look != '':
            cmds.select(look)
            childs = neon.get_all_sources_of_shading(look)
            cmds.select(childs, add = True)
            cmds.delete(cmds.ls(sl=True))
            
        if self._pub_type == 'ANI' or self._pub_type == 'LDV_with_VERSION':            
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
