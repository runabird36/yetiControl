import maya.cmds as cmds
import re

'''
ToggleAll -> 
(On)
1. basemesh를 복사하여 원본 -> 복사본으로 outMesh >> inMesh 연결 [모든 쉐잎 중 (intermediateObject ==0) 인것으로 특정하는 것이 오류가 덜 날 것 같습니다.]
2. 원본을 assetname_GRP 밖으로 꺼내어 어딘가에 두고, translate/rotate/scale을(0,0,0,0,0,0,1,1,1)로 만든 후 hide
3. 복사본의 숏네임을 원본과 같게 설정 (숫자가 자동으로 붙는 것을 수정)
4. 기존과 동일하게 TRS연결

(Off)
TRS연결끊고,
복사본 지우고,
원본을 기존하이라키대로 수정
'''


def get_tfname_from_mesh(mesh_sn_name :str) -> str:
    if "Shape" not in mesh_sn_name:
        return mesh_sn_name
    
    return mesh_sn_name.split("Shape")[0]

def get_mesh_from_tf(tf_name :str) -> str:
    return cmds.listRelatives(tf_name, f=True, c=True, typ="mesh")[0]

def find_long_name(s_name :str) -> str:
    check_list = cmds.ls(s_name, l=True)

    for check_tar in check_list:
        if "_yetiGRP" in check_tar:
            return check_tar
    
    return None


def check_and_make_originGRP(node_name :str) -> None:
    def find_root(node :str) -> str:
        if "|" not in node:
            node = find_long_name(node)
        word_elements = []
        for element in node.split("|"):
            word_elements.append(element)
            if "_yetiGRP" in element:
                break
        return "|".join(word_elements)
    
    origin_grp_name = "originGRP"
    root_name       = find_root(node_name)

    check_l_name = f"{root_name}|{origin_grp_name}"
    if cmds.objExists(check_l_name) == True:
        pass
    else:
        cmds.group(n=origin_grp_name, p=root_name, em=True)

    return check_l_name



def get_selected_yeti() -> list:
    return cmds.ls(sl=True, ni=True, dag=True, typ="pgYetiMaya")



def find_link_info(yeti_nodes :list) -> list:
    yeti_infos = []
    for y_node in yeti_nodes:
        _linked_node_list = cmds.listConnections(y_node, d=False, s=True, sh=True)
        temp_dict = {"YETI":"", "BASEMESH":[]}
        temp_dict["YETI"] = y_node
        for check_tar in _linked_node_list:
            if cmds.nodeType(check_tar) == "mesh":
                temp_dict["BASEMESH"].append(check_tar)

        yeti_infos.append(temp_dict)

    return yeti_infos




def check_already_duplicated(where :str, check_tar :str) -> bool:
    find_res = cmds.ls(cmds.listRelatives(where, c=True), sn=True, dag=True, ni=True, typ="mesh")
    
    if find_res == []:
        return False
    
    for candidate in find_res:
        if check_tar in candidate:
            return True
    return False




def connect_mesh(from_target_mesh :str, to_target_mesh :str) -> bool:
        
    try:
        cmds.connectAttr(f"{from_target_mesh}.outMesh", f"{to_target_mesh}.inMesh", f=True)
    except Exception as e:
        print(str(e))
        
        return False



def connect_trs(from_tf, to_tf) -> bool:
    try:
        cmds.connectAttr(f"{from_tf}.translate", f"{to_tf}.translate")
        cmds.connectAttr(f"{from_tf}.rotate", f"{to_tf}.rotate")
        # cmds.connectAttr(f"{self.anim_cache}.s", f"{self.yeti_transform_node}.s")
        return True
    except:
        return False
    
    pass






def run() -> None:
    yeti_nodes = get_selected_yeti()
    link_info = find_link_info(yeti_nodes)


    make_default_tars   = []
    hide_tars           = []
    for info in link_info:
        yeit_name     = info.get("YETI")  
        basemesh_list = info.get("BASEMESH")
        originGRP_grp = check_and_make_originGRP(yeit_name)
        hide_tars.append(originGRP_grp)

        for basemesh in basemesh_list:
            if check_already_duplicated(originGRP_grp, basemesh) == False:
                l_name = find_long_name(basemesh)
                duplicated_mesh = cmds.duplicate(l_name)
                duplicated_mesh = duplicated_mesh[0]
                cmds.parent(l_name, originGRP_grp)
                tf_name = get_tfname_from_mesh(basemesh)
                orign_mesh = f"{originGRP_grp}|{tf_name}|{basemesh}"

                render_mesh = get_mesh_from_tf(duplicated_mesh)
                
                connect_mesh(orign_mesh, render_mesh)


                if re.search(r"\d+$", duplicated_mesh):
                    render_tf = re.sub(r"\d+$", "", duplicated_mesh)
                    cmds.rename(duplicated_mesh, render_tf)
                else:
                    render_tf = duplicated_mesh

                make_default_tars.append(f"{originGRP_grp}|{render_tf}")
            
    
    for tf_node in make_default_tars:
        cmds.setAttr(f"{tf_node}.translateX", 0)
        cmds.setAttr(f"{tf_node}.translateY", 0)
        cmds.setAttr(f"{tf_node}.translateZ", 0)

        cmds.setAttr(f"{tf_node}.rotateX", 0)
        cmds.setAttr(f"{tf_node}.rotateY", 0)
        cmds.setAttr(f"{tf_node}.rotateZ", 0)


    hide_tars = list(set(hide_tars))
    for hide_tar in hide_tars:
        print(hide_tar)
        print(f"{hide_tar}.visibility")
        cmds.setAttr(f"{hide_tar}.visibility", 0)



