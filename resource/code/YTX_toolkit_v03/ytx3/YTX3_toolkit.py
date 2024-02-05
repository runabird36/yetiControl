import sys
import maya.cmds as cmds
from PySide2.QtWidgets import (QMessageBox)

from pprint import pprint
from qt_material import apply_stylesheet

try:
    from maya_md import yt_py
except:
    sys.path.append("/usersetup/linux/module")
    from maya_md import yt_py

def show_msg_box(_msg :str) -> None:
    info_box = QMessageBox()
    info_box.setWindowTitle("YTX3")
    info_box.setText(_msg)
    info_box.setStandardButtons(QMessageBox.Ok)
    apply_stylesheet(info_box, "dark_teal.xml")
    info_box.exec_()



def delete_cv_val() -> None:
    all_yeti_list = cmds.ls(sl=True, ni=True, dag=True, l=True, type='pgYetiMaya')
    basemesh_list = []
    for _y_node in all_yeti_list:
        _linked_node_list = cmds.listConnections(_y_node, d=False, s=True, sh=True)
        
        for _linked_node in _linked_node_list:
            _node_type = cmds.nodeType(_linked_node)
            if _node_type == 'mesh':
                basemesh_list.append(_linked_node)


    basemesh_list = list(set(basemesh_list))
    cluster_res = cmds.cluster(basemesh_list)
    print(cluster_res)
    cmds.delete(cluster_res)

    for basemesh in basemesh_list:
        tf_node = cmds.listRelatives(basemesh, p=True, f=True)[0]
        shapes = cmds.listRelatives(tf_node, c=True, s=True, f=True)
        for _sh in shapes:
            if "Orig" in _sh:
                print(_sh)
                cmds.delete(_sh)


    cmds.select(cl=True)
    cmds.select(all_yeti_list)





def get_shortname(l_name :str) -> str:
    return l_name.split("|")[-1]


# def find_exact_longname(s_name :str, tar_root_name :str) -> str:
#     to_target_mesh = ""
#     for check_tar in cmds.ls(f"*{s_name}*", l=True, ni=True):
#         if tar_root_name in check_tar:
#             to_target_mesh = check_tar
#             break
#     return to_target_mesh

def find_exact_longname(s_name :str, tar_root_name :str) -> str:
    to_target_mesh = ""
    for check_tar in cmds.ls(f"*{s_name}*", l=True, ni=True):
        
        if check_tar.startswith(f"{tar_root_name}|"):
            
            to_target_mesh = check_tar
            break

    return to_target_mesh

