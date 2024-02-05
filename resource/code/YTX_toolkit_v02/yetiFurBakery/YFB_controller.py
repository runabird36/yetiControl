
from PySide2 import QtWidgets, QtCore
from importlib import reload
from pprint import pprint
import maya.cmds as cmds
import YFB_path_module
import window_adaptor, YFB_main_view
import YFB_maya_toolkit
reload(YFB_path_module)
reload(YFB_main_view)
reload(YFB_maya_toolkit)



class YetiFurController(QtWidgets.QMainWindow):
    def __init__(self):
        
        window_parent = window_adaptor._maya_main_window()
        QtWidgets.QMainWindow.__init__(self, window_parent)
        self._ui = YFB_main_view.Ui_MainWindow()




    def set_ui(self):
        self._ui.setupUi(self)
        pass


    def show_ui(self):
        self.show()
        pass


    def run(self):
        if YFB_maya_toolkit.get_filename() == None:
            self.error_controll('NOT_SAVE')
            return
        elif YFB_maya_toolkit.is_right_filename() == False:
            self.error_controll('NOT_FILENAME')
            return

        self.set_ui()
        self.show_ui()
        self.set_link()
        self.set_init_info()




    def set_link(self):
        self._ui.YFB_targets_sub_all_btn.clicked.connect(self.add_all_item)
        self._ui.YFB_targets_sub_plus_btn.clicked.connect(self.add_additional_item)
        self._ui.YFB_targets_view_lw.itemClicked.connect(self.set_selected_yeti_info)
        self._ui.YFB_yeti_info_grms_contents_lv.itemClicked.connect(self.select_cur_groom)
        self._ui.YFB_bake_btn.clicked.connect(self.start_baking)



    def add_all_item(self) -> None:
        for cur_yeti_info in YFB_maya_toolkit.get_all_yeti():
            sname = cur_yeti_info.short_name
            if YFB_maya_toolkit.is_yeti_node(sname) == False:
                self.error_controll(_flag="NOT_YETINODE")
                return
            
            self._ui.add_targets_in_view_v02(cur_yeti_info)


    def add_additional_item(self):
        # selected_tar_list =  cmds.ls(sl=True)
        selected_tar_list = YFB_maya_toolkit.get_selected_yeti_v02()
        for cur_yeti_info in selected_tar_list:
            sname = cur_yeti_info.short_name
            if YFB_maya_toolkit.is_yeti_node(sname) == False:
                self.error_controll(_flag="NOT_YETINODE")
                return
            
            self._ui.add_targets_in_view_v02(cur_yeti_info)
        



    def set_init_info(self) -> None:
        '''
            - bake dir
            - start frame
            - end frame
            - step
        '''
        bake_dirpath = YFB_maya_toolkit.get_bake_dir()
        self._ui.set_bake_dir(bake_dirpath)

        bake_vernum = YFB_maya_toolkit.get_bake_vernum()
        self._ui.set_bake_vernum(bake_vernum)


        start_frame = YFB_maya_toolkit.get_start_time()
        end_frame = YFB_maya_toolkit.get_end_time()
        self._ui.set_s_frame(start_frame)
        self._ui.set_e_frame(end_frame)
        self._ui.set_samples_info(YFB_path_module.default_samples)





    def set_selected_yeti_info(self, selected_item) -> None:
        
        cur_yeti_model = self._ui.get_selected_yeti_info(selected_item)
        
        # set namespace of alembic
        self._ui.set_ns_info(cur_yeti_model.ns_num)
        # set one basemesh
        self._ui.set_assetname(cur_yeti_model.ns_num.split("_")[0])
        # Set grooms list information
        grm_list = YFB_maya_toolkit.get_grooms_from_yeti(cur_yeti_model)
        self._ui.set_grooms_in_view(grm_list)




    def select_cur_groom(self, selected_item) -> None:

        grm_long_name = selected_item.data(QtCore.Qt.UserRole)
        YFB_maya_toolkit.select_node(grm_long_name)




    def start_baking(self) -> None:
        res = True
        try:
            bake_targets_list   = self._ui.get_cur_tarlist()
            info_hub = {}
            for yeti_info_model in bake_targets_list:
                print(yeti_info_model)
                y_ns_num    = yeti_info_model.ns_num
                y_sname     = yeti_info_model.short_name

                # if y_ns_num not in info_hub:
                #     info_hub[y_ns_num] = [y_sname]
                # else:
                #     info_hub[y_ns_num].append(y_sname)

                if y_ns_num not in info_hub:
                    info_hub[y_ns_num] = [yeti_info_model]
                else:
                    info_hub[y_ns_num].append(yeti_info_model)

            

            bake_dir            = self._ui.get_bake_dir()
            bake_vernum         = self._ui.get_bake_vernum()
            bake_s_frame        = self._ui.get_s_frame()
            bake_e_frame        = self._ui.get_e_frame()
            bake_samples        = self._ui.get_samples_info()

            
            for y_ns_num, yeti_node_list in info_hub.items():
                YFB_maya_toolkit.bake_yeti_fur(
                                                    bake_targets    =yeti_node_list,
                                                    bake_dir        =bake_dir,
                                                    bake_vernum     =bake_vernum,
                                                    s_frame         =bake_s_frame,
                                                    e_frame         =bake_e_frame,
                                                    input_samples   =bake_samples
                                                )
        except:
            res = False
        
        if res == True:
            cmds.confirmDialog(title='Clear', message="Baking 완료!", b='확인', bgc=YFB_maya_toolkit.convert2_maya_color([95, 217, 148]))
        else:
            self.error_controll("BAKING_FAIL")
        

    def error_controll(self,_flag=''):
        if _flag == '':
            return
        elif _flag == 'NOT_SAVE':
            _msg = '현재파일이 작업파일 이름 규약에 맞게 저장되지 않았습니다.\n\n'+\
                    'bake를 진행하기 전에 파일을 이름 규약에 맞게 저장해주십시오'
        elif _flag == 'NOT_FILENAME':
            cur_fname = YFB_maya_toolkit.get_filename()
            _msg = '현재 파일이름이 pipeline 규약에 맞지 않습니다 : {0}\n\n'.format(cur_fname)+\
                    '같이 제공된 규약문서와 아래의 예시를 참고해서 이름을 저장해주십시오\n\n'+\
                    '규약 : Shot(3글자)_Shotnum(4개의숫자)_taskname_version.mb\n\n'+\
                    'ex) CFX_0040_ani01_v03.mb'
        elif _flag == "NOT_YETINODE":
            _msg = '현재 yeti node 이름이 규약에 맞지 않습니다. 아래 규약에 맞게 rename해주십쇼\n\n'+\
                    '규약 : assetname_<NAME>_YETI_namesapceNumber\n\n'+\
                    'ex) kadan_body_eye_YETI_002Shape'
        elif _flag == "BAKING_FAIL":
            _msg = 'Baking 실패했습니다.\n\n'+\
                    'pipeline팀에 문의 부탁드리겠습니다.\n\n'
            
        cmds.confirmDialog(title='Error', message=_msg, b='확인', bgc=YFB_maya_toolkit.convert2_maya_color([242, 137, 131]))

    def mousePressEvent(self, event) -> None:
        focused_widget = QtWidgets.QApplication.focusWidget()
        if focused_widget == None:
            return super().mousePressEvent(event)
        if isinstance(focused_widget, QtWidgets.QListWidget):
            # focused_widget.clear()
            focused_widget.clearSelection()
        elif isinstance(focused_widget, QtWidgets.QMainWindow):
            self._ui.clear_info_view()
        elif isinstance(focused_widget, QtWidgets.QLineEdit):
            focused_widget.setText("")
        else:
            focused_widget.clearFocus()


        return super().mousePressEvent(event)