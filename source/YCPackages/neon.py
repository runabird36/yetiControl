
import maya.cmds as cmds
import maya.mel as mel

import pprint, re, os

all_source_nodes = []
node_set = set()
num_re_ex = re.compile('\_\d{3}$')
num_re_ex_2 = re.compile('\d+')

def get_all_shape_in_hierarchy(grp=None):
    if grp is None:
        grp = cmds.ls(sl=True)[0]
    return cmds.listRelatives(grp, ad=True, f=True, typ = 'shape')

def get_shading_engines(shape):
    connected_list = cmds.listConnections (shape, source=False, destination=True)
    result_shading_engine_list = []
    if connected_list == None:
        return None
    else:
        for node in connected_list:
            node_type = cmds.nodeType(node)
            if node_type == 'shadingEngine':
                result_shading_engine_list.append(node)
        return result_shading_engine_list

def get_shading_groups_in_hierarchy(grp):
    shading_engine_list = []

    for shape in get_all_shape_in_hierarchy(grp):
        shading_engines = get_shading_engines(shape)
        if not shading_engines == None:
            check_engines_list = shading_engines
            while 'initialShadingGroup' in check_engines_list:
                shading_engines.remove('initialShadingGroup')
            if not shading_engines:
                continue
            else:
                for _shadinggroup in shading_engines:
                    if not _shadinggroup in shading_engine_list:
                        shading_engine_list.append(_shadinggroup)
    return shading_engine_list

def get_inputs(destination):
    input_list = []
    try:
        source_nodes = cmds.listConnections(destination, c=True, s=True, d=False)
    except:
        return

    if source_nodes is None:
        return

    source_nodes = source_nodes[::2]

    for node_name in source_nodes:
        input_name = node_name.split('.')[1]
        if 'message' in input_name:
            continue
        input_list.append(input_name)

    input_list = list(set(input_list))
    return input_list

def get_source(destination, input_name):
    source_name = None
    for in_name in get_inputs(destination):
        if in_name == input_name:
            source = cmds.connectionInfo( destination + '.' + in_name, sfd = True)
            source_name = source.split('.')[0]

    return source_name

def get_sources(destination):
    inputs = get_inputs(destination)
    sources = []
    for in_node in inputs:
        src = get_source(destination, in_node)
        if 'ShapeDeform' in src:
            continue
        sources.append(get_source(destination, in_node))

    sources = list(set(sources))
    return sources

def get_outputs(source):
    output_list = []
    try:
        dst_nodes = cmds.listConnections(source, c=True, s=False, d=True)
    except:
        return
    if dst_nodes is None:
        return
    dst_nodes = dst_nodes[::2]
    for node_name in dst_nodes:
        output_name = node_name.split('.')[1]
        if 'message' in output_name:
            continue
        output_list.append(output_name)

    output_list = set(list(output_list))
    return output_list

def get_destinations(source):
    destinations = []
    dst_nodes = []

    for output_name in get_outputs(source):
        dst = cmds.connectionInfo( source + '.' + output_name, dfs = True)
        dst_nodes.extend(dst)

    for dst in dst_nodes:
        destinations.append(dst.split('.')[0])

    return destinations

def get_assign_full_paths(shading_group):
    assignment_path_list = []

    assignment_path_temp = cmds.listConnections (shading_group, source=True, destination=False, sh=True, t='mesh')
    if assignment_path_temp is None:
        return

    for assignement in assignment_path_temp:
        assignment_path_list.append(cmds.listRelatives(assignement, f=True, ap=True)[0])

    return assignment_path_list

def _recursive_source_search(shd):
    global all_source_nodes, node_set

    if get_inputs(shd) is None:
        return

    if shd in node_set:
        return
    node_set.add(shd)
    sources = get_sources(shd)

    if len(sources) == 0:
        return

    for src in sources:
        if 'defaultColorMgtGlobals' in src:
            continue

        if 'initialShadingGroup' in src:
            continue

        if 'lambert1' in src:
            continue

        if '' in src:
            continue

        if cmds.objectType(src) in ['mesh', 'reference']:
            continue
        all_source_nodes.append(src)
        _recursive_source_search(src)

