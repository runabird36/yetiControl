from importlib import reload
import checker
#reload (checker)
from checker import Checker
import maya.cmds as cmds
import tex_info_provider
reload (tex_info_provider)


import pprint


from maya_md import neon
from general_md_3x import LUCY





class NodeNameChecker(Checker):

    warn_count = 0
    clear_items = []
    err_list = []
    def __init__(self):
        Checker.__init__(self)
        self.set_title("Node Name Check")
        self.warnings = []
        self.err_list = []

    def check_assetName_in_node(self, check_target, asset_name):
        '''condition 2 : start with asset name in all tree address(object)'''
        asset_name_idx = 0

        name_list = check_target.split('_')
        # if len(name_list) <= 1:
        #      self.err_list.append(check_target)
        # elif name_list[asset_name_idx] != asset_name:
        #     self.err_list.append(check_target)
        # else:
        #     self.clear_items.append(check_target)

        if len(name_list) <= 1:
            self.err_list.append([check_target, " is not started with " + asset_name])
        elif name_list[asset_name_idx] != asset_name:
            self.err_list.append([check_target, " is not started with " + asset_name])
        else:
            self.clear_items.append(check_target)


    def execute(self, targets):
        self.warn_count = 0
        self.clear_items = []
        self.err_list = []

        asset_name = LUCY.get_assetname()
        assigned_sg = []


        grp_name = "{0}_GRP".format(asset_name)
        shapes_list =  cmds.ls(grp_name, dag=1,o=1,s=1)
        # get shading groups from shapes:
        shadingGrps = cmds.listConnections(shapes_list,type='shadingEngine')
        all_nodes = list(set(shadingGrps))

        assigned_sg = neon.get_shading_groups_in_hierarchy(grp_name)

        

        # tex_list = []
        tex_info_dict = tex_info_provider.get_info(grp_name)
        print('============== 0. check texture file node ========')
        # pprint.pprint(tex_info_dict)
        for key_tex_file_node_name in tex_info_dict:
            self.check_assetName_in_node(key_tex_file_node_name, asset_name)

        print('============== 1. check shading group ========')
        for node in all_nodes:
            if node == "":
                continue
            if 'initialShadingGroup' in node:
                continue
            if 'initialParticleSE' in node:
                continue
            elif 'textureEditorIsolateSelectSet' in node:
                continue
            if cmds.nodeType(node) in ['groupId']:
                continue
            self.check_assetName_in_node(node, asset_name)


        print('========== 2. check material node ============')
        for mat in cmds.ls(mat=True):
            if mat in ['lambert1', 'particleCloud1', 'initialParticleSE']:
                continue
            sg_bind = "{0}.outColor".format(mat)
            if  cmds.nodeType(mat) ==  "displacementShader":
                sg_bind = "{0}.displacement".format(mat)
            shaindg_group = None
            try:
                shaindg_group = cmds.listConnections(sg_bind, d = True, s = False).pop(0)
            except Exception as e:
                continue

            if not shaindg_group in assigned_sg:
                continue

            self.check_assetName_in_node(mat, asset_name)


        # for err_target in self.err_list:
        #     self.add_warnning(err_target, " is not started with " + asset_name, "error", err_target)
        #     self.warn_count += 1

        self.add_items(self.err_list)
        self.warn_count = len(self.err_list)

    def is_all_clear(self):
        return self.warn_count == 0

    def show_all_clear_items(self):
        msg = "{0} of items are clear".format(len(self.clear_items))
        # self.add_item(msg, "Clear", "clear")
        self.add_items([["", msg]])
