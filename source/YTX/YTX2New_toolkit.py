

from importlib import reload
import maya.cmds as cmds
import maya.mel as mel
from source.YCPackages import neon, yt_py
reload(neon)
import re
from traceback import print_exc

# from customQT import core

def disconnect_linked_attr(_target):
    if _target == []:
        return
    if isinstance(_target, str):
        tar = _target
        con_info = cmds.listConnections(tar, c=True,p=True,s=True)
        for con in con_info:
            #print con

            connected_attr = cmds.connectionInfo(con,sfd=True)
            if connected_attr == '':
                continue
            cmds.disconnectAttr(connected_attr, con)
    elif isinstance(_target, list):
        for tar in _target:
            con_info = cmds.listConnections(tar, c=True,p=True,s=True)
            if con_info == None:
                continue
            for con in con_info:
                #print con

                connected_attr = cmds.connectionInfo(con,sfd=True)
                if connected_attr == '':
                    continue
                cmds.disconnectAttr(connected_attr, con)






def connect_texRef_2_tarShape(tex_ref, tar_shape):
    cmds.connectAttr(tex_ref + ".message", tar_shape + ".referenceObject", f=True)




# def get_next_number(asset_name):
#     grp_name = "{0}_*_yetiGRP".format(asset_name)
#     all_tars = cmds.ls(grp_name, l=True, typ='transform')
#
#     all_tars.sort()
#
#     last_tar = all_tars[-1]
#     ns_num_check = last_tar.split('_')[1]
#     try:
#         ns_num = int(ns_num_check)
#     except Exception as e:






def create_yeti_group_cfx_ver(tar_assetname_GRP):
    re_ex_num = re.compile(r'[0-9]+$')
    asset_name = tar_assetname_GRP.split('_')[0]



    print(11111111111, tar_assetname_GRP)
    ns_num = neon.get_aniNS_from_geo(tar_assetname_GRP)
    print(ns_num)
    if ns_num == '':
        # group_num = get_next_number(asset_name, group_num)
        group_num = "0"
        _res = re_ex_num.search(tar_assetname_GRP)
        if _res:
            group_num = str(int(_res.group()) + 1)
        else:
            group_num = "1"

        group_num = group_num.zfill(3)
    else:
        group_num = ns_num.split('_')[-1]

    grp_name = "{0}_{1}_yetiGRP".format(asset_name, group_num)
    if cmds.objExists(grp_name) == True:
        geo_exists_check = cmds.listRelatives(grp_name+'|geo', c=True)
        if geo_exists_check != []:
            cmds.parent(geo_exists_check, w=True)
        cmds.delete(grp_name)
    else:
        pass
    top_group = cmds.group(em=True, n=grp_name)

    geo_group = cmds.group(em=True, p=top_group ,n="geo")
    yeti_group = cmds.group(em=True, p=top_group ,n="yeti")
    grm_group = cmds.group(em=True, p=top_group ,n="grm")

    cmds.parent(tar_assetname_GRP, geo_group)



    return top_group, group_num



def create_yeti_group_sim_ver(tar_assetname_GRP):
    re_ex_num = re.compile(r'[0-9]+$')
    asset_name = tar_assetname_GRP.split('_')[0]




    ns_num = neon.get_aniNS_from_geo(tar_assetname_GRP)
    if ns_num == '':
        # group_num = get_next_number(asset_name, group_num)
        group_num = "0"
        _res = re_ex_num.search(tar_assetname_GRP)
        if _res:
            group_num = _res.group()

        group_num = group_num.zfill(3)
    else:
        group_num = ns_num.split('_')[-1]

    grp_name = "{0}_{1}_yetiGRP".format(asset_name, group_num)
    if cmds.objExists(grp_name) == True:
        geo_exists_check = cmds.listRelatives(grp_name+'|geo', c=True)
        if geo_exists_check != []:
            cmds.parent(geo_exists_check, w=True)
        cmds.delete(grp_name)
    else:
        pass
    top_group = cmds.group(em=True, n=grp_name)

    geo_group = cmds.group(em=True, p=top_group ,n="geo")
    yeti_group = cmds.group(em=True, p=top_group ,n="yeti")
    

    cmds.parent(tar_assetname_GRP, geo_group)



    return top_group, group_num



