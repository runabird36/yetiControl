import maya.cmds as cmds
import os, re, sys
import collections

import checker
# reload (checker)
from checker import Checker
import pickle
from maya_md import neon
from general_md_3x import LUCY

class GeoChecker(Checker):
    warn_count = 0
    clear_items = []
    def __init__(self):
        Checker.__init__(self)
        self.set_title("Geo Check")
        self._err_list = []


    def add_custom_warnning(self, _tar, error_msg, status, _etc):
        self._err_list.append([_tar, error_msg])


    def get_all_mdl_ref_address(self, targets):
        '''
        {u'vampLordAwakenNew_001': u'Z:/projects/projectName/2018_11_kakako/asset/char/vampLordAwakenNew/mdl/pub/ma/publish_vampLordAwakenNew_mdl_asset01_v20.ma'}
        '''
        # =====================this part for only selected target in ani step===============================
        # before : although erase target among targets, targets get all targets in ani step
        targets_ns_list = []
        for target in targets:
            if target.find(':')>0:
                target_ns = target.split(':')[0]
            else:
                target_ns = target
            targets_ns_list.append(target_ns)

        all_ref_list_with_num = []
        rn_list_by_neon = []
        rn_list_by_neon=neon.get_all_RNs()
        for target_ns in targets_ns_list:
            for rn in rn_list_by_neon:
                if target_ns in rn and LUCY.get_category() == 'sequence':
                    all_ref_list_with_num.append(rn)
                else:
                    if LUCY.get_pipe_step() in ['lookdev','rigging']:
                        all_ref_list_with_num.append(rn)

        # this part for erase num which is in the end of RN name
        all_ref_list = []
        re_ex_num = re.compile(r'\d+$')
        for ref in all_ref_list_with_num:
            if re_ex_num.search(ref):
                # this part for like 'pub_ryan_mdlRN1 pub_rayn_mdl' or 'pub_ryan_mdlRN2 pub_rayn_mdl'...
                # Thus if there is number behind of 'RN',
                # unlock reference node -> rename reference node -> lock reference node
                if LUCY.get_pipe_step() in ['lookdev', 'rigging']:
                    if 'mdl' in ref:
                        continue
                    from_rn = ref
                    ref = re_ex_num.sub('', ref)
                    to_rn = ref
                    cmds.lockNode(from_rn, lock=False)
                    cmds.rename(from_rn, to_rn)
                    cmds.lockNode(to_rn, lock=False)
                else:
                    ref = re_ex_num.sub('', ref)
            else:
                ref= ref
            all_ref_list.append(ref)

        #======================================================================================================

        mdl_ref_address_dict = {}
        for ref in all_ref_list:
            if ref.find('_mdl')>0:
                if ref.startswith('pasted__'):
                    continue
                try:
                    mdl_ref_address = cmds.referenceQuery(ref, filename=True)
                except Exception as e:
                    print(e)
                    print('There is no reference node named {0}!!!!!!\nPlease check if there is number behind RN word'.format(ref))
                ref = ref.split(':')
                if ref[0].endswith('RN'):
                    regular_ex = re.compile(r'\BRN\b')
                    ref[0] = regular_ex.sub('', ref[0])
                mdl_ref_address_dict[ref[0]] = mdl_ref_address
        # pprint.pprint(mdl_ref_address_dict)
        return mdl_ref_address_dict

    def remove_prefix_in_data(self, remove_target, all_shape):
        removed_all_shape = []

        for shape in all_shape:
            des_shape = shape.replace(remove_target, '')
            removed_all_shape.append(des_shape)

        return removed_all_shape

    def removeshape_Deform_posfix_in_data(self, all_shape):
        removed_all_shape = []
        regular_ex = re.compile('Constraint')
        regular_ex_2 = re.compile('Deformed$|Deformed\w+$|Deform$') # $ : similar with endswith()
                                                                    # \w : all num and all word
                                                                    # \d : all num
                                                                    # + : repeat
                                                                    # | : or
                                                                    # \w+$ : catch 'Deformed1', 'Deformed12', 'Deformedaa'
        regular_ex_3 = re.compile('Orig$|Orig\w+$|\d+Orig')

        for shape in all_shape:
            only_shape_node_list = shape.split('|')
            check_type_target = only_shape_node_list[-1]
            if self.step_data in ['animation','layout']:
                check_type_target = '{0}{1}'.format(self.remove_target_namespace,check_type_target)
            if check_type_target == '':
                continue
            else:
                try:
                    shape_type = cmds.objectType(check_type_target)
                except:
                    try:
                        shape_type = cmds.objectType(shape)
                    except Exception as e:
                        print(e)

            if regular_ex_2.search(shape):
                continue
            elif regular_ex_3.search(shape):
                continue
            elif regular_ex.search(shape_type):
                continue
            else:
                removed_all_shape.append(shape)

        return removed_all_shape
    def remove_namespace_in_data(self, target_namespace, all_shape):

        removed_all_shape = []
        regular_ex = re.compile(target_namespace)
        for shape in all_shape :
            shape= regular_ex.sub('',shape)
            removed_all_shape.append(shape)

        # pprint.pprint(removed_all_shape)
        return removed_all_shape

    def get_asset_GRP_from_assetGroup(self, targets_from_controller):
        check_target_list = []

        for tar in targets_from_controller:
            if '_groupAsset' in tar:
                target_rigs_list = cmds.listRelatives(tar, c=True)
                for rig in target_rigs_list:
                    rig_geo = '{0}|*:geo'.format(rig)
                    rig_geo_child = cmds.listRelatives(rig_geo, c=True)
                    check_target_list.append(rig_geo_child[0])
            else:
                check_target_list.append(tar)

        return check_target_list


    def execute(self, targets):
        targets = self.get_asset_GRP_from_assetGroup(targets)
        self.clear_items = []
        self._err_list = []
        
        self.step_data = LUCY.get_pipe_step()
        asset_name = LUCY.get_assetname()


        # 1. get hichy format file address
        # 2. put the address in dict with namespace by key
        mdl_hichy_format_address_dict = {}
        mdl_all_ref_address_dict = self.get_all_mdl_ref_address(targets)
        # pprint.pprint( mdl_all_ref_address_dict)
        for mdl_ref_address_key in mdl_all_ref_address_dict:
            mdl_ref_address =  mdl_all_ref_address_dict[mdl_ref_address_key]

            #delete  referrence version num
            regular_ex_1 = re.compile(r'{[0-9]+}')
            if regular_ex_1.search(mdl_ref_address):
                mdl_ref_address = regular_ex_1.sub('',mdl_ref_address)


            # change file format from ma or mb to hichy
            if mdl_ref_address.endswith('.mb'):
                regular_ex_2 = re.compile(r'\bmb\b')
                hichy_address= regular_ex_2.sub('hichy',mdl_ref_address)
            elif mdl_ref_address.endswith('.abc'):
                regular_ex_2 = re.compile(r'\babc\b')
                hichy_address= regular_ex_2.sub('hichy',mdl_ref_address)
            else:
                regular_ex_2 = re.compile(r'\bma\b')
                hichy_address= regular_ex_2.sub('hichy',mdl_ref_address)

            # this is temperary code
            if mdl_ref_address.find('publish_')>0:
                regular_ex_3 = re.compile('publish_')
                hichy_address = regular_ex_3.sub('pub_',hichy_address)


            if mdl_ref_address.find('_hi')>0:
                regular_ex_4 = re.compile('_hi\.hichy')
                hichy_address = regular_ex_4.sub('.hichy',hichy_address)

            # this part is for '_hi' postfix scene file
            if mdl_ref_address.find('/pub/scenes/maya')>0:
                regular_ex_4 = re.compile('/pub/scenes/maya')
                hichy_address = regular_ex_4.sub('/pub/hichy',hichy_address)

            # print hichy_address
            mdl_hichy_format_address_dict[mdl_ref_address_key] = hichy_address


        # 1. read hichy format file
        # 2. put all hichy data in dict with namespace by key
        mdl_hichy_format_data = {}
        try:
            for mdl_hichy_address_key in mdl_hichy_format_address_dict:
                dir_path_hichy=os.path.dirname(mdl_hichy_format_address_dict[mdl_hichy_address_key])
                if not os.path.exists(dir_path_hichy):
                    print('there is no hichy folder')
                with open(mdl_hichy_format_address_dict[mdl_hichy_address_key], "rb") as p:
                    mdl_hichy_format_data[mdl_hichy_address_key] = pickle.load(p)
        except Exception as e:
            print(e)
            error_msg = 'There is no mdl team shapes info, need to check mdl pub data(hichy)'
            self.add_custom_warnning('', error_msg, "error", '')
            self.warn_count += 1




        # 1. get all transform groups and shapes
        # 2. put all transform groups and shapes in dict with namespace by key
        # 3. all_shape info must not include namespace, root node name, deformed ...
        # 4. standard is 'assetname_GRP'
        no_ns_ani_mdl_shapes_data = {}
        all_ref_cache_list =  neon.get_all_namespaces()
        for cache_target in all_ref_cache_list:
            if cache_target in mdl_hichy_format_data:
                if self.step_data == 'lookdev':
                    cache_target_root = targets
                    ldv_all_shape = cmds.ls(cache_target_root, dag =True, long=True)
                    if cache_target_root[0].endswith('_hi'):
                        asset_name = LUCY.get_assetname()
                        removed_target = '|{0}_{1}_hi'.format(asset_name, self.step_data)
                        prefix_removed_all_shape=self.remove_prefix_in_data(removed_target,ldv_all_shape)
                        no_ns_ani_mdl_shapes_data[cache_target] = prefix_removed_all_shape
                    elif cache_target_root[0].endswith('_GRP'):
                        prefix_removed_and_deform_except_all_shape = self.removeshape_Deform_posfix_in_data(ldv_all_shape)
                        no_ns_ani_mdl_shapes_data[cache_target] = prefix_removed_and_deform_except_all_shape

                elif self.step_data == 'rigging':
                    asset_name = LUCY.get_assetname()
                    target_s_children = cmds.listRelatives(targets[0], children=True)

                    # check geo grp node in hierarchy
                    if 'geo' not in target_s_children:
                        error_msg = 'There is no geo grp'
                        self.add_custom_warnning('obj', error_msg, "error", 'obj')
                        self.warn_count += 1
                        return

                    # normally geo check
                    if targets[0].endswith('_hi'):
                        cache_target_root = '{0}_geo'.format(asset_name)
                        removed_target = '|{0}_{1}_hi|{0}_geo|{0}_mdl_hi'.format(asset_name, self.step_data)
                    elif targets[0].endswith('_rig'):
                        cache_target_root = 'geo'
                        removed_target = '|{0}_{1}|geo'.format(asset_name, self.step_data)

                    rig_all_shape = cmds.ls(cache_target_root, dag =True, long=True)
                    prefix_removed_all_shape=self.remove_prefix_in_data(removed_target,rig_all_shape)
                    prefix_removed_and_deform_except_all_shape = self.removeshape_Deform_posfix_in_data(prefix_removed_all_shape)
                    
                    # pprint.pprint(prefix_removed_and_deform_except_all_shape)
                    no_ns_ani_mdl_shapes_data[cache_target] = prefix_removed_and_deform_except_all_shape

                elif self.step_data in ['animation','layout']:
                    self.remove_target_namespace = cache_target+":"
                    namespace_splited_list = cache_target.split('_')
                    asset_name = namespace_splited_list[0]


                    cache_target_GRP_node_name = '{0}:{1}_GRP'.format(cache_target, asset_name)
                    cache_target_RIG_node_name = '{0}:{1}_rig'.format(cache_target, asset_name)

                    # if scn.get_project() in ['2019_08_millenniumUnderSea','2019_06_apollo']:
                    #     pass
                    # else:
                    # check there is wrong group name
                    check_parent_list = cmds.listRelatives(cache_target_GRP_node_name, parent=True, fullPath=True)
                    check_ancestor_name = check_parent_list[0].split('|')
                    check_ancestor_name = check_ancestor_name[1]
                    if '_groupAsset' in check_ancestor_name:
                        pass
                    elif check_ancestor_name != cache_target_RIG_node_name:
                        error_msg = 'There is wrong grp name(top node). need to remove that'
                        self.add_custom_warnning(check_ancestor_name, error_msg, "error", check_ancestor_name)
                        self.warn_count += 1
                        return

                    # nomally geo check
                    ani_all_shape = cmds.ls(cache_target_GRP_node_name, dag =True, long=True)

                    namesapce_removed_all_shape = self.remove_namespace_in_data(self.remove_target_namespace, ani_all_shape)
                    
                    if namesapce_removed_all_shape[0].find('_mdl_hi')>0:
                        remove_target_prefix = '|{0}_rig_hi|{0}_geo|{0}_mdl_hi'.format(asset_name)
                    elif namesapce_removed_all_shape[0].find('_groupAsset')>0:
                        groupAsset_name = namesapce_removed_all_shape[0].split('|')[1]
                        remove_target_prefix = '|{0}|{1}_rig|geo'.format(groupAsset_name, asset_name)
                    else:
                        remove_target_prefix = '|{0}_rig|geo'.format(asset_name)
                    prefix_removed_all_shape = self.remove_prefix_in_data(remove_target_prefix, namesapce_removed_all_shape)

                    posfix_Deformed_removed_all_shape = self.removeshape_Deform_posfix_in_data(prefix_removed_all_shape)
                    no_ns_ani_mdl_shapes_data[cache_target] = posfix_Deformed_removed_all_shape






        for key in no_ns_ani_mdl_shapes_data:
            no_ns_cur_step_mdl_shapes = no_ns_ani_mdl_shapes_data[key]
            mdl_hichy_shapes = mdl_hichy_format_data[key]

            if len(mdl_hichy_shapes) == 0:
                error_msg = 'There is no mdl team shapes info, need to check mdl pub data(hichy)'
                self.add_custom_warnning('', error_msg, "error", '')
                self.warn_count += 1

            if len(no_ns_cur_step_mdl_shapes) == 0:
                error_msg = 'Current geo is not identified, need to check geo name in outliner'
                self.add_custom_warnning('', error_msg, "error", '')
                self.warn_count += 1

            unmatched_hichy_in_ref_geo = collections.Counter(no_ns_ani_mdl_shapes_data[key]) - collections.Counter(mdl_hichy_format_data[key])
            unmatched_hichy_in_hichy_geo = collections.Counter(mdl_hichy_format_data[key]) - collections.Counter(no_ns_ani_mdl_shapes_data[key])

            if unmatched_hichy_in_ref_geo:
                for mesh in unmatched_hichy_in_ref_geo:
                    address_component = mesh.split('|')
                    error_msg = "{0}: {1}:geo is not latest mesh".format(self.step_data.upper(),key)
                    shape_name = address_component[-1]
                    if len(shape_name) == 0:
                        continue
                    else:
                        self.add_custom_warnning(shape_name, error_msg, "error", shape_name)
                        self.warn_count += 1
            else:
                print('Geo check clear!')
                self.clear_items += no_ns_ani_mdl_shapes_data[key]

            if unmatched_hichy_in_hichy_geo:
                for mesh in unmatched_hichy_in_hichy_geo:
                    address_component = mesh.split('|')
                    error_msg = "MDL: {0}: the latest MDL mesh is updated".format(key)
                    shape_name = address_component[-1]
                    if len(shape_name) == 0:
                        continue
                    else:
                        self.add_custom_warnning(shape_name, error_msg, "error", shape_name)
                        self.warn_count += 1
            else:
                print('Geo check clear!')
                self.clear_items += mdl_hichy_format_data[key]

        if self._err_list:
            self.add_items(self._err_list)


    def is_all_clear(self):
        self._err_list = []
        return self.warn_count == 0


    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        # self.add_item(msg, "Clear", "clear")
        self.add_items([["", msg]])
