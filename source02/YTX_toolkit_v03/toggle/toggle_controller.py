
from os import getcwd, path
from re import search
import sys
_path = "/usersetup/linux/scripts/maya_sc/yetiScripts/YTX_toolkit_v03/toggle"
_module_path = "/usersetup/linux/module"
if _path not in sys.path:
    sys.path.append(path.realpath(_path))
if _module_path not in sys.path:
    sys.path.append(path.realpath(_module_path))


from importlib import reload
import toggle_toolkit
reload(toggle_toolkit)


from PySide2.QtWidgets import (
                                QApplication, QDialog, QHBoxLayout, QVBoxLayout,
                                QLabel, QPushButton, QCheckBox, QFrame, QSpacerItem,
                                QSizePolicy, QRadioButton, QButtonGroup, QMessageBox,
                                QWidget, QTabWidget, QListWidget, QLineEdit, QSpinBox
                            )
from PySide2.QtCore import Qt

from functools import partial
from qt_material import apply_stylesheet
from traceback import print_exc


import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets

import maya.cmds as cmds

# import YTX3_toolkit
# reload(YTX3_toolkit)


def _maya_main_window():
   '''
   Get the maya main window as a QMainWindow instance
   '''
   import maya.cmds as cmds
   import maya.OpenMayaUI as mui
   from shiboken2 import wrapInstance
   ptr = mui.MQtUtil.mainWindow()
   if ptr is not None:
        return wrapInstance(int(ptr),QWidget)








class SelectShotAsset(QWidget):
    def __init__(self, _parent=None) -> None:
        super(SelectShotAsset, self).__init__(_parent)
        self.selected_target_l = ""
        self.setupUi()

    def setupUi(self) -> None:

        self.title_lb       = QLabel("Shot Anim Cache")
        self.title_lb.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 15px;
                                               font-weight      : bold;
                                        }}
                                    ''')
        self.line_fm    = QFrame()
        self.line_fm.setFrameShape(QFrame.HLine)


        self.selected_target   = QLineEdit()

        self.select_btn         = QPushButton("선택")
        self.select_btn.clicked.connect(self.set_selected_target)


        self.sub_hl = QHBoxLayout()
        self.sub_hl.addWidget(self.selected_target)
        self.sub_hl.addWidget(self.select_btn)

        self.main_v_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.title_lb)
        self.main_vl.addWidget(self.line_fm)
        self.main_vl.addLayout(self.sub_hl)
        self.main_vl.addItem(self.main_v_spacer)
        self.main_vl.setContentsMargins(30,40,20,30)

        self.setLayout(self.main_vl)

    def set_selected_target(self) -> None:
        
        selected_targets = cmds.ls(sl=True, l=True)
        if selected_targets:
            self.selected_target.setText(selected_targets[0].split("|")[-1])
            self.selected_target_l = selected_targets[0]


    def get_res(self) -> list:
        if self.selected_target_l == "":
            return None

        res = self.selected_target_l
        return res





class SelectYetiGroup(QWidget):
    def __init__(self, _parent=None) -> None:
        super(SelectYetiGroup, self).__init__(_parent)
        self.selected_target_l = ""
        self.setupUi()

    def setupUi(self) -> None:

        self.title_lb       = QLabel("Yeti Transform Group")
        self.title_lb.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 15px;
                                               font-weight      : bold;
                                        }}
                                    ''')
        self.line_fm    = QFrame()
        self.line_fm.setFrameShape(QFrame.HLine)


        self.selected_target   = QLineEdit()

        self.select_btn         = QPushButton("선택")
        self.select_btn.clicked.connect(self.set_selected_target)


        self.sub_hl = QHBoxLayout()
        self.sub_hl.addWidget(self.selected_target)
        self.sub_hl.addWidget(self.select_btn)

        self.main_v_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.title_lb)
        self.main_vl.addWidget(self.line_fm)
        self.main_vl.addLayout(self.sub_hl)
        self.main_vl.addItem(self.main_v_spacer)
        self.main_vl.setContentsMargins(30,40,20,30)

        self.setLayout(self.main_vl)

    def set_selected_target(self) -> None:
        
        selected_targets = cmds.ls(sl=True, l=True)
        if selected_targets:
            self.selected_target.setText(selected_targets[0].split("|")[-1])
            self.selected_target_l = selected_targets[0]


    def get_res(self) -> list:
        if self.selected_target_l == "":
            return None

        res = self.selected_target_l
        return res








