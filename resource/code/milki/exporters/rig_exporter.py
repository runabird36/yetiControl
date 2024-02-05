# -*- coding:utf-8 -*-

import os
import re
import glob
import pickle
import sys
if sys.version_info.major == 3:
    from importlib import reload
if sys.platform.count("win"):
    import neon
    from win_md import MaterialX
else:
    from maya_md import neon
    from general_md_3x import MaterialX
import maya.cmds as cmds


from general_md_3x import LUCY
import exporter
reload (exporter)
from exporter import Exporter
import export_rig_setArnold_attr
reload(export_rig_setArnold_attr)



def get_to_transform_target(ct_name :str) -> str:
    if cmds.nodeType(ct_name) in ["parentConstraint", "pointConstraint"]:
        search_res = cmds.connectionInfo(f"{ct_name}.constraintTranslateX", dfs=True)
    elif cmds.nodeType(ct_name) in ["orientConstraint"]:
        search_res = cmds.connectionInfo(f"{ct_name}.constraintRotateX", dfs=True)
    else:
        return ""
       
    if search_res:
        return search_res[0].split(".")[0]
    else:
        return ""
        

    

def get_from_target(ct_name :str) -> str:
    if cmds.nodeType(ct_name) in ["parentConstraint", "pointConstraint"]:
        search_res = cmds.connectionInfo(f"{ct_name}.target[0].targetTranslate", sfd=True)
    elif cmds.nodeType(ct_name) in ["orientConstraint"]:
        search_res = cmds.connectionInfo(f"{ct_name}.target[0].targetRotate", sfd=True)
    else:
        return ""
        
    if search_res:
        return search_res[0].split(".")[0]
    else:
        return ""
    
    
def get_target_transform_from_loc(loc_name :str) -> dict:
    translate_search = cmds.connectionInfo(f"{loc_name}.translate", dfs=True)
    rotate_search = cmds.connectionInfo(f"{loc_name}.rotate", dfs=True)
    
    if translate_search == None and rotate_search == None:
        return {}
    
    ct_list = []
    for _node in translate_search + rotate_search:
        _node.split(".")[0]
        ct_list.append(_node.split(".")[0])
        
    ct_list = list(set(ct_list))
    
    transform_list = []
    for _ct in ct_list:
        transform_target = get_to_transform_target(_ct)
        transform_list.append(transform_target)

    if transform_list == []:
        return {}
    loc_sn_name = loc_name.split("|")[-1]
    return {
            "LOC":loc_sn_name,
            "TARGET":transform_list
            }