def get_all_sources_of_shading(shd):
    global all_source_nodes, node_set
    node_set.clear()
    all_source_nodes = []
    _recursive_source_search(shd)
    all_source_nodes = list(set(all_source_nodes))
    return all_source_nodes

def get_all_nodes_in_hierarchy(grp):
    nodes = []

    shadings = get_shading_groups_in_hierarchy(grp)
    for shading in shadings:
        nodes.append(shading)
        all_src = get_all_sources_of_shading(shading)
        nodes.extend(all_src[:])
    nodes = list(set(nodes))
    return nodes



def get_all_exacttype_sources_of_shading(shd, _type):

    _pair_info = {}

    connected_node_list = cmds.listConnections(shd, s=True, p=True, c=True, d=False)
    if connected_node_list is None:
        return {}
    for _idx in range(len(connected_node_list)/2):
        from_node = connected_node_list[_idx*2]
        to_node = connected_node_list[_idx*2+1]

        all_children = cmds.listHistory(to_node)
        all_exact_type_children = cmds.ls(all_children, type=_type)

        _pair_info[from_node] = all_exact_type_children

    return _pair_info



def get_all_RNs():
    '''
    return value : [u'SWT_0040_mmv_camRN', u'hair_mesh_v03RN', u'vampLordAwakenNew_001:publish_vampLordAwakenNew_mdl_asset01_hiRN', u'vampLordAwakenNew_001RN']
    '''
    return cmds.ls(references = True)

def get_all_reference_file_name():
    '''
    return value : [u'SWT_0040_mmv_cam.abc', u'hair_mesh_v03.mb', u'publish_vampLordAwakenNew_mdl_asset01_hi.ma', u'publish_vampLordAwakenNew_rig_asset01_hi.ma']
    '''
    all_ref = get_all_RNs()
    _err_list = []
    ref_file_shortnames_list = []
    for reference in all_ref:
        try:
            ref_file_short_name = cmds.referenceQuery(reference, filename=True, shortName=True)
        except Exception as e:
            print(str(e))
            _err_list.append(reference)
            cmds.lockNode(reference, l=False)
            cmds.delete(reference)
            continue
        ref_file_shortnames_list.append(ref_file_short_name)
    if _err_list != []:
        print('='*50)
        pprint.pprint(_err_list)
        print('='*50)
    return ref_file_shortnames_list

def replace_reference(path: str, tar_ns: str):
    cmds.file(path, loadReference=tar_ns)

def remove_reference(path: str):
    cmds.file(path, removeReference=True)

def get_all_namespaces():
    '''
    return value : [u'SWT_0040_mmv_cam', u'hair_mesh_v03', u'vampLordAwakenNew_001']
    '''
    ref_list = get_all_RNs()
    cache_list = []
    for ref in ref_list:
        if ref.find(':') < 0:
            ref = ref.replace('RN','')
            cache_list.append(ref)
        else:
            ref_splited_list = ref.split(':')
            cache_list.append(ref_splited_list[0])
    return list(set(cache_list))


def ns_exists(ns_name: str):
    return cmds.namespace( exists=ns_name )

def get_start_time():
    return cmds.playbackOptions(q=True, min=True)

def get_end_time():
    return cmds.playbackOptions(q=True, max=True)

def get_start_frame():
    return cmds.getAttr ("defaultRenderGlobals.startFrame")

def get_end_frame():
    return cmds.getAttr ("defaultRenderGlobals.endFrame")

def get_RN_file(rn_name):
    '''
    get reference filename with format
    parameter : vampLordAwakenNew_v001(str)
    return : 1(int)
    '''
    return cmds.referenceQuery(rn_name, filename=True, shortName=True)

