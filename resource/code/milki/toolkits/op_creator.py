from importlib import reload


import maya.cmds as cmds
from maya_md import neon
from maya_md import op
reload(op)

def get_arnold_visibility(shape):
    attrList = ['primaryVisibility', 'castsShadows', 'aiVisibleInDiffuseReflection', 'aiVisibleInSpecularReflection', 'aiVisibleInDiffuseTransmission', 'aiVisibleInSpecularTransmission', 'aiVisibleInVolume', 'aiSelfShadows']
    value = 0

    if cmds.getAttr(shape + '.' + attrList[0]) == True:
        value += 1

    if cmds.getAttr(shape + '.' + attrList[1]) == True:
        value += 2

    if cmds.getAttr(shape + '.' + attrList[2]) == True:
        value += 4

    if cmds.getAttr(shape + '.' + attrList[3]) == True:
        value += 8

    if cmds.getAttr(shape + '.' + attrList[4]) == True:
        value += 16

    if cmds.getAttr(shape + '.' + attrList[5]) == True:
        value += 32

    if cmds.getAttr(shape + '.' + attrList[6]) == True:
        value += 64

    if cmds.getAttr(shape + '.' + attrList[7]) == True:
        value += 128

    #check if visibility attr is off.
    if cmds.getAttr(shape + '.visibility') == 0:
        value = 0

    return value

def get_arnold_visibility_groups(shapes):
    visList = []
    for shape in shapes:
        visibility_value = get_arnold_visibility(shape)
        if not visibility_value == 255:
            index = -1
            for r in range(len(visList)):
                if visibility_value in visList[r]:
                    index = r

            if index == -1:
                vis = [ [shape], visibility_value]
                visList.append(vis)
            else:
                visList[index][0].append(shape)

    return visList

def create(grp, assetName):
    #Selection from top asset group
    sel = cmds.listRelatives(ad=True, f=False, typ = 'transform')
    sel = grp
    #======================================================================
    #ROOT
    #======================================================================
    root_look_name = assetName + '_look'
    if cmds.objExists(root_look_name) == False:
        aiMLook = cmds.shadingNode('aiMerge', n = root_look_name, asPostProcess=True)
    else:
        aiMLook = root_look_name

    aiMCollection = cmds.shadingNode('aiMerge', n = assetName + '_collection', asPostProcess=True)
    op.connect_operator(aiMCollection, aiMLook)

    aiMAssignShd = cmds.shadingNode('aiMerge', n = assetName + '_shaderAssign', asPostProcess=True)
    op.connect_operator(aiMAssignShd, aiMLook)

    root_attr_name = assetName + '_attributes'
    if cmds.objExists(root_attr_name) == False:
        aiMAttr = cmds.shadingNode('aiMerge', n = root_attr_name, asPostProcess=True)
    else:
        aiMAttr = root_attr_name
    op.connect_operator(aiMAttr, aiMLook)



    #======================================================================
    #All COLLECTION
    #======================================================================
    end_names = []
    for shp in neon.get_all_shape_in_hierarchy(sel):
        end_name = "*{0}*".format(shp.split("|")[-1])
        if '_GEOShapeDeform' in end_name:
            end_name = end_name.replace('_GEOShapeDeform','_GEOShape')
        end_names.append(end_name)
    all_path = " or ".join(end_names)

    #newCollection = op.create_collection(assetName + '_all', op.get_path_selection_string(neon.get_all_shape_in_hierarchy(sel)), assetName + 'All')
    newCollection = op.create_collection(assetName + '_all', all_path, assetName + 'All')
    op.connect_operator(newCollection, aiMCollection)

    #======================================================================
    #ATTRIBUTES
    #======================================================================
    # #SetParameters - Subdivision
    # assignments = ["subdiv_type = 'catclark'", "subdiv_iterations = 2"]
    # newSetParemeter = op.create_setParameter(assetName + '_subdiv', "#" + assetName + 'All', assignments)
    # op.connect_operator(newSetParemeter, aiMAttr)
    #
    # #Arnold Visibility Mask
    # for visibilityGroup in get_arnold_visibility_groups( neon.get_all_shape_in_hierarchy( sel )):
    #
    #     collection_selection = op.get_path_selection_string(visibilityGroup[0])
    #     collection_name = assetName + '_visibility' + str(visibilityGroup[1])
    #     visibility_value = str(visibilityGroup[1])
    #
    #     newCollection = op.create_collection(collection_name, collection_selection, collection_name)
    #     op.connect_operator(newCollection, aiMCollection)
    #     newSetParemeter = op.create_setParameter(collection_name, "#" + collection_name, ['visibility = ' + visibility_value])
    #     op.connect_operator(newSetParemeter, aiMAttr)
    #
    # #Attr = aiOpaque
    # attrList = ['aiOpaque']
    # for attr in attrList:
    #     if not op.get_shapes_by_attr(sel, attr) == '':
    #         # shapes = op.get_shapes_by_attr(sel, attr)
    #         # end_names = []
    #         # for shp in shapes:
    #         #     end_name = "*{0}*".format(shp.split("|")[-1])
    #         #     if '_GEOShapeDeform' in end_name:
    #         #         end_name = end_name.replace('_GEOShapeDeform','_GEOShape')
    #         #     end_names.append(end_name)
    #         # op_path = " or ".
    #         newCollection = op.create_collection(assetName + '_' + attr, op.get_shapes_by_attr(sel, attr), assetName + '_' + attr)
    #         op.connect_operator(newCollection, aiMCollection)
    #         newSetParemeter = op.create_setParameter(assetName + '_' + attr, "#" + assetName + '_' + attr, ['opaque = False'])
    #         # op.connect_operator(newSetParemeter, aiMAttr)

    #======================================================================
    #SHADING NETWORK
    #======================================================================
    for shadingGroup in neon.get_shading_groups_in_hierarchy(sel):
        shaderName = neon.get_source(shadingGroup, 'surfaceShader')
        dispName = neon.get_source(shadingGroup, 'displacementShader')
        full_paths = []
        for fp in neon.get_assign_full_paths(shadingGroup):
            end_name = "*{0}*".format(fp.split("|")[-1])
            if '_GEOShapeDeform' in end_name:
                end_name = end_name.replace('_GEOShapeDeform','_GEOShape')

            full_paths.append(end_name)
        print(full_paths)

        #selection_paths = op.get_path_selection_string(full_paths)
        selection_paths = " or ".join(full_paths)

        #Create Collection
        newCollection = op.create_collection(shaderName, selection_paths, shaderName)
        op.connect_operator(newCollection, aiMCollection)

        #Create Shader Assign
        shdAssign = ['shader = ' '\"' + shaderName + '\"']
        if not dispName == None:
            # shdAssign.append('disp_map = ' '\"' + dispName + '.displacement' + '\"')
            shdAssign.append('disp_map = ' '\"' + dispName + '\"')
            

        newSetParemeter = op.create_setParameter(shaderName + '_shdAssign', "#" + shaderName, shdAssign)
        op.connect_operator(newSetParemeter, aiMAssignShd)

    #Exporting operators
    cmds.select(aiMLook)
    return aiMLook


# def pub_op(self):
#         try:
#             return oc.create(self.grp, self.asset_name)
#         except:
#             return None