class RigExporter(Exporter):
    pub_paths = []
    target = None
    restore_info_dict = {}

    def __init__(self, m_sg_tk, p_dialog):
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog


        self.ASSET_ANI_FLAG = False



    def pre_execute(self, targets, options):
        self.ma_pub_path_list = []
        self.hichy_pub_path_list = []
        
        self.target = targets
        print('rig export selected target : {0}'.format(self.target))
        self.deformed_re_ex = re.compile('Deformed$|Deformed\w+$|Deform$') # $ : similar with endswith()
                                                                    # \w : all num and all word
                                                                    # \d : all num
                                                                    # + : repeat
                                                                    # | : or
                                                                    # \w+$ : catch 'Deformed1', 'Deformed12', 'Deformedaa'
        
        
        
        assetname = LUCY.get_assetname()

        search_res = cmds.ls(f"{assetname}_keyGRP", l=True)

        self.loc_connection_infos = []
        if search_res:
            tar_loc_list = cmds.listRelatives(search_res[0], c=True, f=True)
            if tar_loc_list:
                for _loc in tar_loc_list:
                    res = get_target_transform_from_loc(_loc)
                    if res == {}:
                        continue
                    self.loc_connection_infos.append(res)

            
        
        
        
        
        
        
        
        
        
        
        self.orig_re_ex = re.compile('Orig$|Orig\w+$')
        # set Arnold attr
        if cmds.pluginInfo("mtoa", query=True, loaded=True):
            try:
                export_rig_setArnold_attr.set_ai_attr(LUCY.get_assetname())
            except Exception as e:
                print(str(e))
        # this part for exporting only target's shading group
        # self.filter_only_export_shd(self.target)
        self._set_basic_info()
        self.ma_pub_path_list.append(self.get_pub_paths('ma'))
        if LUCY.get_pipe_step() == 'animation' and LUCY.get_category() == 'assets':
            self.ASSET_ANI_FLAG = True
            self.hichy_pub_path_list = []
        else:
            self.ASSET_ANI_FLAG = False
            self.hichy_pub_path_list.append(self.get_pub_paths('hichy'))

        all_path = self.ma_pub_path_list + self.hichy_pub_path_list
        
        self.add_pub_files(all_path)


    def execute(self):
        self.check_pub_condition()
        print('execute!')
        # select objectSet
        sel_tar_objectSet_list = cmds.ls("{0}_*".format(LUCY.get_assetname()), type="objectSet")
        cmds.select(clear=True)
        cmds.select(sel_tar_objectSet_list, noExpand=True)
        cmds.select(self.target, add=True)
        ma_idx=0
        ma_pub_path=self.ma_pub_path_list[ma_idx]
        
        # check and make ma folder
        dir_path_ma=os.path.dirname(ma_pub_path)
        if not os.path.exists(dir_path_ma) :
            os.makedirs(dir_path_ma)

        cmds.file(ma_pub_path, type="mayaAscii",force = True, exportSelected=True,preserveReferences=True, expressions=True)
        
        
        # after exporting target's shading group, restore shape and shading group set
        # wich are except
        # this part for cfx geo checker
        # Export hichy ( Shape information )
        if self.ASSET_ANI_FLAG == False:
            hichy_idx=0
            hichy_pub_path = self.hichy_pub_path_list[hichy_idx]
            
            
            
            
            
            dir_path_hichy=os.path.dirname(hichy_pub_path)
            if not os.path.exists(dir_path_hichy):
                os.makedirs(dir_path_hichy)
            with open(hichy_pub_path, "wb") as p:
                pickle.dump(self.loc_connection_infos, p)

        cur_scene_ver = LUCY.get_dev_vernum()
        self.pub_to_sg([ma_pub_path], cur_dev_ver=cur_scene_ver)
        self.finish(ma_pub_path)


    def attatch_preview(self, mtx_full_path = None):
        self.init_preview()
        rig_path = LUCY.get_full_path()
        if mtx_full_path is None:
            mtx_path = self.get_mtx_path(rig_path)
        else:
            mtx_path = mtx_full_path
        if mtx_path is None:
            return
        print('succed to find mtx path')
        geom_info = mx.createDocument()
        mx.readFromXmlFile(geom_info, mtx_path)
        infos =  geom_info.getGeomInfos()
        shaders = []
        for info in infos:
            print(info)
            shd = self.assign_tex(info)
            shaders.append(shd)
        print('succed to attatch texs')
        return shaders


    def assign_basic_shader(self, shapes):
        lam = "lambert1"
        cmds.select(shapes)
        cmds.hyperShade(assign = lam)


    def delete_shd(self, sg):
        mats = cmds.ls(cmds.listConnections(sg),materials=1)
        material = mats[0]
        cmds.delete(neon.get_sources(material))
        cmds.delete(sg)
        cmds.delete(material)


    def init_preview(self):
        for sg in cmds.ls(type='shadingEngine'):
            preview_attr =  cmds.listAttr(sg , string="Preview")
            if preview_attr is None:
                continue
            if not "Preview" in preview_attr:
                continue
            if cmds.getAttr("{0}.Preview".format(sg)) == False:
                continue
            shapes = neon.get_assign_full_paths(sg)
            try:
                self.assign_basic_shader(shapes)
                self.delete_shd(sg)
            except Exception as e:
                print(str(e))
                continue


    def get_mtx_path(self, file_path):
        rig_idx = file_path.find("/rig/")
        if rig_idx < 0 :
            return
        asset_dir = file_path[:rig_idx]
        mtx_dir = asset_dir + "/ldv/pub/mtlx/"
        if not os.path.exists(mtx_dir):
            return
        files = os.listdir(mtx_dir)
        if 'versions' in files:
            files.remove('versions')
        if len(files) > 0:
            return mtx_dir + files[-1]
        else:
            return None


    def assign_tex(self, info):
        name = info.getName()
        suf_name = '{0}_preview'.format(name)
        suf = cmds.shadingNode( 'surfaceShader', n = suf_name, asShader=True )
        sg_name = '{0}_previewSG'.format(name)
        sg = cmds.sets(renderable=True,noSurfaceShader=True,empty=True,n = sg_name)
        cmds.addAttr(sg, longName = "Preview", attributeType = "bool")
        cmds.setAttr("{0}.{1}".format(sg, "Preview"), True)
        cmds.connectAttr( suf + '.outColor', sg + '.surfaceShader')
        for attr in info.getGeomAttrs():
            print(attr)
            name_split = attr.getName().split('_')
            ch = '{0}.outColor'.format(suf)
            _src_attr = cmds.connectionInfo(ch, sfd=True)
            if _src_attr == '':
                pass
            else:
                continue
            tex_name = '_'.join(name_split[:-1])
            if attr.getType() == 'string':
                img_name = "{0}_aiImage".format(tex_name)
                ai_image = cmds.shadingNode( 'aiImage', n = img_name, asTexture=True )
                tex_path = attr.getValue()
                if '<UDIM>' in tex_path:
                    tex_path = tex_path.replace('<UDIM>', '*')
                    globs = glob.glob(tex_path)
                    if len(globs) == 0:
                        continue
                    globs.sort()
                    tex_path = globs.pop(0)
                cmds.setAttr(ai_image + '.filename', tex_path ,type="string")
                out = ai_image + '.outColor'
                cmds.connectAttr(out, ch)
        geoms = info.getGeom().split(', ')
        for geo in geoms:
            if '_ldv_' in geo:
                geo = geo.replace('_ldv_', '_rig_')
            else:
                geo = '{0}/{1}'.format(self.target[0], geo)
            geo_split = geo.split('/')
            while '' in geo_split: geo_split.remove('')
            geo_split.insert(1, 'geo')
            geo = '|'.join(geo_split)
            self.hypershade_shd(geo, suf)
            print('-'* 30)
        return suf


    def shader_exists(self, geo):
        shapes = cmds.ls(geo, dagObjects=True,objectsOnly=True,shapes=True)
        shading_grps = cmds.listConnections(shapes, type='shadingEngine')
        while 'initialShadingGroup' in shading_grps:
            shading_grps.remove('initialShadingGroup')
        return len(shading_grps) > 0


    def hypershade_shd(self, geo, shd):
        try:
            cmds.select(geo + "*")
            if self.shader_exists(geo) == True:
                return
            cmds.hyperShade( assign = shd )
        except:
            try:
                geo = geo.replace('|geo|', '|obj|')
                if self.shader_exists(geo) == True:
                    return
                cmds.select(geo + "*")
                cmds.hyperShade( assign = shd )
            except Exception as e:
                print(str(e))


    def filter_only_export_shd(self, target):
        ''' this part for exporting only target's shading group '''
        shading_grps = neon.get_shading_groups_in_hierarchy(target)
        for shd in shading_grps:
            meshes_with_shd_grp = cmds.listConnections (shd, source=True, destination=False, shapes=True, t='mesh')
            if meshes_with_shd_grp != None:
                for shape in meshes_with_shd_grp:
                    parent_full_path_str = cmds.listRelatives(shape, ap=True, f=True)
                    splited_list = parent_full_path_str[0].split('|')
                    splited_list.remove('')
                    if splited_list[0] == target[0]:
                        continue
                    else:
                        self.restore_info_dict[shape] = shd
                        cmds.sets(shape, e=True, forceElement='initialShadingGroup')
