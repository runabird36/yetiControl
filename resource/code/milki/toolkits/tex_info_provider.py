# -*- coding:utf-8 -*-

import sys
if sys.platform.count("win"):
    import neon
else:
    from maya_md import neon
import maya.cmds as cmds
grp_shadings =[]


def get_tex_path(tex_node):
    attr_list = cmds.listAttr(tex_node)
    if 'fileTextureName' in attr_list:
        return cmds.getAttr(tex_node + '.' + 'fileTextureName')
    elif 'filename' in attr_list:
        return cmds.getAttr(tex_node + '.' + 'filename')


def get_linked_plugs(src, dst):
    name_idx = -1
    dot = '.'
    linked_plugs = []
    dst_type =cmds.nodeType(dst)
    all_plugs = cmds.listConnections(src, plugs = True)
    for plug in all_plugs:
        plug_type = cmds.nodeType(plug)
        if plug_type != dst_type:
            continue
        plug_name = plug.split(dot)[name_idx]
        linked_plugs.append(plug_name)
        return linked_plugs


def is_exception_node(node):
    except_list = ['default', 'hyperShade', 'maya', 'material']
    for execpt_name in except_list:
        if execpt_name.lower() in node.lower():
            return True
    return False


def get_mat(shd):
    mats = cmds.ls(cmds.listConnections(shd),materials=1)
    return mats[0] if len(mats) > 0 else None


def find_tex_root(node, roots, binds, suf_type, mat_types):
    global grp_shadings
    root_type = 'shadingEngine'
    if neon.get_outputs(node) is None:
        return
    cons = neon.get_destinations(node)
    if cons is None:
        return
    for con in cons:
        # this node is not recognized.
        # when error occur in client computer, and open the scene in self computer.
        # the node disappear...
        if con == 'internal_soloSE':
            continue
        con_type = cmds.objectType(con)
        if is_exception_node(con):
            continue
        if con_type in mat_types:
            if suf_type is None:
                suf_type = con_type
            if suf_type == con_type:
                binds.extend(get_linked_plugs(node, con))
        if cmds.objectType(con) == root_type:
            if 'displacementShader' in get_linked_plugs(node, con):
                binds.append('displacementShader')
            if con in grp_shadings:
                mat = get_mat(con)
                roots.append(mat)
        else:
            find_tex_root(con, roots, binds, suf_type, mat_types)


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


def get_all_mat_types(grp):
    mat_types = []
    for sg in neon.get_shading_groups_in_hierarchy(grp):
        mat = get_mat(sg)
        if sg is None:
            continue
        mat_types.append(cmds.nodeType(mat))
    return list(set(mat_types))


def get_info(grp):
    global grp_shadings
    tex_info = {}
    grp_shadings = neon.get_shading_groups_in_hierarchy(grp)
    texs = cmds.ls(tex=1)
    mat_types = get_all_mat_types(grp)
    file_types = ['file', 'aiImage']
    for tex in texs:
        if not cmds.nodeType(tex) in file_types:
            continue
        roots = []
        binds = []
        find_tex_root(tex, roots, binds, None, mat_types)
        roots = list(set(roots))
        binds = list(set(binds))
        if len(roots) == 0:
            continue
        tex_info[tex] = {}
        tex_info[tex]['roots'] = roots
        tex_info[tex]['binds'] = binds
        tex_info[tex]['path'] = get_tex_path(tex)
        tex_info[tex]['is_udim'] = is_udim(tex)
    return tex_info
