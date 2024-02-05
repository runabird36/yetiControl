
import maya.cmds as cmds
import maya.mel as mel
import os, re
from importlib import reload
from maya_md import yt_py
import YFB_yeti_model
reload(YFB_yeti_model)

def convert2_maya_color(color_code_list):
    converted_code = []
    for _code_num in color_code_list:
        converted_code.append(_code_num/256.0)
    return converted_code

def get_start_time():
    return cmds.playbackOptions(q=True, min=True)

def get_end_time():
    return cmds.playbackOptions(q=True, max=True)

def get_start_frame():
    return cmds.getAttr ("defaultRenderGlobals.startFrame")

def get_end_frame():
    return cmds.getAttr ("defaultRenderGlobals.endFrame")





def getFilePath() -> str:
    return  cmds.file(q=True, sn=True)


def get_dirpath() -> str:
    full_filepath = getFilePath()
    if full_filepath == '':
        return None
    return os.path.dirname(full_filepath)



def get_filename() -> str:
    full_filepath = getFilePath()
    if full_filepath == '':
        return None
    return os.path.basename(full_filepath)


def get_bake_fullpath() -> str:
    cur_dirpath = get_dirpath()
    if "\\" in cur_dirpath:
        cur_dirpath = cur_dirpath.replacE("\\", "/")


    if "/dev/scenes/maya" in cur_dirpath:
        root_path = cur_dirpath.split("/dev/")[0]
        return root_path + "/dev/cache/fur/<version_num>/<namespace>_<yeti_name>.%04d.fur"
    else:
        return cur_dirpath + "/cache/fur/<version_num>/<namespace>_<yeti_name>.%04d.fur"


def does_furcache_exists(fur_fullpath :str) -> bool:
    
    dirname = os.path.dirname(fur_fullpath)
    basename = os.path.basename(fur_fullpath)
    
    bias = basename.split(".%04d.")[0]
    
    for _file in os.listdir(dirname):
        if re.search(bias+"\.\d+\.fur", _file):
            print(re.search(bias+"\.\d+\.fur", _file).group())
            return True
            
    return False    



def get_bake_dir() -> str:
    cur_dirpath = get_dirpath()
    if "\\" in cur_dirpath:
        cur_dirpath = cur_dirpath.replacE("\\", "/")

    bake_dir = ""
    if "/dev/scenes/maya" in cur_dirpath:
        root_path = cur_dirpath.split("/dev/")[0]
        bake_dir = root_path + "/dev/cache/fur/<version_num>"
    else:
        bake_dir = cur_dirpath + "/cache/fur/<version_num>"

    check_path = bake_dir.replace("<version_num>", "")
    if not os.path.exists(check_path):
        os.makedirs(check_path)
    return bake_dir


def set_visibility(node_name :str, status :bool) -> None:
    
    if re.search(r"\|cache\|v\d+",node_name):
        root_temp   = node_name.split("|cache")[0]
        tar_ver     = node_name.split("|cache|")[-1]
        root        = root_temp + "|" + "cache"
        for cache_ver in cmds.listRelatives(root, c=True, f=True):
            if status == False:
                cmds.setAttr(cache_ver+".visibility", status)
                continue
            if cache_ver.endswith(tar_ver) == True and status == True:
                cmds.setAttr(cache_ver+".visibility", status)
            else:
                cmds.setAttr(cache_ver+".visibility", not status)
        return
    try:
        cmds.setAttr(node_name+".visibility", status)
    except Exception as e:
        print(str(e))


def get_yeti_cache_fname(ns_num :str, yeti_short_name :str) -> str:
    temp01 = yeti_short_name.split("_YETI")[0]
    temp02_list = temp01.split("_")
    temp02_list.pop(0)
    cache_name = '_'.join(temp02_list)
    cache_name = ns_num+"_"+cache_name

    return cache_name + ".%04d.fur"


def get_yeti_cache_path(bake_dir :str, yeti_ns_num :str, yeti_short_name :str, cache_vernum :str) -> list:

    if  "/<version_num>" in bake_dir:
        bake_dir = bake_dir.replace("<version_num>", "")
    
    cache_dir_path = bake_dir + "/" + cache_vernum
    cache_fname = get_yeti_cache_fname(yeti_ns_num, yeti_short_name)

    return cache_dir_path + "/" + cache_fname


def get_bake_vernum() -> str:
    def make_upper_version(low_ver :str) -> str:
        low_ver_only_num = int(low_ver.replace("v", ""))
        upper_ver_only_num = low_ver_only_num + 1
        return "v" + str(upper_ver_only_num).zfill(3)

    dirpath = get_bake_dir()
    without_vernum = dirpath.replace("/<version_num>", "")

    real_num_folder = []
    for folder in os.listdir(without_vernum):
        if not re.search(r"v\d+", folder):
            continue
        real_num_folder.append(folder)

    if real_num_folder == []:
        return "v001"
    real_num_folder.sort()
    last_vernum = real_num_folder.pop()

    return make_upper_version(last_vernum)
        