def get_RN_path(rn_name):
    '''
    get full path of reference file
    parameter : vampLordAwakenNew_v001(str)
    return : 1(int)
    '''
    return cmds.referenceQuery(rn_name, filename=True)

def get_RN_version(rn_name):
    '''
    get reference name version
    parameter : vampLordAwakenNew_v001(str)
    return : '/usersetup/pipeline/playground/tools/milki/branches/taiyeong/scene_data/projects/projectName/2018_11_kakako/asset/char/vampLordAwakenNew/mdl/pub/ma/publish_vampLordAwakenNew_mdl_asset01_v20.ma'(str)
    '''
    version_finder = re.compile('v\d+')
    find_result=version_finder.search(rn_name)
    if find_result is None:
        return None

    version_num=find_result.group()
    try:
        version_num = int(version_num[1:])
    except:
        return None
    return version_num

def select_asset(asset_name):
    '''parameter : asset_name(str)'''
    '''return : None'''
    '''make root grp selected in hier'''
    cmds.select(asset_name+"*", hi= True)


def get_all_roots():
    '''make all root selected except orthographic cameras'''
    all_root = cmds.ls(assemblies = True)
    all_ortho_cam = cmds.listCameras(orthographic=True)
    only_asset_root = set(all_root)-set(all_ortho_cam)
    return list(only_asset_root)


def select_all_root():
    '''make all root selected'''
    all_root_asset=get_all_roots()
    cmds.select(all_root_asset)

def get_tex_path(tex_node):
    attr_list = cmds.listAttr(tex_node)
    if 'fileTextureName' in attr_list:
        return cmds.getAttr(tex_node + '.' + 'fileTextureName')
    elif 'filename' in attr_list:
        return cmds.getAttr(tex_node + '.' + 'filename')

def get_fps_info():
    cur_fps = cmds.currentUnit(q=True, time=True)
    fps_lsit = ['game', 'film', 'pal', 'ntsc', 'show', 'palf', 'ntscf']
    if cur_fps in fps_lsit:
        fps_dict = {'game': '15 fps', 'film':'24 fps', 'pal':'25 fps', 'ntsc':'30 fps', 'show':'48 fps', 'palf':'50 fps', 'ntscf':'60 fps'}
        return fps_dict[cur_fps]
    else:
        return cur_fps

def get_abcFullpath_from_alembicNode(connected_geo):
    if cmds.nodeType(connected_geo) == 'transform':
        connected_geo = cmds.listRelatives(connected_geo ,ad=True, ni=True, typ='mesh', f=True)
    connected_abc = cmds.listConnections(connected_geo, d=True, type='AlembicNode')
    if connected_abc == None:
        return ''
    connected_abc = list(set(connected_abc))
    connected_abc = connected_abc[0]

    abc_file_attr = '{0}.abc_File'.format(connected_abc)
    abc_file_path = cmds.getAttr(abc_file_attr)

    return abc_file_path

def _get_assetnum_from_assetGRP(connected_geo):
    abc_file_path = get_abcFullpath_from_alembicNode(connected_geo)
    if len(abc_file_path.split('_')):
        asset_name = connected_geo.split('_')[0]
        attr_value = '{0}_{1}'.format(asset_name, "001")
        if num_re_ex.search(attr_value):
            return attr_value
        else:
            return ""
    file_name = os.path.basename(abc_file_path)
    file_name = file_name.split('.')[0]
    asset_num = file_name.split('_')[-1]
    asset_name = file_name.split('_')[-2]

    attr_value = '{0}_{1}'.format(asset_name, asset_num)
    if num_re_ex.search(attr_value):
        return attr_value
    else:
        return ''