class AssignControl():
    def __init__(self, *args) -> None:
        print(args)
        self.yeti_list      = args[0]
        yeti_transform_node = cmds.listRelatives(self.yeti_list[0], p=True, f=True)[0]
        self.yeti_root_node = cmds.listRelatives(yeti_transform_node, p=True, f=True)[0]
        self.anim_cache     = args[1]
        self.curve_is_ok    = args[2]
        self.input_ns_num   = args[3]




    def run(self) -> None:
        vis_tar_list = []

        asset_info          = self.find_info()
        self.pre_execute(asset_info, vis_tar_list)




        mesh_is_connected   = self.connect_mesh(asset_info)
        if mesh_is_connected == False:
            return
        
        if self.curve_is_ok == True:
            cv_is_connected     = self.connect_cv(asset_info)
            if cv_is_connected == False:
                return
        

        trs_is_connected    = self.connect_trs()
        if trs_is_connected == False:
            return
        



        self.post_execute(vis_tar_list)

        ns_is_updated       = self.update_ns(asset_info)
        if ns_is_updated == False:
            return

        

    def pre_execute(self, asset_yeti_info :list[dict], vis_tar_list :list) -> None:
        
        geo_root_node   = ""
        yeti_root_node  = ""
        grm_root_node   = ""
        for asset_yeti in asset_yeti_info:
            yeti_node    = asset_yeti.get("YETI")
            mesh_list    = asset_yeti.get("BASEMESH_LIST")
            grm_list     = asset_yeti.get("GRM_LIST")
            
            vis_tar_list.append(yeti_node)
            vis_tar_list.extend(mesh_list)
            vis_tar_list.extend(grm_list)
            
            cv_exists    = asset_yeti.get("CV_EXISTS")
            set_list      = []
            if cv_exists == True:
                set_list = asset_yeti.get("CV_LIST")
                cvs         = cmds.sets(set_list, query=True)
                cv_grp_name = cmds.listRelatives(cvs[0], p=True, f=True)[0]
                vis_tar_list.append(cv_grp_name)

            if yeti_root_node == "":
                yeti_transform_node = cmds.listRelatives(yeti_node, p=True, f=True)[0]
                yeti_root_node      = cmds.listRelatives(yeti_transform_node, p=True, f=True)[0]
            if grm_root_node == "" and grm_list != []:
                grm_transform_node  = cmds.listRelatives(grm_list[0], p=True, f=True)[0]
                grm_root_node       = cmds.listRelatives(grm_transform_node, p=True, f=True)[0]
            if geo_root_node == "":
                word_elements = yeti_root_node.split("|")
                word_elements.pop()
                word_elements.append("geo")
                geo_root_node = "|".join(word_elements)

        
        vis_tar_list.append(geo_root_node)
        vis_tar_list.append(yeti_root_node)
        vis_tar_list.append(grm_root_node)



        for _node in vis_tar_list:
            cmds.setAttr(f"{_node}.visibility", False)

        # print(vis_tar_list)


    def post_execute(self, vis_tar_list :list) -> None:
        for _node in vis_tar_list:
            if _node.endswith("|geo") == True:
                continue
            if _node.endswith("|grm") == True:
                continue
            cmds.setAttr(f"{_node}.visibility", True)
        

    def find_info(self) -> list:
        
        asset_info_list = []

        all_yeti_list = self.yeti_list
        for _y_node in all_yeti_list:
            
            info_dict_of_yeti = {"YETI":_y_node, "BASEMESH_LIST":[], "GRM_LIST":[], "CV_LIST":[], "CV_EXISTS":False}
            
            _linked_node_list = cmds.listConnections(_y_node, d=False, s=True, sh=True)
            
            for _linked_node in _linked_node_list:
                _node_type = cmds.nodeType(_linked_node)
                if _node_type == 'mesh':
                    basemeshes = info_dict_of_yeti.get("BASEMESH_LIST")
                    basemeshes.append(_linked_node)
            
                elif _node_type == 'pgYetiGroom':
                    grms       = info_dict_of_yeti.get("GRM_LIST")
                    grms.append(_linked_node)

            
                elif _node_type == 'objectSet':
                    info_dict_of_yeti["CV_EXISTS"] = True
                    cvs        = info_dict_of_yeti.get("CV_LIST")
                    cvs.append(_linked_node)
                    

            asset_info_list.append(info_dict_of_yeti)

        return asset_info_list
                    
    def connect_mesh(self, asset_yeti_info :list[dict]) -> bool:
        for asset_yeti in asset_yeti_info:
            basemesh_list = asset_yeti.get("BASEMESH_LIST")

            # 하나의 yeti 노드에 여러개의 basemesh 있게되면 for문으로 추후 업데이트
            basemesh = basemesh_list[0]
            base_short_name = get_shortname(basemesh)
            to_target_mesh  = basemesh


            from_target_mesh = ""
            from_target_mesh = find_exact_longname(base_short_name, self.anim_cache)
          
            if from_target_mesh == "":
                show_msg_box(f"{self.anim_cache} 에 basemesh가 없습니다.")
                return False
            
            try:
                cmds.connectAttr(f"{from_target_mesh}.outMesh", f"{to_target_mesh}.inMesh", f=True)
            except Exception as e:
                print(str(e))
                show_msg_box("메쉬 .in / .out 연결하는데 있어 에러가 생겼습니다.")
                return False
        return True

    def connect_cv(self, asset_yeti_info :list[dict]) -> bool:
        for asset_yeti in asset_yeti_info:
            asset_cv_list = asset_yeti.get("CV_LIST")

            if asset_cv_list == []:
                continue

            for asset_cv_set in asset_cv_list:
                cv_grp_name = ""
                cvs         = cmds.sets(asset_cv_set, query=True)
                cv_grp_names= cmds.listRelatives(cvs, p=True, f=True)
                cv_grp_names= list(set(cv_grp_names))
                for cv_grp_name in cv_grp_names:
                    # cv_shapes   = cmds.ls(cvs, l=True, ni=True, dag=True, shapes=True)
                    cvs         = cmds.listRelatives(cv_grp_name, c=True, f=True)
                    cv_shapes   = cmds.ls(cvs, l=True, ni=True, dag=True, shapes=True)
                    cv_shapes.sort()

                    
                    s_name = cv_grp_name.split('|')[-1]
                    from_target_cvgrp = find_exact_longname(s_name, self.anim_cache)                
                    from_cvs = cmds.listRelatives(from_target_cvgrp, c=True, f=True)
                    from_cv_shapes   = cmds.ls(from_cvs, l=True, ni=True, dag=True, shapes=True)
                    from_cv_shapes.sort()

                    if len(cv_shapes) != len(from_cv_shapes):
                        show_msg_box(f"커브 갯수가 맞지 않습니다.")
                        return False
                    

                    for f_cv, t_cv in zip(from_cv_shapes, cv_shapes):
                        try:
                            print(f"{f_cv}  ------> {t_cv}")
                            cmds.connectAttr(f"{f_cv}.worldSpace", f"{t_cv}.create")
                        except:
                            print("Warnning : fail to connect cv from worldSpace to create")
                            pass

        return True

    def connect_trs(self) -> bool:
        try:
            cmds.connectAttr(f"{self.anim_cache}.translate", f"{self.yeti_root_node}.translate")
            cmds.connectAttr(f"{self.anim_cache}.rotate", f"{self.yeti_root_node}.rotate")
            # cmds.connectAttr(f"{self.anim_cache}.s", f"{self.yeti_transform_node}.s")
            return True
        except:
            return False
        
        pass
        

    def update_ns(self, asset_yeti_info :dict[list]) -> bool:
        for asset_yeti in asset_yeti_info:
            yeti_shape_name = asset_yeti.get("YETI")
            yeti_tf_name    = cmds.listRelatives(yeti_shape_name, p=True, f=True)[0]
            asset_set_list  = asset_yeti.get("CV_LIST")

            
            asset_set_list = list(set(asset_set_list))
            


            to_yeti_tf_name = f"{yeti_tf_name}_{self.input_ns_num}"
            to_asset_set_list = []
            for cv_set in asset_set_list:
                to_asset_set_list.append(f"{cv_set}_{self.input_ns_num}")


            
            # Start rename
            if asset_set_list != []:
                for f_set, t_set in zip(asset_set_list, to_asset_set_list):
                    # print(f"{f_set} --> {t_set}")
                    cmds.rename(f_set, t_set)

                    yt_py.update_set_name(yeti_shape_name, f_set, t_set)
            
            to_yeti_tf_s_name = to_yeti_tf_name.split("|")[-1]
            # print(f"{yeti_tf_name} --> {to_yeti_tf_s_name}")
            cmds.rename(yeti_tf_name, to_yeti_tf_s_name)
            
