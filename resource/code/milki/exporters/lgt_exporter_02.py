from importlib import reload
import maya.cmds as cmds
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui
import exporter
reload (exporter)
from exporter import Exporter
from toolkits import maya_toolkit
import os, pickle, pprint, time, socket, re


from maya_md import neon
from general_md_3x import LUCY


_abc_cmd_template = '-frameRange 1 1 -attr notes -stripNamespaces -uvWrite -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {0} -file {1}'

class LgtExporter(Exporter):

    pub_paths = []

    def __init__(self, m_sg_tk, p_dialog):
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog

        self.assetname = LUCY.get_assetname()


    

    def get_assembly_target(self, user_selections :list=[]) -> str:
        def get_aistandin_target(input_nodes :list) -> list:
            ai_standin_nodes    = cmds.ls(res, ni=True, dag=True, l=True, type="aiStandIn")
            targets = []
            for ai_standin_node in ai_standin_nodes:
                all_nodes = neon.get_all_connected_nodes(ai_standin_node)
                targets.extend(all_nodes)
            return targets

        check_tar = f"{self.assetname}_assemblyGRP"

        if check_tar not in user_selections:
            return None

        root                = cmds.ls(check_tar, l=True)
        res                 = cmds.ls(check_tar, ni=True, l=True, dag=True)
        ai_connected_nodes  = get_aistandin_target(res)

        

        if res:
            return root + ai_connected_nodes
        else:
            return None

    def get_light_target(self, user_selections :list=[]) -> str:
        check_tar   = f"{self.assetname}_lgtGRP"
        check_tar02 = f"{self.assetname}_lgt_GRP"
        
        if check_tar not in user_selections:
            return None

        res = cmds.ls(check_tar, ni=True, l=True, dag=True)
        if res:
            return res[0]
        else:
            return None
        
    def get_light02_target(self, user_selections :list=[]) -> str:
        check_tar = f"{self.assetname}_lgt_GRP"
        
        if check_tar not in user_selections:
            return None

        res = cmds.ls(check_tar, ni=True, l=True, dag=True)
        if res:
            return res[0]
        else:
            return None



    def pre_execute(self, targets, options):

        self._set_basic_info()


        self.target = targets
        cmds.select(self.target)

        all_path = []
        self.mb_pub_path = self.get_pub_paths('mb')

        self.assembly_pub_path = re.sub(r"\.mb$", "_assembly.mb",   self.mb_pub_path)
        self.light_pub_path    = re.sub(r"\.mb$", "_light.mb",      self.mb_pub_path)

        # all_path.append(self.mb_pub_path)
        if self.get_assembly_target(targets) != None:
            all_path.append(self.assembly_pub_path)
        if self.get_light_target(targets) != None:
            all_path.append(self.light_pub_path)
        if self.get_light02_target(targets) != None:
            all_path.append(self.light_pub_path)



        # Get pub version
        search_res = re.search("/v\d+/", self.mb_pub_path)
        if search_res:
            pub_lastver = search_res.group()
            pub_lastver = pub_lastver.replace("/", "")
        else:
            pub_lastver = "None"





        self.add_pub_files(all_path)




    



    def execute(self):
        print('execute!')
        thumb = self.panel.get_thumb()

        self.check_pub_condition()
        cmds.select(self.target)


        


        pub_targets = []


        
        # check and make mb folder
        dir_path_ma=os.path.dirname(self.mb_pub_path)
        if not os.path.exists(dir_path_ma) :
            os.makedirs(dir_path_ma)




        
        assembly_grp = self.get_assembly_target(self.target)
        light_grp    = self.get_light_target(self.target)
        light02_grp  = self.get_light02_target(self.target)


        # only light publish
        if light_grp != None:
            light_tars = cmds.listRelatives(light_grp, c=True)
            unparented_tars = cmds.parent(light_tars, world=True)
            
            cmds.select(cl=True)
            cmds.select(unparented_tars)
            cmds.file(self.light_pub_path, type="mayaBinary",force = True, exportSelected=True,preserveReferences=True,shader=False, expressions=True)
            cmds.parent(unparented_tars, light_grp)
        else:
            # light_tars = cmds.listRelatives(light02_grp, c=True)
            # unparented_tars = cmds.parent(light_tars, world=True)
            
            cmds.select(cl=True)
            cmds.select(light02_grp)
            cmds.file(self.light_pub_path, type="mayaBinary",force = True, exportSelected=True,preserveReferences=True,shader=False, expressions=True)
            # cmds.parent(unparented_tars, light02_grp)
        # light + assembly publish
        if assembly_grp != None:
            cmds.select(assembly_grp, add=True)
            cmds.file(self.assembly_pub_path, type="mayaBinary",force = True, exportSelected=True,preserveReferences=True,shader=True, expressions=True)
        

        pub_targets.append(self.light_pub_path)
        pub_targets.append(self.assembly_pub_path)










        # maya_toolkit.set_display_setting("3")
        self.pub_to_sg(pub_targets)
        self.finish(self.mb_pub_path)
