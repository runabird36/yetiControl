# -*- coding:utf-8 -*-

import sys
import maya.cmds as cmds
import os
if sys.platform.count("win"):
    import neon
    mxPath = "/usersetup/linux/module/win_md"
    if not mxPath in sys.path:
        sys.path.append(mxPath)
    import win_md.MaterialX as mx
    node_def_path = "C:/solidangle/mtoadeploy/2018/materialx/arnold/nodeDefs.mtlx"
    node_def_path_z_drive = "Z:/backstage/modules/solidangle/mtoadeploy/2018/materialx/arnold/nodeDefs.mtlx"
    from_solidagle_folder = 'Z:/backstage/modules/solidangle/mtoadeploy/2018/materialx'
    to_solidagle_folder = 'C:/solidangle/mtoadeploy/2018/materialx'
else:
    from maya_md import neon
    import general_md_3x.MaterialX as mx
    node_def_path = "/usersetup/linux/module/general_md/nodedefs.mtlx"
    node_def_path_z_drive = "/usersetup/backstage/modules/solidangle/mtoadeploy/2018/materialx/arnold/nodedefs.mtlx"
node_defs = mx.createDocument()
try:
    mx.readFromXmlFile(node_defs, node_def_path)
except:
    mx.readFromXmlFile(node_defs, node_def_path_z_drive)
    if not os.path.exists(to_solidagle_folder) and sys.platform.count("win"):
        import shutil
        shutil.copytree(from_solidagle_folder, to_solidagle_folder)


def is_udim(tex):
    node_type = cmds.nodeType(tex)
    tex_path = neon.get_tex_path(tex)
    if tex_path is None:
        return False
    if node_type == "aiImage":
        return "<udim>" in tex_path.lower()
    elif node_type == "file":
        tile_mode = "{0}.{1}".format(tex, "uvTilingMode")
        seq_mode = "{0}.{1}".format(tex, "useFrameExtension")
        if ( cmds.getAttr(tile_mode) == 3 ) or ( cmds.getAttr(tile_mode) == 0 and  cmds.getAttr(seq_mode) == True):
            return True
        return cmds.getAttr(tile_mode) == 3
    return False


def get_tex_path(tex_node):
    attr_list = cmds.listAttr(tex_node)
    if 'fileTextureName' in attr_list:
        return cmds.getAttr(tex_node + '.' + 'fileTextureName')
    elif 'filename' in attr_list:
        return cmds.getAttr(tex_node + '.' + 'filename')


def find_linked_texs(node, texs):
    tex_types = ['file', 'aiImage']
    if neon.get_inputs(node) is None or cmds.nodeType(node) in ['expression']:
        return
    print(node)
    for src in neon.get_sources(node):
        try:
            src_type = cmds.nodeType(src)
            if src_type in tex_types:
                texs.append(src)
        except:
            pass
        find_linked_texs(src, texs)


def get_mat(shd):
    mats = cmds.ls(cmds.listConnections(shd),materials=1)
    return mats[0] if len(mats) > 0 else None


def get_textures(nodeName):
    tex_dic = {}
    tex_types = ['file', 'aiImage']
    source = nodeName
    colors = ['baseColor', 'subsurfaceColor', 'emissionColor']
    node_type = cmds.nodeType(nodeName)
    if node_type == 'aiRaySwitch':
        source = neon.get_source(nodeName, 'camera')
    elif node_type == 'aiLayerShader':
        source = neon.get_source(nodeName, 'input1')
    if cmds.nodeType(source) == 'aiLayerShader':
        source = neon.get_source(source, 'input1')
    for col in colors:
        tex_list = []
        if neon.get_inputs(source) is None:
            continue
        src_node = neon.get_source(source, col)
        if src_node is None:
            continue
        if cmds.nodeType(src_node) in tex_types:
            tex_dic[col] = [src_node]
            continue
        find_linked_texs(src_node, tex_list)
        tex_list = list(set(tex_list))
        if len(tex_list) > 0:
            tex_dic[col] = tex_list
    return tex_dic


def get_geom(sg):
    def replace_splitter(_f_list :list) -> str:
        for _idx, _f in enumerate(_f_list):
            _f_list[_idx] = _f.replace("|", "/")
        
    members = cmds.sets(sg, q=True)
    if members is None:
        return ''
    paths = cmds.listRelatives(members, fullPath=True, allParents=True)
    replace_splitter(paths)
    return ", ".join(paths)


# def get_geom(sg):
#     members = cmds.sets(sg, q=True)
#     if members is None:
#         return ''
#     paths = []
#     for member in members:
#         _IS_ATTRIBUTE = False
#         if '.f' in member:
#             _IS_ATTRIBUTE = True
#         else:
#             _IS_ATTRIBUTE = False
        
#         if _IS_ATTRIBUTE == False:
#             full_path = cmds.listRelatives(member, fullPath=True, allParents=True).pop()
#             paths.append(full_path.replace('|', '/'))
#         else:
#             full_path = cmds.ls(member, l=True).pop()
#             paths.append(full_path.replace('|', '/'))
#     return ", ".join(paths)


def is_face_assign(root :str) -> bool:
    _is_face_assign_ = False
    for sg in neon.get_shading_groups_in_hierarchy(root):
        members = cmds.sets(sg, q=True)
        if members is None:
            return ''
        paths = []
        for member in members:
            _IS_ATTRIBUTE = False
            if '.f' in member:
                _IS_ATTRIBUTE = True
            else:
                _IS_ATTRIBUTE = False
                
            
            if _IS_ATTRIBUTE == True:
                _is_face_assign_ = True
                break
        if _is_face_assign_ == True:
            break
    return _is_face_assign_