re_ex_fname = re.compile(r'[a-zA-Z]{3}\_\d{4}_\w+\_v\d+')
def is_right_filename() -> bool:
    file_name = get_filename()
    _res = re_ex_fname.search(file_name)
    if _res:
        return True
    else:
        return False





def is_sim_grp(check_tar :str) -> bool:
    if re.search(r"[a-zA-Z]+\_\d{3}\_yetiGRP"):
        return True
    else:
        return False


def is_yeti_node(check_tar :str) -> bool:
    '''
    kadan_body_YETI_002
    '''
    if re.search(r"([a-zA-Z]+\_)+YETI_(\d{3}|\d{3}Shape)", check_tar):
        return True
    else:
        return False


def get_selected_yeti() -> list:
    return cmds.ls(sl=True, ni=True, dag=True, type="pgYetiMaya")






num_re_ex = re.compile('\_\d{3}$')
num_re_ex_2 = re.compile('\d+')


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
        return None
    
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
            if asset_namespace == None:
                return None
    except Exception as e:
        print(str(e))
        asset_namespace = _get_assetnum_from_assetGRP(connected_geo)
    return asset_namespace



def get_aniNS(basemesh_info) -> str:
    if isinstance(basemesh_info, list):
        return get_aniNS_from_geo(basemesh_info[0])
    else:
        return get_aniNS_from_geo(basemesh_info)

def get_aniNS_from_yetiGRP(yeti_node : str) -> str:
    tar = ""
    if '|' in yeti_node:
        tar = yeti_node.split('|')[-1].split('_')[-1]
    else:
        tar = yeti_node.split('_')[-1]
    if not re.search(r'\d+', tar):
        return None

    if re.search(r'Shape$|Shape[a-zA-Z]+$', tar):
        return re.sub(r'Shape$|Shape[a-zA-Z]+$', '', tar)
    else:
        return tar


def get_selected_yeti_v02():
    cur_bake_dir = get_bake_dir()
    for cur_yeti in cmds.ls(sl=True, ni=True, dag=True, l=True, type="pgYetiMaya"):
        long_name       = cur_yeti
        short_name      = cur_yeti.split('|')[-1]
        basemesh_list   = yt_py.get_info_from_yeti(cur_yeti, info_type="mesh")

        ani_ns_num = get_aniNS(basemesh_list)
        print(33333333, ani_ns_num)
        if ani_ns_num == None:
            ani_ns_num = get_aniNS_from_yetiGRP(cur_yeti)
        yield YFB_yeti_model.YetiInfo(long_name=long_name, short_name=short_name, ns_num=ani_ns_num, bake_dir=cur_bake_dir)

def get_all_yeti():
    cur_bake_dir = get_bake_dir()
    for cur_yeti in cmds.ls(ni=True, dag=True, l=True, type="pgYetiMaya"):
        if "|yeti|" in cur_yeti:
            long_name       = cur_yeti
            short_name      = cur_yeti.split('|')[-1]
            basemesh_list   = yt_py.get_info_from_yeti(cur_yeti, info_type="mesh")

            ani_ns_num = get_aniNS(basemesh_list)
            if ani_ns_num == None:
                ani_ns_num = get_aniNS_from_yetiGRP(cur_yeti)
            yield YFB_yeti_model.YetiInfo(long_name=long_name, short_name=short_name, ns_num=ani_ns_num, bake_dir=cur_bake_dir)


def get_grooms_from_yeti(yeti_model) -> list:
    return yt_py.get_info_from_yeti(yeti_model.long_name, info_type="pgYetiGroom")

def get_bmesh_from_yeti(yeti_model) -> list:
    return yt_py.get_info_from_yeti(yeti_model.long_name, info_type="mesh")


def get_yeti_from_simGRP(selected_node):
    target = ""




def select_node(node) -> None:
    try:
        cmds.select(node)
    except Exception as e:
        print(str(e))



# ============================================================================
#                       Fur cache baking
# ============================================================================

def name_setting(func):
    def to_cachename(tar):
        cache_name = tar.split('_')[1]
        cmds.rename(tar, cache_name)
        return cache_name
        
    def get_namespace(tar):
        word_list = tar.split("_")
        assetname = word_list[0]
        ns_num = word_list[-1]
        ns_num = re.sub(r"[a-zA-Z]+", "", ns_num)
        return assetname+"_"+ns_num
        
    def to_cachename_v02(tar, cur_ns):
        sh_name = tar.short_name
        l_name = tar.long_name
        temp01 = sh_name.split("_YETI")[0]
        temp02_list = temp01.split("_")
        temp02_list.pop(0)
        cache_name = '_'.join(temp02_list)
        cache_name = cur_ns+"_"+cache_name

        print(l_name , " -> ", cache_name)
        try:
            cmds.rename(l_name, cache_name)
        except:
            pass
        return cache_name
        
    def to_origin_name(tar, origin_name):
        cmds.rename(tar, origin_name)
        
        
    def decorated(*args, **kwargs):
        yeti_list = kwargs["tar_list"]
        changed_name_list = []
        for yeti_info in yeti_list:
            cur_ns = get_namespace(yeti_info.short_name)
            res = to_cachename_v02(yeti_info, cur_ns)
            changed_name_list.append(res)
        kwargs["cache_name_list"] = changed_name_list
        try:
            func(**kwargs)
        except:
            pass
        for origin, changed in zip(yeti_list, changed_name_list):
            to_origin_name(changed, origin.short_name)
        
    return decorated
    

