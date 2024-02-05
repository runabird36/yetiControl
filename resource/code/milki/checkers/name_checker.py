import maya.cmds as cmds
import os, re
import collections
from importlib import reload
import checker
reload (checker)
from checker import Checker


from maya_md import neon
from general_md_3x import LUCY




class NameChekcer(Checker):

    warn_count = -1
    clear_items = []

    def __init__(self):
        Checker.__init__(self)
        self.set_title("Name Check")

        self.warnings = []
        # self.except_list = ['nurbsCurve', 'instancer', 'nParticle', 'nucleus', 'pointEmitter', 'pointLight']
        self.except_list = ['instancer', 'nParticle', 'nucleus', 'pointEmitter', 'pointLight', 'nurbsCurve', 'gpuCache', 'aiMeshLight']


    def filter_shape(self, all_shape):

        filtered_shape = []
        for _shape in all_shape:

            if cmds.nodeType(_shape) == 'lattice' or cmds.nodeType(_shape) == 'baseLattice':
                if 'Orig' in _shape:
                    filtered_shape.append(_shape)

                _connect_info_list = list(set(cmds.listConnections(_shape, d=True)))
                ffd_list = cmds.ls(_connect_info_list, type='ffd')
                linked_mesh_list = []
                for _ffd in ffd_list:
                    tar_objectSet_list = cmds.listConnections(_ffd, d=True, type='objectSet')
                    tar_mesh_list = cmds.listConnections(tar_objectSet_list, d=True, type='mesh')
                    linked_mesh_list.extend(tar_mesh_list)
                linked_mesh_list = list(set(linked_mesh_list))
                for _mesh in linked_mesh_list:
                    _res = cmds.ls('*{0}Shape*Orig*'.format(_mesh))
                    filtered_shape.extend(_res)


            filtered_shape = cmds.ls(list(set(filtered_shape)), l=True)




        return list(set(all_shape) - set(filtered_shape))


    def check_asset_name_in_hierarchy(self,asset_name, each_mesh):
        '''condition 2 : start with asset name in all tree address(object)'''
        name_list = each_mesh.split('_')
        asset_name_idx = 0
        if name_list[asset_name_idx] != asset_name:
            self.condition_second_error_list.append([each_mesh ," is not started with " + asset_name])
        else:
            self.clear_items.append(each_mesh)

    def check_match_transform_mesh(self, each_transform, each_mesh):
        '''condition 3 : all mesh type name is started with transform name'''
        if each_mesh.startswith(each_transform) is False:
            self.condition_third_error_list.append([each_mesh , "transform name and shape name is not same" ])
        else:
            self.clear_items.append(each_mesh)

    def check_name_error_GEO(self, each_transform, each_mesh):
        '''condition 4 : mesh name and transform are ended with "GEO" '''
        trasform_name_list = each_transform.split('_')
        transform_check_target = trasform_name_list[-1]
        shape_name_list = each_mesh.split('_')
        shape_check_target = shape_name_list[-1]

        # target_child_type = cmds.objectType(each_mesh)
        # if target_child_type == 'nurbsCurve':
        #     self.clear_items.append(each_transform )
        #     return

        if transform_check_target == 'GEO' and shape_check_target == 'GEOShape' :
            self.clear_items.append(each_transform + " and " + each_mesh)
        else:
            self.condition_fourth_error_list.append([each_mesh, "GEO name error : the mesh must be end with GEO or GEOShape"])

    def check_name_error_GRP_and_GEO(self,each_transform):
        '''condition 4 : mesh name and transform are ended with "GRP" '''
        target_child=cmds.listRelatives(each_transform, c=True)
        if target_child is None:
            target_child = each_transform
            self.condition_sixth_error_list.append([target_child,"GRP has no GEO"])
            return
        try:
            target_child_type = cmds.objectType(target_child[0])
        except Exception as e:
            self.condition_fifth_error_list.append([target_child[0]," is not unique name "])
            return

        transform_name_list = each_transform.split('_')
        check_target_name = transform_name_list[-1]

        # if target_child_type == 'nurbsCurve':
        #     self.clear_items.append(each_transform )
        #     return


        if target_child_type=='transform' and check_target_name == 'GRP':
            self.clear_items.append(each_transform )
        elif target_child_type=='mesh' and check_target_name == 'GEO' :
            self.clear_items.append(each_transform )
        elif target_child_type=='aiStandIn' and check_target_name == 'GEO':
            self.clear_items.append(each_transform )
        elif target_child_type == 'stroke' and check_target_name == 'GEO':
            self.clear_items.append(each_transform )
        elif target_child_type in ['baseLattice', 'lattice'] and check_target_name == 'GEO':
            self.clear_items.append(each_transform )
        elif target_child_type == 'nurbsCurve' and check_target_name == 'CRV':
            self.clear_items.append(each_transform )
        elif target_child_type == 'locator' and check_target_name == 'GEO':
            self.clear_items.append(each_transform )
        else:
            # Error Case
            if target_child_type == 'nurbsCurve':
                self.condition_fourth_error_list.append([each_transform, "CRV name error : curve must be end with CRV"])
            else:
                self.condition_fourth_error_list.append([each_transform, "GRP and GEO name error : must be end with GRP or GEO"])

    def check_unique_name(self, unique_check_list):
        '''condition 5 : mesh(shape) name should be unique'''
        unique_check_collection = []
        unique_check_collection = collections.Counter(unique_check_list)
        for key in unique_check_collection:
            if unique_check_collection[key] >= 2:
                self.condition_fifth_error_list.append([key," is not unique name "])
            else:
                self.clear_items.append(key)


    def get_error_list(self):
        whole_error_list = []

        error_second = self.condition_second_error_list
        error_third = self.condition_third_error_list
        error_fourth = self.condition_fourth_error_list
        error_fifth = self.condition_fifth_error_list
        error_sixth = self.condition_sixth_error_list

        if error_second:
            whole_error_list.extend(error_second)
        else:
            pass
            # whole_error_list.append([['second condition clear', None]])

        if error_third:
            whole_error_list.extend(error_third)
        else:
            pass
            # whole_error_list.append([['third condition clear', None]])

        if error_fourth:
            whole_error_list.extend(error_fourth)
        else:
            pass
            # whole_error_list.append([['fourth condition clear', None]])

        if error_fifth:
            whole_error_list.extend(error_fifth)
        else:
            pass
            # whole_error_list.append([['fifth condition clear', None]])

        if error_sixth:
            whole_error_list.extend(error_sixth)
        else:
            pass
            # whole_error_list.append([['sixth condition clear', None]])

        return whole_error_list



    def execute(self, targets):
        print('Execute name checker')
        self.warn_count = 0
        self.condition_second_error_list = []
        self.condition_third_error_list = []
        self.condition_fourth_error_list = []
        self.condition_fifth_error_list = []
        self.condition_sixth_error_list = []


        root_grp = targets[0]
        neon.select_asset(root_grp)
        all_shape = cmds.ls(root_grp, dagObjects = True, long = True, shapes = True)

        # filter shapes which in some case
        all_shape = self.filter_shape(all_shape)


        divider = '|'
        mesh_index = -1
        GEO_transform_index = -2
        asset_name = LUCY.get_assetname()
        unique_name_check_list = []
        for  shape in all_shape:
            objectType = cmds.objectType(shape)



            if objectType in self.except_list:
                continue

            shape_list = shape.split(divider)

            each_mesh = shape_list[mesh_index]
            each_transform = shape_list[GEO_transform_index]

            #condition 2
            self.check_asset_name_in_hierarchy(asset_name, each_mesh)
            # #condition 3
            # self.check_match_transform_mesh(each_transform, each_mesh)
            # #condition 4
            # self.check_name_error_GEO(each_transform, each_mesh)
            #condition 5
            unique_name_check_list.append(each_mesh)

        #condition 5
        self.check_unique_name(unique_name_check_list)

        transform_unique_check_list = []
        child_type = ''
        all_transform = cmds.ls(root_grp, dagObjects = True, transforms = True)
        for transform in all_transform:
            tranform_type = cmds.objectType(transform)

            if tranform_type in self.except_list:
                continue

            target_child_list = cmds.listRelatives(transform, c = True)

            try:
                geo_shape = target_child_list[0]
                child_type = cmds.objectType(geo_shape)
                if child_type in self.except_list:
                    continue
            except:
                pass

            # check that GRP is empty group
            target_child_list = cmds.listRelatives(transform, c = True)
            if target_child_list is None:
                self.condition_sixth_error_list.append([transform, "This is Empty!!"])
            elif len(target_child_list) == 0:
                self.condition_sixth_error_list.append([geo_shape, "GRP has no GEO(This is empty group)"])



            # if child_type in self.except_list:
            #     continue

            #condition 2
            self.check_asset_name_in_hierarchy(asset_name, transform)

            #condition 4
            self.check_name_error_GRP_and_GEO(transform)
            #condition 5
            if transform.find('|')>0:
                transform_list = transform.split(divider)
                transform = transform_list[-1]
            transform_unique_check_list.append(transform)

        #condition 5
        self.check_unique_name(transform_unique_check_list)


        #print error
        whole_error_list = self.get_error_list()
        if whole_error_list == []:
            self.warn_count = 0
        else:

            self.add_items(whole_error_list)
            self.warn_count = len(whole_error_list)

    def is_all_clear(self):
        return self.warn_count == 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        self.add_item(msg, "Clear", "clear")


    def virtual_clear(self):
        self.warn_count = 0