def add_texs(geom, tex_dic):
    for ch, texs in tex_dic.items():
        tex = texs.pop()
        tex_name = '{0}_{1}'.format(tex, ch)
        new_attr = geom.addGeomAttr(tex_name)
        new_attr.setValue(get_tex_path(tex))
        is_udim_attr_name = '{0}_udim'.format(tex)
        new_attr_udim = geom.addGeomAttr(is_udim_attr_name)
        new_attr_udim.setValue(is_udim(tex))



def get_basecolor_value(suf):
    _type = cmds.nodeType(suf)
    if _type == 'aiStandardSurface':
        _baseColor = cmds.getAttr(suf+'.baseColor')[0]
        _transparency = cmds.getAttr(suf + '.transmission')
    elif _type == 'surfaceShader':
        _baseColor = cmds.getAttr(suf+'.outColor')[0]
        _transparency = cmds.getAttr(suf + '.outTransparency')[0][0]
    else:
        return {}
    _col_value = _baseColor + tuple([_transparency])
    return {'baseColor':_col_value}


def add_base_mat(geom, suf, color_dict):
    for _attr, _value in color_dict.items():
        mat_name = '{0}_{1}'.format(suf, _attr)
        new_attr = geom.addGeomAttr(mat_name)
        if _attr == 'baseColor':
            new_attr.setValue(mx.Color4(_value[0], _value[1], _value[2], _value[3]))


def get_source_by_nodetype(destination, _type):
    source_list = cmds.listConnections(destination,  s=True, d=False)
    if source_list is None:
        return []
    _res = []
    for _s in source_list:
        if cmds.nodeType(_s) == _type:
            _res.append(_s)
        else:
            _res.extend(get_source_by_nodetype(_s, _type))
    return _res


def create(asset_name):
    if sys.platform.count("win"):
        from_solidagle_folder = 'Z:/backstage/modules/solidangle/mtoadeploy/2018/materialx/arnold/nodeDefs.mtlx'
        to_solidagle_folder = 'C:/solidangle/mtoadeploy/2018/materialx/arnold/nodeDefs.mtlx'
    else:
        from_solidagle_folder = "/usersetup/backstage/modules/solidangle/mtoadeploy/2018/materialx/arnold/nodeDefs.mtlx"
        to_solidagle_folder = "/usersetup/linux/module/general_md/nodedefs.mtlx"
    doc = mx.createDocument()
    try:
        mx.prependXInclude(doc, to_solidagle_folder)
    except:
        mx.prependXInclude(doc, from_solidagle_folder)
        import shutil
        if not os.path.exists(to_solidagle_folder) and sys.platform.count("win"):
            shutil.copytree(from_solidagle_folder, to_solidagle_folder)
    root = cmds.ls(sl=True).pop()
    duplicated_check = []
    for sg in neon.get_shading_groups_in_hierarchy(root):
        suf = neon.get_source(sg, 'surfaceShader')
        # ==================================================
        # This part is updated version
        # This part do consider ani assign shader
        # This part is for swtich node network
        # ==================================================
        if cmds.nodeType(suf) in ['aiSwitch']:
            cur_index = cmds.getAttr(suf+'.index')
            cur_index_mtl = cmds.connectionInfo(suf+'.input'+str(cur_index),  sfd=True)
            suf = cur_index_mtl.split('.')[0]
        if cmds.nodeType(suf) in ['aiLayerShader']:
            cur_index_mtl = cmds.connectionInfo(suf+'.input1',  sfd=True)
            suf = cur_index_mtl.split('.')[0]
            if cmds.nodeType(suf) != 'aiStandardSurface':
                _d_res = get_source_by_nodetype(suf, 'aiStandardSurface')
                if _d_res != []:
                    suf = _d_res[0]
        tex_dic = get_textures(suf)
        if suf in duplicated_check:
            tex_dic = {}
        duplicated_check.append(suf)
        # ==================================================
        # This part is old version
        # This part do not consider ani assign shader
        # ==================================================
        # if len(tex_dic) == 0:
        #     continue
        #
        # geom = doc.addGeomInfo(suf, get_geom(sg))
        # add_texs(geom, tex_dic)
        # ==================================================

        # ==================================================
        # This part is updated version
        # This part do consider ani assign shader
        #       - if there is no texture connected, Store RGB value
        #       - if there is texture, Store texpath value
        # ==================================================
        try:
            if len(tex_dic) == 0:
                color_dict = get_basecolor_value(suf)
                geom = doc.addGeomInfo(suf, get_geom(sg))
                add_base_mat(geom, suf, color_dict)
            else:
                geom = doc.addGeomInfo(suf, get_geom(sg))
                add_texs(geom, tex_dic)
        except Exception as e:
            print(str(e))
    look = doc.addLook("Assignees")
    shds = neon.get_shading_groups_in_hierarchy(root)
    for idx, shd in enumerate(shds):
        name = "ma{0}".format(idx)
        mat = get_mat(shd)
        if mat is None:
            continue
        geom = get_geom(shd)
        if geom == '':
            continue
        mat_assign = look.addMaterialAssign(name, mat)
        mat_assign.setGeom(geom)
    return doc