@name_setting
def bake_fur(**kwargs):
    
    print("Input parms : ", kwargs)
    tar_list     = kwargs["cache_name_list"]
    path_dir     = kwargs["path_dir"]
    frame_in     = kwargs["frame_in"]
    frame_out    = kwargs["frame_out"]
    samples      = kwargs["samples"]
    
    if os.path.exists(path_dir) == False:
        os.makedirs(path_dir)
    
    cmds.select(tar_list)
    print("Bake targets : ", tar_list)
    bake_cmd = "pgYetiCommand -writeCache \"{DIRNAME}/<NAME>.%04d.fur\" -range {FRAME_IN} {FRAME_OUT} -samples {SAMPLES}".format(DIRNAME  = path_dir,
                                                                                                                                   FRAME_IN = frame_in,
                                                                                                                                   FRAME_OUT= frame_out,
                                                                                                                                   SAMPLES  = samples)
    try:                                                                                                                                   
        print("Bake Command : ", bake_cmd)
        mel.eval(bake_cmd)
    except:
        pass
    


def bake_yeti_fur(bake_targets :list, bake_dir :str, bake_vernum :str, s_frame :str, e_frame :str, input_samples :str="3") -> None:
    bake_dir = bake_dir + "/" + bake_vernum
    bake_fur(tar_list=bake_targets, path_dir=bake_dir, frame_in=s_frame, frame_out=e_frame, samples=input_samples)







# ============================================================================
#                       Fur cache setting
# ============================================================================

def get_root_node(l_name) -> str:
    tar_name_list = []
    for elem in l_name.split("|"):
        if elem == "yeti":
            break
        tar_name_list.append(elem)
    return "|".join(tar_name_list)
    

def does_exists(l_name) -> bool:
    return cmds.objExists(l_name)
    
def create_node(l_name, n_type) -> None:
    node_name = l_name.split("|")[-1]
    temp = l_name.split("|")
    temp.pop()
    parent_node = "|".join(temp)
    cmds.createNode(n_type, n=node_name, p=parent_node)

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

def get_attr_info_from_yeti(yeti_lname :str) -> dict:
    
    # Get assigned shadingGroup
    assigned_hair_mat = get_shading_engines(yeti_lname)
    if assigned_hair_mat == []:
        assigned_hair_mat = ""
    else:
        assigned_hair_mat = assigned_hair_mat[0]
    
    # Get image search path
    isp_info = yt_py.get_yeti_imageSearchPath(yeti_name=yeti_lname)

    return {"MAT":assigned_hair_mat, "ISP":isp_info}

def init_cache_structure( yeti_short_name :str, yeti_long_name :str, cache_vernum :str, cache_path :str) -> None:
    
    # Create Empty trasform node group
    root_node = get_root_node(yeti_long_name)

    yeti_node = root_node + "|" + "yeti"
    grm_node = root_node + "|" + "grm"
    cache_node = root_node + "|" + "cache"

    version_node = cache_node + "|" + cache_vernum

    if does_exists(cache_node) == False:
        create_node(cache_node, "transform")

    if does_exists(version_node) == False:
        create_node(version_node, "transform")


    # Get original yeti node info : Material / Image Search Path
    yeti_info_dict = get_attr_info_from_yeti(yeti_long_name)
    hair_mat            = yeti_info_dict["MAT"]
    image_search_path   = yeti_info_dict["ISP"]


    # Create Yeti node for cache and set information
    if re.search(r'Shape$|Shape[a-zA-Z]+$', yeti_short_name):
        y_nodename= re.sub(r'Shape$|Shape[a-zA-Z]+$', '', yeti_short_name)
    else:
        y_nodename = yeti_short_name
    tar_yeti_node = version_node + "|" + y_nodename
    if does_exists(tar_yeti_node) == False:
        tar_yeti_node = yt_py.create_yeti_node(y_nodename)
        
        # print(1111111, tar_yeti_node) # 1111111 |kadan_body_YETI_002
    
    yt_py.set_yeti_cachepath(yeti_name=tar_yeti_node, cache_path=cache_path)
    yt_py.set_yeti_imageSearchPath(yeti_name=tar_yeti_node, isp_path=image_search_path)
    cmds.select(tar_yeti_node)
    cmds.hyperShade(assign=hair_mat)

    cmds.setAttr(tar_yeti_node+".fileMode", 1)

    try:
        cmds.parent(tar_yeti_node, version_node)
    except:
        pass

    origin_yeti_node    = yeti_node
    cache_version_node  = version_node
    return origin_yeti_node, cache_version_node





    

    



    
