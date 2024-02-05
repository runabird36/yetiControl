import maya.cmds as cmds

# def get_object_set_elements(object_set_node):
#     # Get the elements of the objectSet node
#     elements = cmds.sets(object_set_node, query=True)
#     return elements

# # Usage example:
# object_set_node = "kadanLow_hair_CV_set"  # Replace with the name of your objectSet node
# elements = get_object_set_elements(object_set_node)



# res = cmds.listRelatives(elements[0], ap=True, f=True)
# print(res)


# # if elements:
# #     print("ObjectSet Elements:", elements)
# # else:
# #     print("No elements found in the objectSet.")


# tar = "kadan_hair_groomShape_strand_Shape0"
# tar = cmds.ls(tar, l=True)[0]

# tar02 = "curveShape1"

# # for i in cmds.listAttr(tar):
# #     if "space" in i.lower():
# #         print(i)
# #         print(f"{tar}.worldSpace")
# #         print(cmds.getAttr(f"{tar}.worldSpace"))


# tar = "|kadanLow_yeti_GRP|geo|kadanLow_GRP|kadanLow_CV_GRP|kadanLow_hair_CV|kadan_hair_groomShape_strand_9|kadan_hair_groomShape_strand_Shape9"
# tar02 = "|kadanLow_GRP1|kadanLow_CV_GRP1|kadanLow_hair_CV|kadan_hair_groomShape_strand_9|kadan_hair_groomShape_strand_Shape9"

# # cmds.select(tar02)
# cmds.connectAttr(f"{tar02}.worldSpace", f"{tar}.create")




# from re import search

# def find_exact_longname(s_name :str, tar_root_name :str) -> str:
#     to_target_mesh = ""
#     for check_tar in cmds.ls(f"*{s_name}*", l=True, ni=True):
        
#         if check_tar.startswith(f"{tar_root_name}|"):
            
#             to_target_mesh = check_tar
#             break

#     return to_target_mesh


# s_name = "kadan_front_groomShape_strand_0"
# tar_root_name = "|kadanLow_GRP"
# res = find_exact_longname(s_name, tar_root_name)
# print(res)



import maya.cmds as cmds
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

