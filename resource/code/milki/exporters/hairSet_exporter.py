from importlib import reload
import maya.cmds as cmds
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui
import exporter
reload (exporter)
from exporter import Exporter
from toolkits import maya_toolkit
import os, re


from maya_md import neon
from general_md_3x import LUCY



import mdl_set_arnold_attr

import ui_progressbar
# reload(ui_progressbar)

_abc_cmd_template = '-frameRange 1 1 -attr notes -stripNamespaces -uvWrite -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {0} -file {1}'

class HairSetExporter(Exporter):

    pub_paths = []

    def __init__(self, m_sg_tk, p_dialog):
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog


    def pre_execute(self, targets, options):

        self._set_basic_info()


        self.target = targets
        cmds.select(self.target)

        all_path = []
        self.ma_pub_path = self.get_pub_paths('mb')
        all_path.append(self.ma_pub_path)



        # Get pub version
        search_res = re.search("/v\d+/", self.ma_pub_path)
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


        
        # check and make ma folder
        dir_path_ma=os.path.dirname(self.ma_pub_path)
        if not os.path.exists(dir_path_ma) :
            os.makedirs(dir_path_ma)


        # include export special target : Mash...
        sepcial_targets = cmds.ls(type='instancer')
        if sepcial_targets:
            cmds.select(sepcial_targets, add=True)

        # file -force -options "v=1;" -type "mayaBinary" -pr -ea "/home/taiyeong.song/Desktop/pipeTemp/aaa/v04.mb";
        # ma file publish
        cmds.file(self.ma_pub_path, type="mayaBinary",options="v=1;", force = True, ea=True,preserveReferences=True, expressions=True)
        

        pub_targets.append(self.ma_pub_path)





        # maya_toolkit.set_display_setting("3")
        self.pub_to_sg(pub_targets)
        self.finish(self.ma_pub_path)