def get_aniNS_from_geo(shape_or_transform):
    ''' This function to get namespace which set in animation step
                1. query Asset_number attr made in animation pub process
                2. query alembic node wiche linked with geo '''
    connected_geo = shape_or_transform
    assetnum_attr = '{0}.Asset_number'.format(connected_geo)
    try:
        asset_namespace = cmds.getAttr(assetnum_attr)

        if num_re_ex_2.search(asset_namespace):
            return asset_namespace
        elif not num_re_ex.search(asset_namespace):
            asset_namespace = _get_assetnum_from_assetGRP(connected_geo)
    except Exception as e:
        print(str(e))
        asset_namespace = _get_assetnum_from_assetGRP(connected_geo)
    return asset_namespace

def convert2_maya_color(color_code_list):
    converted_code = []
    for _code_num in color_code_list:
        converted_code.append(_code_num/256.0)
    return converted_code

def copyAttr(from_tar, to_tar):
    '''
    There is cmds.copyAttr() in maya
    But, the cmds.copyAttr() does not support with mesh target
    Thus, In mesh case, we need to use this function
    '''
    _attr_list = cmds.listAttr(from_tar)
    for _attr in _attr_list:
        try:
            _attr_value = cmds.getAttr(from_tar+'.'+_attr)
        except Exception as e:
            print(str(e))
            continue

        try:
            if isinstance(_attr_value, int) or isinstance(_attr_value, bool) or isinstance(_attr_value, float):
                cmds.setAttr(to_tar+'.'+_attr, _attr_value)
            elif isinstance(_attr_value, str):
                cmds.setAttr(to_tar+'.'+_attr, _attr_value, typ='string')
            else:
                continue
        except Exception as e:
            print(str(e))

def get_next_available_idx(node_name):
    return mel.eval("getNextFreeMultiIndex(\"{0}.aiFilters\", 0)".format(node_name))

def get_next_available_attr(node_name, attrname):
    return int(mel.eval("getNextFreeMultiIndex(\"{0}.{1}\", 0)".format(node_name, attrname)))


def del_exists_child_nodeTree(p_nodename, p_attrname):
    
    connected_node_list = cmds.listConnections(p_nodename + "."+ p_attrname, destination=True)
    
    if connected_node_list:
        attr_range = len(connected_node_list)
        cmds.delete(connected_node_list)
    else:
        attr_range = 0
    for _idx in range(attr_range):
        cmds.removeMultiInstance("{0}.{1}[{2}]".format(p_nodename, p_attrname, str(_idx)))
        
        

def is_connected(from_attr_fullname, to_attr_fullname):
    list_cons = cmds.listConnections(to_attr_fullname, destination=True, p=True)
    
    if list_cons != None:
        if from_attr_fullname in list_cons:
            return True
    return False

def connect_attr(from_attrname, to_attrname, to_idx=""):
    if cmds.ls(from_attrname) == [] or cmds.ls(to_attrname.split('.')[0]) == []:
        return
    if is_connected(from_attrname, to_attrname) == True:
        return
    try:
        if to_idx != "":
            if not isinstance(to_idx, str):
                to_idx = str(to_idx)
            to_attrname = to_attrname+"[{0}]".format(to_idx)
        cmds.connectAttr(from_attrname, to_attrname, f=True)
    except Exception as e:
        print(str(e))

def create_gpu_cache(input_name, full_path, geompath='|'):
    '''
    Use this method to create gpu cache
    Because, when we use 'createNode -n "mine" gpuCache;' to create gpu cache,
    there is only gpu node whoes name changed, not transform node name

    # ==================================================================
    # Mel script reference
    # ==================================================================
    # createNode -n "mine" gpuCache;
    # setAttr -e -type "string" mine.cacheFileName "dd.abc";
    # setAttr -e -type "string" mine.cacheGeomPath "|"; // eg the root.

    '''

    created_node = cmds.createNode("gpuCache", n=input_name+'Shape')
    transform_node = cmds.listRelatives(created_node, p=True)[0]
    created_transform_node = cmds.rename(transform_node, input_name)

    filepath_attr = '{0}.cacheFileName'.format(created_node)
    geompath_attr = '{0}.cacheGeomPath'.format(created_node)

    try:
        cmds.setAttr(filepath_attr, full_path, typ='string', e=True)
        cmds.setAttr(geompath_attr, geompath, typ='string', e=True)
    except Exception as e:
        print(str(e))

    return created_node