def find_exactTar_under_curTopNode(cur_top_node, tar_info):
    print(tar_info)
    _magic_name = '*{0}'.format(tar_info)
    for _check_tar in cmds.ls(_magic_name, l=True):
        if cur_top_node in _check_tar:
            return _check_tar

    return ''








def grouping_tar(root_grp, tar_node, node_type):
    if node_type == 'YETI':
        tar_group = '|{0}|yeti'.format(root_grp)
    elif node_type == 'GROOM':
        tar_group = '|{0}|grm'.format(root_grp)

    cmds.parent(tar_node, tar_group)
    return '{0}|{1}'.format(tar_group, tar_node)





def get_real_tar_shape(real_shape_list, shape_of_grm):
    for _real in real_shape_list:
        if shape_of_grm in _real:
            return _real

# [{u'Y_value': 0.0, u'y_type': u'FLOAT', u'Y_max': [1.0], u'name': u'yetiVariableF_guideOff', u'Y_min': [0.0]}]
# [{u'y_type': u'VECTOR', u'name': u'yetiVariableV_AAA', u'detail': [{u'Y_value': 0.0, u'Y_max': None, u'name': u'yetiVariableV_AAAX', u'Y_min': None}, {u'Y_value': 1.0, u'Y_max': [1.0], u'name': u'yetiVariableV_AAAY', u'Y_min': None}, {u'Y_value': 2.0, u'Y_max': [2.0], u'name': u'yetiVariableV_AAAZ', u'Y_min': [0.0]}]}]

_addAttr_basic_template = "addAttr -ln \"{0}\""
def create_yeti_float_var(created_yeti, _float_info_dict, _do_exists_parent=False, _p_attr=""):
    global _addAttr_basic_template

    _addAttr_template = _addAttr_basic_template
    created_yeti = cmds.ls(created_yeti, l=True, ni=True, dag=True, type="pgYetiMaya")[0]

    _attr_name = _float_info_dict.get('name')
    _min = _float_info_dict.get('Y_min')
    _max = _float_info_dict.get('Y_max')
    _value = _float_info_dict.get('Y_value')

    _addAttr_template = _addAttr_template.format(_attr_name)

    if _do_exists_parent == True:
        _addAttr_template += " -p \"{0}\"".format(_p_attr)
    _addAttr_template += " -at double"


    if _min:
        if isinstance(_min, list) == True:
            _min = _min[0]
        print(_min)
        print(type(_min))
        _addAttr_template += " -min " + str(_min)

    if _max:
        if isinstance(_max, list) == True:
            _max = _max[0]
        _addAttr_template += " -max " + str(_max)

    _addAttr_template += " -dv " + str(_value)
    _addAttr_template += " " + created_yeti
    print('='*50)
    print(_addAttr_template)
    mel.eval(_addAttr_template+";")







def create_yeti_vector_var(created_yeti, _vec_info_dict):
    global _addAttr_basic_template

    _addAttr_template = _addAttr_basic_template
    created_yeti = cmds.ls(created_yeti, l=True, ni=True, dag=True, type="pgYetiMaya")[0]

    _p_attr_name = _vec_info_dict.get('name')
    _child_detail = _vec_info_dict.get('detail')

    _addAttr_template = _addAttr_template.format(_p_attr_name)
    _addAttr_template += " -at double3 " + created_yeti

    print('='*50)
    print(_addAttr_template)
    mel.eval(_addAttr_template+";")
    for _child_info_dict in _child_detail:
        create_yeti_float_var(created_yeti, _child_info_dict, _do_exists_parent=True, _p_attr=_p_attr_name)




