import maya.cmds as cmds
import os, pprint, re, collections

import checker
# reload (checker)
from checker import Checker


from maya_md import neon


class DeformedChecker(Checker):

    warn_count = 0
    clear_items = []
    def __init__(self):
        Checker.__init__(self)
        self.set_title("Shape deformed Check")
        self.except_list = ['instancer', 'nParticle', 'nucleus', 'pointEmitter', 'pointLight', 'nurbsCurve', 'gpuCache']



    def execute(self, targets):
        root_grp = targets[0]
        error_content = []
        neon.select_asset(root_grp)
        root_grp = root_grp.replace('_rig', '_GRP')


        # first case : in mdl, change shape name and then, transform have two shapes
        all_shape = cmds.ls(root_grp, dagObjects = True, shapes = True, v=True)
        check_deuplicated_shape_dict ={}


        for shape in all_shape:
            shape_type = cmds.objectType(shape)
            if shape_type in self.except_list:
                continue
            target_parent_list = cmds.listRelatives(shape, p = True)
            target_parent = target_parent_list[0]
            if target_parent in check_deuplicated_shape_dict:
                target_child_list = check_deuplicated_shape_dict[target_parent]
                target_child_list.append(shape)
            else:
                check_deuplicated_shape_dict[target_parent] = [shape]
        # pprint.pprint(check_deuplicated_shape_dict)


        re_ex_deformedOrig = re.compile('DeformedOrig')
        re_ex_deform = re.compile('Deformed')
        re_ex_orig = re.compile('Orig')
        re_ex_orig_with_num = re.compile('\d+Orig')
        re_ex_num = re.compile('\d+$')
        for check_target in check_deuplicated_shape_dict:
            target_transform_s_shapes_list = check_deuplicated_shape_dict[check_target]
            delete_list = []
            update_list = []
            for shape in target_transform_s_shapes_list:
                if shape.find('|')>0:
                    delete_list.append(shape)
                    shape_component_list = shape.split('|')
                    shape = shape_component_list[-1]

                if re_ex_deformedOrig.search(shape):
                    result=re_ex_deformedOrig.sub('', shape)
                    result = re_ex_num.sub('', result)
                    update_list.append(result)
                    delete_list.append(shape)
                elif re_ex_deform.search(shape):
                    result=re_ex_deform.sub('', shape)
                    result = re_ex_num.sub('', result)
                    update_list.append(result)
                    delete_list.append(shape)
                elif re_ex_orig.search(shape):
                    result=re_ex_orig.sub('', shape)
                    result = re_ex_num.sub('', result)
                    update_list.append(result)
                    delete_list.append(shape)
                elif re_ex_orig_with_num.search(shape):
                    result=re_ex_orig_with_num.sub('', shape)
                    result = re_ex_num.sub('', result)
                    update_list.append(result)
                    delete_list.append(shape)
                elif shape.endswith('Shape'):
                    update_list.append(shape)

            target_transform_s_shapes_list.extend(update_list)

            for del_target in delete_list:
                print(del_target)
                try:
                    target_transform_s_shapes_list.remove(del_target)
                except Exception as e:
                    print(str(e))




        # pprint.pprint(check_deuplicated_shape_dict)

        for check_target in check_deuplicated_shape_dict:
            target_transform_s_shapes_list = check_deuplicated_shape_dict[check_target]
            
            check_result = set(target_transform_s_shapes_list)
            
            target_shape_list = list(check_result)
            print(target_shape_list)
            try:
                target_shape_without_deformed = target_shape_list[0]
                target_shape = '{0}Deformed'.format(target_shape_without_deformed)
                err_target_parent_list = cmds.listRelatives(target_shape, p = True)
                err_target_parent = err_target_parent_list[0]
            except Exception as e:
                print(e)
                try:
                    target_shape = target_shape_list[0]
                    err_target_parent_list = cmds.listRelatives(target_shape, p = True)
                    err_target_parent = err_target_parent_list[0]
                except Exception as e:
                    print(e)
                    target_shape = target_shape_list[1]
                    err_target_parent_list = cmds.listRelatives(target_shape, p = True)
                    err_target_parent = err_target_parent_list[0]

            if len(check_result) >= 2:
                self.add_warnning(err_target_parent, 'has multiple shapes', "error",err_target_parent)
                self.warn_count += 1
            elif len(check_result) == 1:
                self.clear_items.append(err_target_parent)




        # second case : in mdl, change transform node name, and then fosterParent node is created
        all_roots_in_outliner = neon.get_all_roots()

        for root in all_roots_in_outliner:
            root_type = cmds.objectType(root)
            if root_type == 'fosterParent':
                self.add_warnning(root, 'has multiple shapes', "error",root)
                self.warn_count += 1
            else:
                self.clear_items.append(root)







    def is_all_clear(self):
        return self.warn_count == 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        self.add_item(msg, "Clear", "clear")