class YTXDialog(QDialog):
    def __init__(self, _parent=None) -> None:
        super(YTXDialog, self).__init__(_parent)

        self.selected_type = ""
        self.cur_contents_idx = 0


        

        self.info_hub      = [
                                {"TITLE"    : "1. yeti group 선택",
                                "MSG"       : "yeti 노드들을 묶어서 들고있는 transform group노드를 선택해주십시오.",
                                "WIDGET"    : SelectYetiGroup()},
                                {"TITLE"    : "2. Shot Anim Cache 선택",
                                "MSG"       : "0,0,0 에 있지 않는 Ani cache를 선택해주십시오.",
                                "WIDGET"    : SelectShotAsset()}
                            ]
        self.res_info       = []

        self.setupUi()



    def setupUi(self) -> None:
        
        self.title_lb = QLabel("")
        self.title_lb.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 20px;
                                               font-weight      : bold;
                                        }}
                                    ''')
        self.desc_lb = QLabel()
        self.desc_lb.setText("")
        self.desc_lb.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 13px;
                                        }}
                                    ''')

        
        # self.cur_contents_wg = ContentsWidget()

        self.contents_tw = QTabWidget()
        self.contents_tw.setStyleSheet("QTabBar::tab { border: 0; height: 1px;}")

        
        self.btn_h_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.select_btn   = QPushButton("다음")
        self.cancel_btn   = QPushButton("닫기")
        self.select_btn.clicked.connect(self.next_contents)
        self.cancel_btn.clicked.connect(self.close)

        self.btn_hl      = QHBoxLayout()
        self.btn_hl.addItem(self.btn_h_spacer)
        self.btn_hl.addWidget(self.select_btn)
        self.btn_hl.addWidget(self.cancel_btn)


        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.title_lb)
        self.main_vl.addWidget(self.desc_lb)
        self.main_vl.addWidget(self.contents_tw)
        
        self.main_vl.addLayout(self.btn_hl)
        


        self.setLayout(self.main_vl)
        main_margin = 15
        self.setContentsMargins(main_margin,main_margin,main_margin,main_margin)
        self.resize(500, 400)
        self.setWindowTitle("Toggle")

        self.register_contents()
        self.set_current_contents(self.cur_contents_idx)

    

    def register_contents(self) -> None:
        for contents in self.info_hub:
            # self.title_lb.setText(contents.get("TITLE"))
            # self.desc_lb.setText(contents.get("MSG"))
            self.contents_tw.addTab(contents.get("WIDGET"), "")



    def set_current_contents(self, idx :int) -> None:
        self.title_lb.setText(self.info_hub[idx].get("TITLE"))
        self.desc_lb.setText(self.info_hub[idx].get("MSG"))
        self.contents_tw.setCurrentIndex(idx)

    
    def set_current_res(self) -> bool:
        current_contents_widget = self.info_hub[self.cur_contents_idx].get("WIDGET")
        input_res = current_contents_widget.get_res()
        if input_res == None:
            return False
        self.res_info.append(input_res)
        return True
    def next_contents(self) -> None:
        res = self.set_current_res()
        if res == False:
            return

        self.cur_contents_idx += 1 
        if self.cur_contents_idx >= len(self.info_hub):
            # Finish Setting
            yeti_trf_node   = self.res_info[0]
            anim_cache      = self.res_info[1]
            
            self.execute(anim_cache, yeti_trf_node)

            self.close()
            return
        self.set_current_contents(self.cur_contents_idx)

    def execute(self, from_node :str, to_node :str) -> None:
        '''
            from_node   : anim_cache transform node : assetname_GRP
            to_node     : yeti transform group node : yeti
        '''
        is_connected = toggle_toolkit.is_connected(from_node, to_node)
        status_msg = ""
        if is_connected == False:
            toggle_toolkit.connect_trs(from_node, to_node)
            status_msg = "두개의 Translate, Rotate를 연결했습니다."
        elif is_connected == True:
            toggle_toolkit.disconnect_trs(from_node, to_node)
            status_msg = "두개의 Translate, Rotate의 연결을 끊었습니다.."

        toggle_toolkit.show_msg_box(status_msg)



def run_tool() -> None:
    maya_view = _maya_main_window()
    ui = YTXDialog(maya_view)
    apply_stylesheet(ui, theme='dark_purple.xml')
    ui.show()


if __name__ == "__main__":
    run_tool()


# if __name__ == "__main__":
#     import sys
    
#     app = QApplication(sys.argv)
#     apply_stylesheet(app, theme='dark_teal.xml')



#     ui = YTXDialog()
#     if ui.exec_():
#         pass
#     else:
#         pass


#     sys.exit(app.exec_())
