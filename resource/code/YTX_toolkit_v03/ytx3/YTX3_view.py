
from os import getcwd, path
from re import search
import sys
_path = "/home/taiyeong.song/Desktop/pipeTemp/updateYTX"

if _path not in sys.path:
    sys.path.append(path.realpath(_path))


from importlib import reload
# import YTX3_path_module
# reload(YTX3_path_module)


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

import YTX3_toolkit
reload(YTX3_toolkit)


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

        self.check_type_title       = QLabel("Hair Curve")
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
            # self.info_box = QMessageBox(self)
            # self.info_box.setWindowTitle("YTX3")
            # self.info_box.setText("Yeti 어싸인이 완료되지 않았습니다.")
            # self.info_box.setStandardButtons(QMessageBox.Ok)
            # self.info_box.exec_()
            # self._parent.close()
        elif button.text() == "예":
            self.selected_type = True

        

    def get_res(self) -> str:
        if self.selected_type == None:
            return None
        return self.selected_type





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




def increase_num(input_num :str) -> str:
    int_num = int(input_num)
    int_num += 1
    return str(int_num).zfill(3)

def get_zfillnum(num: int, padding: int):
    return str(num).zfill(padding)

class NSSpinbox(QSpinBox):
    def __init__(self, _parent=None) -> None:
        super(NSSpinbox, self).__init__(_parent)

        self.setFocusPolicy(Qt.NoFocus)
        self.setRange(1,999)

    def value(self) -> str:
        return get_zfillnum(super().value(), 3)

    def setValue(self, val: str) -> None:
        return super().setValue(int(val))

    def textFromValue(self, v: int) -> str:
        return get_zfillnum(v, 3)


class SetNSNumber(QWidget):
    def __init__(self, _parent=None) -> None:
        super(SetNSNumber, self).__init__(_parent)
        
        self.setupUi()
        self.init_value()

    def setupUi(self) -> None:

        self.title_lb       = QLabel("Namespace Number")
        self.title_lb.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 15px;
                                               font-weight      : bold;
                                        }}
                                    ''')
        self.line_fm    = QFrame()
        self.line_fm.setFrameShape(QFrame.HLine)


        self.ns_num_sb   = NSSpinbox()



        self.main_v_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.title_lb)
        self.main_vl.addWidget(self.line_fm)
        self.main_vl.addWidget(self.ns_num_sb)
        self.main_vl.addItem(self.main_v_spacer)
        self.main_vl.setContentsMargins(30,40,20,30)

        self.setLayout(self.main_vl)

        

    def init_value(self) -> None:
        exists_ns = []
        for _yeti in cmds.ls(sl=True, ni=True, dag=True, l=True, type='pgYetiMaya'):
            yeti_transform = cmds.listRelatives(_yeti, p=True, f=True)[0]
            search_res = search(r"\_\d+$", yeti_transform)
            if search_res:
                ns_num = search_res.group()
                ns_num = ns_num.replace("_", "")
                exists_ns.append(ns_num)

        exists_ns = list(set(exists_ns))
        exists_ns.sort()
        
        if exists_ns == []:
            next_ns = "001"
        else:
            last_ns = exists_ns.pop()
            next_ns = increase_num(last_ns)
            
        self.ns_num_sb.setValue(next_ns)



    def get_res(self) -> list:
        res = self.ns_num_sb.value()
        return res












class SelectChoiceForCVDelete(QWidget):
    def __init__(self, _parent=None) -> None:
        super(SelectChoiceForCVDelete, self).__init__(_parent)
        self._parent = _parent

        self.selected_type = None
        self.setupUi()

    def setupUi(self) -> None:

        self.check_type_title       = QLabel("Delete vertex CVs")
        self.check_type_title.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 15px;
                                               font-weight      : bold;
                                        }}
                                    ''')
        self.check_split_line_fm    = QFrame()
        self.check_split_line_fm.setFrameShape(QFrame.HLine)
        self.yes_rb               = QRadioButton("아니오")
        self.no_rb                = QRadioButton("예")

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
        
        if self.selected_type == True:
            YTX3_toolkit.delete_cv_val()

        return self.selected_type












