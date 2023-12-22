
from os import getcwd, path
from re import search
import sys
_path = "/usersetup/linux/scripts/maya_sc/yetiScripts/YTX_toolkit_v03/toggleAll"
_module_path = "/usersetup/linux/module"
if _path not in sys.path:
    sys.path.append(path.realpath(_path))
if _module_path not in sys.path:
    sys.path.append(path.realpath(_module_path))


from importlib import reload
import toggleAll_toolkit as toggleAll_toolkit
reload(toggleAll_toolkit)


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








class SelectChoiceContents(QWidget):
    def __init__(self, _parent=None) -> None:
        super(SelectChoiceContents, self).__init__(_parent)
        self._parent = _parent

        self.selected_type = None
        self.setupUi()

    def setupUi(self) -> None:

        self.check_type_title       = QLabel("Toggle TRS")
        self.check_type_title.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 15px;
                                               font-weight      : bold;
                                        }}
                                    ''')
        self.check_split_line_fm    = QFrame()
        self.check_split_line_fm.setFrameShape(QFrame.HLine)
        self.yes_rb               = QRadioButton("예")
        self.no_rb                = QRadioButton("아니오")

        self.btn_groups             = QButtonGroup()
        self.btn_groups.addButton(self.yes_rb)
        self.btn_groups.addButton(self.no_rb)
        self.btn_groups.buttonClicked.connect(self.set_choice)
        
        self.main_v_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        checkbox_margin = 40
        self.check_vl = QVBoxLayout()
        self.check_vl.addWidget(self.check_type_title)
        self.check_vl.addWidget(self.check_split_line_fm)
        self.check_vl.addWidget(self.yes_rb)
        self.check_vl.addWidget(self.no_rb)
        self.check_vl.addItem(self.main_v_spacer)
        self.check_vl.setContentsMargins(10,checkbox_margin,0,0)


        self.setLayout(self.check_vl)

    def set_choice(self, button) -> None:
        if button.text() == "아니오":
            self.selected_type = False
        elif button.text() == "예":
            self.selected_type = True

        

    def get_res(self) -> str:
        if self.selected_type == None:
            return None
        return self.selected_type








class ToggleDialog(QDialog):
    def __init__(self, _parent=None) -> None:
        super(ToggleDialog, self).__init__(_parent)

        self.selected_type = ""
        self.cur_contents_idx = 0


        

        self.info_hub      = [
                                {"TITLE"    : "Toggle TRS (translate, rotate)",
                                "MSG"       : "모든 yetiGRP의 노드들의 TRS를 연결하시겠습니까?",
                                "WIDGET"    : SelectChoiceContents()}
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
        self.setWindowTitle("ToggleAll")

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
            connect_all   = self.res_info[0]
            
            status_msg = ""
            if connect_all == True:
                status_msg = "모든 노드들 Connect !"
            elif connect_all == False:
                status_msg = "모든 노드들 Disconnect !"
            
            toggleAll_toolkit.run(connect_all)
            toggleAll_toolkit.show_msg_box(status_msg)    

            self.close()
            return
        self.set_current_contents(self.cur_contents_idx)



def run_tool() -> None:
    maya_view = _maya_main_window()
    ui = ToggleDialog(maya_view)
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