def _get_masks(options):
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
        '''

        2020-07-27 updated

        255 is from the old days, before operators and color managers
            Options = 1
            Camera = 2
            Light = 4
            Shape = 8
            Shader = 16
            Override = 32
            Driver = 64
            Filter = 128
            Color Manager = 2048
            Operators = 4096

        comment 1 : if there is no color manager, render output is not same with original render

        comment 2 : there is also Operators option, but, we have operator tool, thus we can control operator in there
                    not with ass option

        '''

        optionDict = {'option' : 0x0001
                      , 'camera' : 0x0002
                      , 'light' : 0x0004
                      , 'shape' : 0x0008
                      , 'shader' : 0x0010
                      , 'override' : 0x0020
                      , 'driver' : 0x0040
                      , 'filter' : 0x0080
                      , 'colorManager' : 0b100000000000
                      }

        mask = 0
        for option in options:
            try:
                mask += optionDict[option]

            except:
                pass
        return str(mask)

def export_ass(export_fullpath, sel_tar, _options_list, frame_info=[], full_path=True, shadow_link=False, light_link=False, get_only_mel=False):
    
    #create selection command
    cmds.select(clear=True)
    cmds.select(sel_tar)
    
    # Get mask
    mask = _get_masks(_options_list)
    
    # Get frame info
    if frame_info != []:
        step = frame_info[0]
        start = frame_info[1]
        end = frame_info[2]
        frames = '-frameStep {0} -startFrame {1} -endFrame {2}'.format(step, start, end)
        mask = mask + " " + frames
    
    assCommand = 'arnoldExportAss -s -bb -f \"{0}\" -mask {1}'.format(export_fullpath, mask)
    if full_path == True:
        assCommand += ' -fp'
    if shadow_link == True:
        assCommand += ' -shadowLinks 1'
    else:
        assCommand += ' -shadowLinks 0'
    if light_link == True:
        assCommand += ' -lightLinks 1'
    else:
        assCommand += ' -lightLinks 0'
    
    
    # assCommand = 'arnoldExportAss -s -bb -f \"{0}\" -mask {1} -shadowLinks 0 -lightLinks 0;'.format(export_fullpath, mask)
    assCommand = assCommand + ';'
    if get_only_mel == True:
        selection_cmd = "select -clear;\nselect {0};\n".format(sel_tar)
        return selection_cmd+assCommand
    
    try:
        cmds.refresh(suspend=True)
        mel.eval(assCommand)
        cmds.refresh(suspend=False)
    except Exception as e:
        print(str(e))



def export_materialX(sel_tar="", _mtlx_fullpath="", lookName="", properties="", relativeAssignments=True, fullName=False, separator="/"):
    
    if sel_tar == "" or _mtlx_fullpath == "" or lookName == "":
        return
    
    #create selection command
    cmds.select(clear=True)
    cmds.select(sel_tar)
    
    
    # export materialX
    try:
        cmds.arnoldExportToMaterialX(filename=_mtlx_fullpath,
                                    look=lookName,
                                    properties=properties,
                                    relative=relativeAssignments,
                                    fullPath=fullName,
                                    separator=separator)

        return _mtlx_fullpath
    except Exception as e:
        print(str(e))
        
        
        
        