class SelectYETI(QWidget):
    def __init__(self, _parent=None) -> None:
        super(SelectYETI, self).__init__(_parent)
        self.yeti_list = []

        self.setupUi()

    def setupUi(self) -> None:

        self.title_lb       = QLabel("Yeti nodes")
        self.title_lb.setStyleSheet(f'''
                                        QLabel{{
                                               font             : 15px;
                                               font-weight      : bold;
                                        }}
                                    ''')
        self.line_fm    = QFrame()
        self.line_fm.setFrameShape(QFrame.HLine)


        self.selected_yeti_lw   = QListWidget()

        self.select_btn         = QPushButton("선택")
        self.clear_btn          = QPushButton("Clear")

        self.select_btn.clicked.connect(self.set_selected_yeti)
        self.clear_btn.clicked.connect(self.selected_yeti_lw.clear)

        self.btn_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.btn_vl             = QVBoxLayout()
        self.btn_vl.addWidget(self.select_btn)
        self.btn_vl.addWidget(self.clear_btn)
        self.btn_vl.addItem(self.btn_spacer)

        self.sub_hl = QHBoxLayout()
        self.sub_hl.addWidget(self.selected_yeti_lw)
        self.sub_hl.addLayout(self.btn_vl)

        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.title_lb)
        self.main_vl.addWidget(self.line_fm)
        self.main_vl.addLayout(self.sub_hl)
        self.main_vl.setContentsMargins(30,40,20,30)

        self.setLayout(self.main_vl)

    def set_selected_yeti(self) -> None:
        self.selected_yeti_lw.clear()
        self.yeti_list = cmds.ls(sl=True, ni=True, dag=True, l=True, type='pgYetiMaya')
        print(self.yeti_list)
        for _node in self.yeti_list:
            s_name = _node.split("|")[-1]
            self.selected_yeti_lw.addItem(s_name)

        cmds.select(cl=True)
        cmds.select(self.yeti_list)

    def get_res(self) -> list:
        # res = []
        # for _idx in range(self.selected_yeti_lw.count()):
        #     yeti_name = self.selected_yeti_lw.item(_idx).text()
        #     res.append(yeti_name)
        if self.yeti_list == []:
            return None
        return self.yeti_list






class YTXDialog(QDialog):
    def __init__(self, _parent=None) -> None:
        super(YTXDialog, self).__init__(_parent)

        self.selected_type = ""
        self.cur_contents_idx = 0


        

        self.info_hub      = [
                                {"TITLE"    : "1. Asset Yeti 선택",
                                "MSG"       : "Asset-Hair 단계에서 펍된 yeti 노드들을 선택해주십시오.",
                                "WIDGET"    : SelectYETI()},
                                {"TITLE"    : "2. Delete vertex CVs",
                                "MSG"       : "Asset-Hair의 basemesh에 있는 CVs값들을 삭제하시겠습니까?",
                                "WIDGET"    : SelectChoiceForCVDelete()},
                                {"TITLE"    : "3. Namespace number 지정",
                                "MSG"       : "해당 yeti 그룹의 namespacer number를 지정해주십시오.",
                                "WIDGET"    : SetNSNumber()},
                                {"TITLE"    : "4. Shot Anim Cache 선택",
                                "MSG"       : "헤어를 어싸인할 애니메이션 캐쉬 어셋을 선택해주십시오(assetname_GRP)",
                                "WIDGET"    : SelectShotAsset()},
                                {"TITLE"    : "5. 헤어 커브 확인",
                                "MSG"       : "시뮬레이션 진행한 커브 데이터를 assetname_GRP 아래에 넣어져있습니까?, 원래 커브 있이 진행된 어셋입니까?",
                                "WIDGET"    : SelectChoiceContents(self)
                                }
                                
                                
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
        self.setWindowTitle("YTX3")

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
            # print(self.res_info)

            yeti_list   = self.res_info[0]
            does_cv_del = self.res_info[1]
            ns_num      = self.res_info[2]
            anim_cache  = self.res_info[3]
            curve_check = self.res_info[4]

            self.assign_engine = YTX3_toolkit.AssignControl(
                                                yeti_list,
                                                anim_cache,
                                                curve_check,
                                                ns_num
                                            )
            
            self.assign_engine.run()
            self.close()
            return
        self.set_current_contents(self.cur_contents_idx)


def run_tool() -> None:
    maya_view = _maya_main_window()
    ui = YTXDialog(maya_view)
    apply_stylesheet(ui, theme='dark_teal.xml')
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