def do_assign(cur_tar, y_info_hub):
    status = True
    try:
        # Step 1. create empty group hierarchy
        cur_top_node, ns_num = create_yeti_group_cfx_ver(cur_tar)
    except:
        # core.get_confirm_dialog("YTX2", "그룹 hierarchy를 만드는데 있어 문제가 생겼습니다.", "error", ["ok"])
        print_exc()
        status = False
        return status

    for _yeti_data in y_info_hub:

        y_input_shape_list = []
        # Step 2. connect Attribute between .message and .referenceObject
        #         and store basemesh long path name in list
        shape_texRef_pair_list = _yeti_data.get_shape_pair_list()
        for tar_shape_info, tex_ref in shape_texRef_pair_list:
            # print tar_shape_info
            # print tex_ref
            # print '='*50
            tar_basemesh = find_exactTar_under_curTopNode(cur_top_node, tar_shape_info)
            if tar_basemesh == '':
                print('='*50)
                print('Error : There is no hair base mesh!!!!!!!!!!!!!')
                print('--------> {0}'.format(tar_shape_info))
                print('='*50)
                continue


            tex_ref = cmds.ls(tex_ref, dag=True, noIntermediate=True, typ='mesh')[0]
            connect_texRef_2_tarShape(tex_ref, tar_basemesh)
            
            y_input_shape_list.append(tar_basemesh)


        # Step 4. Do yeti node setting
        #   (0) Create Yeti node
        #   (1) import .grm file
        #   (2) set fileMode attribute to Cache
        #   (3) turn on overrideCacheWithInputs attribute


        # (0) Create Yeti node
        grm_path = _yeti_data.get_grm_path()
        img_search_path = _yeti_data.get_image_search_path()
        cur_render_denstiy = _yeti_data.get_render_denstiy()

        _y_node_name = _yeti_data.get_yeti_node()
        _y_node_name = _y_node_name.split('Shape')[0] + '_{0}'.format(ns_num)
        created_yeti = yt_py.create_yeti_node(_y_node_name)
        created_yeti = grouping_tar(cur_top_node, created_yeti, 'YETI')


        created_yeti_with_shape_info = []
        for tar_shape in y_input_shape_list:
            yt_py.add_basemesh_to_yeti(created_yeti, tar_shape)

        created_yeti_with_shape_info.append({'YETI':created_yeti, 'SHAPE_list':y_input_shape_list})

        grm_file_attr = created_yeti + ".cacheFileName"
        file_mode_attr = created_yeti + ".fileMode"
        override_attr = created_yeti + ".overrideCacheWithInputs"
        img_search_path_attr = created_yeti + ".imageSearchPath"

        display_density_attr = created_yeti + ".viewportDensity"
        display_width_attr = created_yeti + ".viewportWidth"
        display_cacheSize_attr = created_yeti + ".displayCacheMaximumSize"

        render_density_attr = created_yeti + ".renderDensity"

        cmds.setAttr(grm_file_attr, grm_path, typ="string")
        cmds.setAttr(file_mode_attr, 1)
        cmds.setAttr(override_attr, 1)

        if img_search_path != None:
            if '\\' in img_search_path:
                img_search_path = img_search_path.replace('\\', '/')
            cmds.setAttr(img_search_path_attr, img_search_path, typ="string")

        # cmds.setAttr(display_density_attr, 0.1)
        cmds.setAttr(display_width_attr, 1)
        cmds.setAttr(render_density_attr, cur_render_denstiy)


        print("Yeti variable")
        try:
            # [{u'Y_value': 0.0, u'y_type': u'FLOAT', u'Y_max': [1.0], u'name': u'yetiVariableF_guideOff', u'Y_min': [0.0]}]
            # [{u'y_type': u'VECTOR', u'name': u'yetiVariableV_AAA', u'detail': [{u'Y_value': 0.0, u'Y_max': None, u'name': u'yetiVariableV_AAAX', u'Y_min': None}, {u'Y_value': 1.0, u'Y_max': [1.0], u'name': u'yetiVariableV_AAAY', u'Y_min': None}, {u'Y_value': 2.0, u'Y_max': [2.0], u'name': u'yetiVariableV_AAAZ', u'Y_min': [0.0]}]}]
            for _float_var_info in _yeti_data.get_float_var_list():
                create_yeti_float_var(created_yeti, _float_var_info)

            for _vec_var_info in _yeti_data.get_vector_var_list():
                create_yeti_vector_var(created_yeti, _vec_var_info)
        except:
            traceback.print_exc()





        # Step 4. Do yeti node setting
        #   (1) import groom from current yeti in for loop and store groomShape name list and number
        #   (2) if the grooming data is related with curve sim, set curve set in yeti graph
        shape_and_grm_info_list = _yeti_data.get_shape_and_grm_list()
        _IS_CURVE_SIM = _yeti_data.is_curve_sim()


        curve_set_info_list = _yeti_data.get_setCurves_list()

        for created_yeti_with_shape in created_yeti_with_shape_info:
            created_yeti = created_yeti_with_shape.get('YETI')
            real_shape_list = created_yeti_with_shape.get('SHAPE_list')


            imported_groom_list = []
            imported_groom_list_transformName = []
            created_yeti_shape = cmds.ls(created_yeti, dag=True, noIntermediate=True, typ='pgYetiMaya')[0]
            for shape_and_grm_dict in shape_and_grm_info_list:
                _grm_of_shape = shape_and_grm_dict.get('EACH_linked_GRM')
                _shape_of_grm = shape_and_grm_dict.get('EACH_linked_SHAPE')
                real_shape = get_real_tar_shape(real_shape_list, _shape_of_grm)



                if real_shape == None:
                    continue
                _new_grm = yt_py.import_groom_from_yeti(_grm_of_shape, real_shape, created_yeti_shape)

                imported_groom_list.append(_new_grm)
                imported_groom_list_transformName.append(cmds.listRelatives(_new_grm, p=True)[0])

                grouping_tar(cur_top_node, _new_grm, 'GROOM')





            if _IS_CURVE_SIM == True:

                rename_info_dict = {}

                for curve_set_dict in curve_set_info_list:
                    # tar_curve_list = curve_set_dict.get('EACH_SET_LIST')
                    # tar_crv_grp_name = curve_set_dict.get('EACH_SET_LIST')
                    tar_curve_grp_name = []
                    tar_crv_grps = curve_set_dict.get('EACH_SET_LIST')
                    print(cur_top_node)
                    print(type(tar_crv_grps))
                    print(tar_crv_grps)
                    if isinstance(tar_crv_grps, list):
                        for _tar_crv_grp in tar_crv_grps:
                            tar_curve_grp_name.append(find_exactTar_under_curTopNode(cur_top_node, _tar_crv_grp))
                    elif isinstance(tar_crv_grps, str) or isinstance(tar_crv_grps, str):
                        tar_curve_grp_name.append(find_exactTar_under_curTopNode(cur_top_node, tar_crv_grps))
                    else:
                        tar_curve_grp_name.append(find_exactTar_under_curTopNode(cur_top_node, tar_crv_grps))
                    tar_set_name = curve_set_dict.get('EACH_SET')
                    to_set_name = '{0}_{1}'.format(tar_set_name, ns_num)
                    # print to_set_name
                    # print(1111111111111111111111111)
                    # print(tar_curve_grp_name)
                    # print(to_set_name)
                    if cmds.objExists(to_set_name) and cmds.nodeType(to_set_name) == 'objectSet':
                        pass
                    else:
                        tar_curve_list = cmds.listRelatives(tar_curve_grp_name, c=True, f=True)
                        cmds.select(tar_curve_list)
                        res_set_name = cmds.sets(name=to_set_name)



                    yt_py.add_set_to_yeti(created_yeti_shape, to_set_name)
                    rename_info_dict[tar_set_name] = to_set_name


                    # Save guide rest pose
                    # print("Do Save guide rest pose")
                    # cmds.select(deselect=True)
                    # cmds.select(to_set_name)
                    # mel.eval("pgYetiCommand -saveGuidesRestPosition;")


            file_mode_attr = created_yeti_shape + ".fileMode"
            override_attr = created_yeti_shape + ".overrideCacheWithInputs"
            cmds.setAttr(file_mode_attr, 0)
            cmds.setAttr(override_attr, 0)

            if _IS_CURVE_SIM == True:
                for _from_set_name, _to_set_name in list(rename_info_dict.items()):

                    yt_py.update_set_name(created_yeti_shape, _from_set_name, _to_set_name)


            # Step 5. Assign hair or fur material
            tar_mat = _yeti_data.get_hair_mat()
            cmds.select(created_yeti_shape)
            cmds.hyperShade(assign=tar_mat)
    

    return status