def set_ai_standin(_ass_path):
    re_sharp_1 = re.compile(r'#(%23){1,4}\.\w+')
    re_sharp_2 = re.compile(r'#(%\d{2}){1,4}\.\w+')
    try:
        from mtoa.ui.arnoldmenu import createStandIn
        print('Arnold plugin - exists')
    except:
        cmds.loadPlugin('mtoa', qt=True)
        from mtoa.ui.arnoldmenu import createStandIn
        print('Arnold plugin - not exists - re loaded')


    


    _is_sequence = False
    _res_1 = re_sharp_1.search(_ass_path)
    _res_2 = re_sharp_2.search(_ass_path)
    if _res_1:
        _is_sequence = True
        _ass_path = re_sharp_1.sub('####'+_ext, _ass_path)
    elif _res_2:
        _is_sequence = True
        _ass_path = re_sharp_2.sub('####'+_ext, _ass_path)
    else:
        _is_sequence = False



    _basename = os.path.basename(_ass_path)
    _basename, _ext = os.path.splitext(_basename)
    if cmds.objExists(_basename+'Shape'):
        if cmds.nodeType(_basename+'Shape') == 'aiStandIn':
            cmds.delete(_basename+'Shape')
            cmds.delete(_basename)


    created_ass_tar = createStandIn()
    created_ass_parent = cmds.listRelatives(created_ass_tar, p=True)[0]
    created_ass_parent = cmds.rename(created_ass_parent, _basename)
    created_ass_tar = created_ass_parent + 'Shape'

    cmds.setAttr('{}.dso'.format(created_ass_tar), _ass_path, type="string")
    if _is_sequence == True:
        cmds.setAttr('{0}.useFrameExtension'.format(created_ass_tar), True)
        
    return created_ass_parent





def get_assetname_GRP(sel_tar: str="") -> str:
    def is_namespace(check_tar):
        if ":" in check_tar:
            return True
        else:
            return False
    if sel_tar == "":
        ls_res = cmds.ls(sl=True, l=True)
        if ls_res == []:
            return ""
        selected_tar = ls_res[0]
    else:
        selected_tar = sel_tar
    
    sn_selected_tar = selected_tar.split("|")[-1]
    if is_namespace(sn_selected_tar):
        tar_namespace = sn_selected_tar.split(":")[0]
        stripped_shapename = sn_selected_tar.split(":")[-1]
        assetname = stripped_shapename.split("_")[0]
        search_res = cmds.ls("{0}*:{1}_GRP*".format(tar_namespace, assetname), l=True)
    else:
        assetname = sn_selected_tar.split("_")[0]
        search_res = cmds.ls("{0}_GRP*".format(assetname), l=True)
        
    if search_res == []:
        return ""
    else:
        return search_res[0]
    

def get_assetname_GRPs(sel_tar :str="") -> dict:
    if sel_tar == "":
        ls_res = cmds.ls(sl=True)
        if ls_res == []:
            return ""
        selected_tar = ls_res[0]
    else:
        selected_tar = sel_tar

    if '|' in selected_tar:
        selected_tar = selected_tar.split("|")[-1]
    assetname = selected_tar.split("_")[0]
    assetname_GRP = "{0}_GRP".format(assetname)

    return {"NORMAL":cmds.ls(assetname_GRP+"*"), "WITH_NAMESPACE":cmds.ls("*:*"+assetname_GRP+"*")}
    



def get_version_info_from_geo(sel_tar: str="") -> str:
    
    assetname_GRP = get_assetname_GRP(sel_tar)
    if assetname_GRP == "":
        return ""
    if cmds.objExists(assetname_GRP+".notes") == False:
        return ""
    return cmds.getAttr(assetname_GRP+".notes")


def get_ver_info(contents: str):
    mdl_pubver = ""
    mdl_devver = ""
    
    pub_search_res = re.search("pub(:|[a-zA-Z]|\s)+v\d+", contents)
    dev_search_res = re.search("dev(:|[a-zA-Z]|\s)+v\d+", contents)
    if pub_search_res:
        mdl_pubver = re.search("v\d+",pub_search_res.group()).group()
    else:
        return "", ""
        
    if dev_search_res:
        mdl_devver = re.search("v\d+",dev_search_res.group()).group()
    else:
        return "", ""
    return (mdl_pubver, mdl_devver)


