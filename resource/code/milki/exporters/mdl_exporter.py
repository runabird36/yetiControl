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



import mdl_set_arnold_attr

import ui_progressbar
# reload(ui_progressbar)

_abc_cmd_template = '-frameRange 1 1 -attr notes -stripNamespaces -uvWrite -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {0} -file {1}'

class MdlExporter(Exporter):

    pub_paths = []

    def __init__(self, m_sg_tk, p_dialog):
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog


    def pre_execute(self, targets, options):

        maya_toolkit.set_display_setting("1")
        # self.pub_type_list = options['Export Order']
        # {'Export Order': [u'maya', u'alembic cache']}
        # {'Export Order': [u'maya', u'alembic cache'], 'pub with Alembic': [u'publish with alembic']}

        self.PUB_WITH_ABC = False
        if options.get('pub with Alembic') == []:
            self.PUB_WITH_ABC = False
        else:
            self.PUB_WITH_ABC = True


        self.PUB_WITH_MAT = False
        if options.get('pub with Material') == []:
            self.PUB_WITH_MAT = False
        else:
            self.PUB_WITH_MAT = True





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



        if self.PUB_WITH_ABC == True:
            self.abc_pub_path = self.get_pub_paths('abc')
            if pub_lastver != "None":
                self.abc_pub_path = re.sub(r"/v\d+/", "/"+pub_lastver+"/", self.abc_pub_path)
                self.abc_pub_path = re.sub(r"\_v\d+\.abc$", "_"+pub_lastver+".abc", self.abc_pub_path)
            
            all_path.append(self.abc_pub_path)


        # self.hichy_pub_path = self.get_pub_paths('hichy')
        # all_path.append(self.hichy_pub_path)
        self.add_pub_files(all_path)

        


        
        

        # Set mdl version to notes in top node of hierarchy
        cur_dev_version = LUCY.get_dev_vernum()
        if cmds.attributeQuery("notes", node=targets[0], exists=True) == False:
            print("warnning : there is no notes attribute")
            cmds.addAttr(targets[0], sn="nts", ln="notes", dt="string")

        ver_info = "MDL pub version     :   {0}\nMDL dev version     :   {1}".format(pub_lastver, cur_dev_version)
        cmds.setAttr('{0}.notes'.format(targets[0]), ver_info, typ="string")


    
    def filtered_not_main_shape(self, export_shape_list):
        real_export_tar_list = []
        re_ex_postifx = re.compile(r'Orig$|\d+Orig$|Orig\d+$')
        for _shape in export_shape_list:
            if re_ex_postifx.search(_shape):
                print(_shape)
                continue
            real_export_tar_list.append(_shape)

        return real_export_tar_list






    def execute(self):
        print('execute!')
        thumb = self.panel.get_thumb()

        self.check_pub_condition()
        cmds.select(self.target)



        '''
        the target which will be published need not to be assigned with arnold attribute information from lookdev pub
        '''

        

        # get all shading group and meshes pair
        if self.PUB_WITH_MAT == False:
            meshes_shd_gpr_pair_dict = {}
            all_shd_grp = neon.get_shading_groups_in_hierarchy(self.target)
            for shd_grp in all_shd_grp:
                if shd_grp == 'MayaNodeEditorSavedTabsInfo':
                    shd_grp = 'initialShadingGroup'
                meshes_with_shd_grp = cmds.listConnections (shd_grp, source=True, destination=False, shapes=True, t='mesh')
                # print meshes_with_shd_grp
                meshes_shd_gpr_pair_dict[shd_grp] = meshes_with_shd_grp




        # assign initial shader
        target = self.target[0]
        if self.PUB_WITH_MAT == False:
            all_shape = cmds.ls(target, dagObjects = True, long = True, shapes = True)
            cmds.sets(all_shape, e=True, forceElement='initialShadingGroup')



        pub_targets = []


        
        # check and make ma folder
        dir_path_ma=os.path.dirname(self.ma_pub_path)
        if not os.path.exists(dir_path_ma) :
            os.makedirs(dir_path_ma)


        # include export special target : Mash...
        sepcial_targets = cmds.ls(type='instancer')
        if sepcial_targets:
            cmds.select(sepcial_targets, add=True)


        # ma file publish
        cmds.file(self.ma_pub_path, type="mayaBinary",force = True, exportSelected=True,preserveReferences=True,shader=self.PUB_WITH_MAT, expressions=True)
        

        pub_targets.append(self.ma_pub_path)







        # # meshes file publish
        # all_shape = cmds.ls(target, dagObjects = True, long = True)


        # dir_path_hichy=os.path.dirname(self.hichy_pub_path)
        # if not os.path.exists(dir_path_hichy):
        #     os.makedirs(dir_path_hichy)



        # export_target_all_shape = []
        # target = self.target[0]
        # asset_name = LUCY.get_assetname()
        # export_target_all_shape = cmds.ls(target, dagObjects = True, long = True)
        
        # export_target_all_shape = self.filtered_not_main_shape(export_target_all_shape)

        
        # with open(self.hichy_pub_path, "wb") as p:
        #     pickle.dump(export_target_all_shape, p)








        if self.PUB_WITH_ABC == True:
            abc_pub_dir_path = os.path.dirname(self.abc_pub_path)
            if not os.path.exists(abc_pub_dir_path):
                os.makedirs(abc_pub_dir_path)

            abc_cmd = _abc_cmd_template.format(self.target[0], self.abc_pub_path)
            cmds.AbcExport ( j = abc_cmd )

            pub_targets.append(self.abc_pub_path)




            # pub_targets = [ma_pub_path]
            # self.pub_to_sg(pub_targets)
            # self.finish(ma_pub_path)






        # reset notes in assetname_GRP
        cmds.setAttr('{0}.notes'.format(self.target[0]), "", typ="string")


        # re-assign shaders
        if self.PUB_WITH_MAT == False:
            for shd_grp in meshes_shd_gpr_pair_dict:
                meshes_list=meshes_shd_gpr_pair_dict[shd_grp]
                shd_grp_type = cmds.objectType(shd_grp)
                if shd_grp_type in ['MASH_Distribute','polyPlanarProj','polyRetopo', 'polyNormalizeUV', 'polyBevel']:
                    continue
                if meshes_list == None:
                    continue
                else:
                    cmds.sets(meshes_list, e=True, forceElement=shd_grp)





        # maya_toolkit.set_display_setting("3")
        self.pub_to_sg(pub_targets)
        self.finish(self.ma_pub_path)
