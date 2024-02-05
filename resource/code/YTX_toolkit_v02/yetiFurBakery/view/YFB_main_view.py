# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AB_main_view.ui'
#
# Created: Sun Oct  4 15:46:01 2020
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!
import os
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from pprint import pprint
import re
from subprocess import Popen


from importlib import reload
import YFB_path_module
reload(YFB_path_module)
import YFB_maya_toolkit
reload(YFB_maya_toolkit)
from YFB_maya_toolkit import (
                                        convert2_maya_color,
                                        select_node,
                                        get_yeti_cache_path,
                                        init_cache_structure,
                                        set_visibility,
                                        does_furcache_exists
                                    )
from window_adaptor import _maya_main_window


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)





def get_zfillnum(num: int, padding: int):
    return str(num).zfill(padding)

class customQspinBox(QtGui.QSpinBox):
    def __init__(self, parent) -> None:
        super(customQspinBox, self).__init__(parent)

        self.style_component = {'background_color': '#3C3C3C',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}


        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimum(1)
        self.setMaximum(1000)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        

    def set_style(self, direction :str) -> None:
        if direction == "updown":
            self.setStyleSheet(
                            "QSpinBox{"+\
                            "border: 1px solid;"+\
                            "border-color: "+ self.style_component['background_color'] +";"+\
                            "border-radius: 3px;"+\
                            "}"+\
                            "QSpinBox::up-button{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center right;"+\
                                "image: url("+YFB_path_module._rigth_arrow+");"+\
                                "background:" +self.style_component['background_color']+";"+\
                                "left: 1px;"+\
                                "height: 24px;"+\
                                "width: 24px;"+\
                            "}"+\
                            "QSpinBox::up-button:pressed{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center right;"+\
                                "image: url("+YFB_path_module._rigth_arrow_pressed+");"+\
                                "background:" +self.style_component['font_color']+";"+\
                                "left: 1px;"+\
                                "height: 24px;"+\
                                "width: 24px;"+\
                                "border: 1px solid;"+\
                                "border-radius: 5px;"+\
                            "}"+\
                            "QSpinBox::down-button{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center left;"+\
                                "image: url("+YFB_path_module._left_arrow+");"+\
                                "background:" +self.style_component['background_color']+";"+\
                                "right: 1px;"+\
                                "height: 24px;"+\
                                "width: 24px;"+\
                            "}"+\
                            "QSpinBox::down-button:pressed{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center left;"+\
                                "image: url("+YFB_path_module._left_arrow_pressed+");"+\
                                "background:" +self.style_component['font_color']+";"+\
                                "right: 1px;"+\
                                "height: 24px;"+\
                                "width: 24px;"+\
                                "border: 1px solid;"+\
                                "border-radius: 5px;"+\
                            "}")
        elif direction == "leftright":
            self.setStyleSheet(
                            "QSpinBox{"+\
                            "border: 1px solid;"+\
                            "border-color: "+ self.style_component['background_color'] +";"+\
                            "border-radius: 3px;"+\
                            "}"+\
                            "QSpinBox::up-button{"+\
                                "image: url("+YFB_path_module._up_arrow+");"+\
                                "background:" +self.style_component['background_color']+";"+\
                                "left: 1px;"+\
                                "height: 12px;"+\
                                "width: 12px;"+\
                            "}"+\
                            "QSpinBox::up-button:pressed{"+\
                                "image: url("+YFB_path_module._up_arrow_pressed+");"+\
                                "background:" +self.style_component['font_color']+";"+\
                                "left: 1px;"+\
                                "height: 12px;"+\
                                "width: 12px;"+\
                                "border: 1px solid;"+\
                                "border-radius: 5px;"+\
                            "}"+\
                            "QSpinBox::down-button{"+\
                                "image: url("+YFB_path_module._down_arrow+");"+\
                                "background:" +self.style_component['background_color']+";"+\
                                "right: 1px;"+\
                                "height: 12px;"+\
                                "width: 12px;"+\
                            "}"+\
                            "QSpinBox::down-button:pressed{"+\
                                "image: url("+YFB_path_module._down_arrow_pressed+");"+\
                                "background:" +self.style_component['font_color']+";"+\
                                "right: 1px;"+\
                                "height: 12px;"+\
                                "width: 12px;"+\
                                "border: 1px solid;"+\
                                "border-radius: 5px;"+\
                            "}")
        elif direction == "updown_13":
            self.setStyleSheet(
                            "QSpinBox{"+\
                            "border: 1px solid;"+\
                            "border-color: "+ self.style_component['background_color'] +";"+\
                            "border-radius: 3px;"+\
                            "}"+\
                            "QSpinBox::up-button{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center right;"+\
                                "image: url("+YFB_path_module._rigth_arrow+");"+\
                                "background:" +self.style_component['background_color']+";"+\
                                "left: 1px;"+\
                                "height: 20px;"+\
                                "width: 20px;"+\
                            "}"+\
                            "QSpinBox::up-button:pressed{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center right;"+\
                                "image: url("+YFB_path_module._rigth_arrow_pressed+");"+\
                                "background:" +self.style_component['font_color']+";"+\
                                "left: 1px;"+\
                                "height: 20px;"+\
                                "width: 20px;"+\
                                "border: 1px solid;"+\
                                "border-radius: 5px;"+\
                            "}"+\
                            "QSpinBox::down-button{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center left;"+\
                                "image: url("+YFB_path_module._left_arrow+");"+\
                                "background:" +self.style_component['background_color']+";"+\
                                "right: 1px;"+\
                                "height: 20px;"+\
                                "width: 20px;"+\
                            "}"+\
                            "QSpinBox::down-button:pressed{"+\
                                "subcontrol-origin: margin;"+\
                                "subcontrol-position: center left;"+\
                                "image: url("+YFB_path_module._left_arrow_pressed+");"+\
                                "background:" +self.style_component['font_color']+";"+\
                                "right: 1px;"+\
                                "height: 20px;"+\
                                "width: 20px;"+\
                                "border: 1px solid;"+\
                                "border-radius: 5px;"+\
                            "}")

    def value(self) -> str:
        return "v"+get_zfillnum(super().value(), 3)

    def setValue(self, val: str) -> None:
        val = val.replace('v', '')
        return super().setValue(int(val))

    def textFromValue(self, v: int) -> str:
        return "v"+get_zfillnum(v, 3)

class YFBSelVersionDialog(QtGui.QDialog):
    def __init__(self, _parent=None):
        super(YFBSelVersionDialog, self).__init__(None)
        self._parent = _parent


        self.style_component = {'background_color': '#3C3C3C',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}

        self.setupUi_1(self)


    def setupUi_1(self, Dialog):
        

        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(344, 121)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setStyleSheet("QDialog{"+\
                                                "background:" +self.style_component['background_color']+";"+\
                                                "border: 2px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 5px;"+\
                                                "color: "+ self.style_component['font_color'] +";"+\
                                                "font: 12px;"+\
                                                "}")
        

    def setupUi_2(self, Dialog):
        

        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.SYC_main_vl = QtGui.QVBoxLayout()
        self.SYC_main_vl.setObjectName(_fromUtf8("SYC_main_vl"))

        self.SYC_contents_lb = QtGui.QLabel(Dialog)
        self.SYC_contents_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.SYC_contents_lb.setObjectName(_fromUtf8("SYC_contents_lb"))
        self.SYC_contents_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background:" +self.style_component['background_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.SYC_main_vl.addWidget(self.SYC_contents_lb)

        self.SYC_count_hl = QtGui.QHBoxLayout()
        self.SYC_count_hl.setObjectName(_fromUtf8("SYC_count_hl"))

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.SYC_count_hl.addItem(spacerItem)

        self.SYC_count_sb = customQspinBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SYC_count_sb.sizePolicy().hasHeightForWidth())
        self.SYC_count_sb.setFixedHeight(26)
        self.SYC_count_sb.setSizePolicy(sizePolicy)
        self.SYC_count_sb.setObjectName(_fromUtf8("SYC_count_sb"))
        self.SYC_count_sb.setAlignment(QtCore.Qt.AlignCenter)
        self.SYC_count_sb.setMinimum(1)
        self.SYC_count_sb.set_style('updown')
        self.SYC_count_hl.addWidget(self.SYC_count_sb)


        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.SYC_count_hl.addItem(spacerItem1)


        self.SYC_count_hl.setStretch(0, 1)
        self.SYC_count_hl.setStretch(1, 1)
        self.SYC_count_hl.setStretch(2, 1)
        self.SYC_main_vl.addLayout(self.SYC_count_hl)

        # spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # self.SYC_main_vl.addItem(spacerItem2)

        self.SYC_btn_hl = QtGui.QHBoxLayout()
        self.SYC_btn_hl.setObjectName(_fromUtf8("SYC_btn_hl"))

        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.SYC_btn_hl.addItem(spacerItem3)

        self.SYC_ok_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SYC_ok_btn.sizePolicy().hasHeightForWidth())
        self.SYC_ok_btn.setSizePolicy(sizePolicy)
        self.SYC_ok_btn.setObjectName(_fromUtf8("SYC_ok_btn"))
        self.SYC_ok_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.SYC_btn_hl.addWidget(self.SYC_ok_btn)

        self.SYC_cancel_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SYC_cancel_btn.sizePolicy().hasHeightForWidth())
        self.SYC_cancel_btn.setSizePolicy(sizePolicy)
        self.SYC_cancel_btn.setObjectName(_fromUtf8("SYC_cancel_btn"))
        self.SYC_cancel_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.SYC_btn_hl.addWidget(self.SYC_cancel_btn)

        self.SYC_btn_hl.setStretch(0, 3)
        self.SYC_btn_hl.setStretch(1, 1)
        self.SYC_btn_hl.setStretch(2, 1)
        self.SYC_main_vl.addLayout(self.SYC_btn_hl)
        self.SYC_main_vl.setStretch(0, 1)
        self.SYC_main_vl.setStretch(1, 2)
        # self.SYC_main_vl.setStretch(2, 1)
        self.SYC_main_vl.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.SYC_main_vl)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.set_link()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.SYC_contents_lb.setText( u"Cache 버전을 선택해주십시오")
        self.SYC_ok_btn.setText(u"확인")
        self.SYC_cancel_btn.setText( u"취소")


    def set_link(self):
        self.SYC_ok_btn.clicked.connect(self.set_add_count)
        self.SYC_cancel_btn.clicked.connect(self.cancel_and_close)




    def set_add_count(self):
        self.accept()



    def cancel_and_close(self):
        self.reject()




    def showEvent(self,_event):

        self.effect = QtGui.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)

        _opac_anim = QtCore.QPropertyAnimation(self.effect, b"opacity")
        _opac_anim.setDuration(200)
        _opac_anim.setStartValue(0)
        _opac_anim.setEndValue(1)
        # _opac_anim.setEasingCurve(QtCore.QEasingCurve.InBack)
        _opac_anim.setEasingCurve(QtCore.QEasingCurve.InOutCirc)



        # _mouse_pos = QtGuiOrig.QCursor.pos()
        _parent_rect = self._parent.geometry().getRect()
        _parent_x = _parent_rect[0] + _parent_rect[2]/3
        _parent_y = _parent_rect[1] + _parent_rect[3]/3
        origin_size = self.size()
        origin_rect = QtCore.QRect(_parent_x, _parent_y,
                                    origin_size.width(), origin_size.height())
        start_rect = QtCore.QRect(_parent_x, _parent_y, 0, 0)
        self.setGeometry(start_rect)


        _anim = QtCore.QPropertyAnimation(self, b'geometry', self)
        _anim.setStartValue(start_rect)
        _anim.setEndValue(origin_rect)
        _anim.setDuration(200)
        _anim.setEasingCurve(QtCore.QEasingCurve.InOutCirc)




        self.parell_open_anim = QtCore.QParallelAnimationGroup()
        self.parell_open_anim.addAnimation(_opac_anim)
        self.parell_open_anim.addAnimation(_anim)
        self.parell_open_anim.start()

        # time.sleep(1)
        self.setupUi_2(self)





    def get_res(self):
        return self.SYC_count_sb.value()

class QLineEditWithPopup(QtGui.QLineEdit):
    def __init__(self, parent) -> None:
        super(QLineEditWithPopup, self).__init__(parent)

    def contextMenuEvent(self, arg__1: QtGuiOrig.QContextMenuEvent) -> None:
        return super().contextMenuEvent(arg__1)

    def mousePressEvent(self, arg__1: QtGuiOrig.QMouseEvent) -> None:
        open_cmd    = YFB_path_module.get_open_dir_cmd()
        open_target = self.get_path()
        try:
            print("{0} {1}".format(open_cmd, open_target))
            Popen([open_cmd, open_target])
        except Exception as e:
            print(str(e))
        return super().mousePressEvent(arg__1)

    def get_path(self) -> str:
        if YFB_path_module.is_windows() == True:
            return self.text().replace("<version_num>", "").replace('/', '\\')
        else:
            return self.text().replace("<version_num>", "")

class Item_Ui_Form(QtGui.QWidget):
    
    def __init__(self, _parent=None):
        super(Item_Ui_Form, self).__init__(_parent)
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_disable_color': '#797979',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}

        self.setupUi(self)

        self.Y_NODE = ''
        self.origin_grp = ""
        self.cache_grp = ""

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(437, 75)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sub_main_hl = QtGui.QHBoxLayout()
        self.sub_main_hl.setObjectName(_fromUtf8("sub_main_hl"))

        self.img_lb = QtGui.QLabel(Form)
        self.img_lb.setText(_fromUtf8(""))
        self.img_lb.setObjectName(_fromUtf8("img_lb"))
        self.sub_main_hl.addWidget(self.img_lb)

        self.sub_context_vl = QtGui.QVBoxLayout()
        self.sub_context_vl.setObjectName(_fromUtf8("sub_main_hl"))

        self.context_lb = QtGui.QLabel(Form)

        self.context_lb.setText(_fromUtf8(""))
        self.context_lb.setObjectName(_fromUtf8("context_lb"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.context_lb.sizePolicy().hasHeightForWidth())
        self.context_lb.setSizePolicy(sizePolicy)
        self.context_lb.setStyleSheet(
                                    "QLabel{"+\
                                    "font: 13px;"+\
                                    "padding-top : 2px;"+\
                                    "}")
        self.sub_context_vl.addWidget(self.context_lb)

        self.context_ns_lb = QtGui.QLabel(Form)

        self.context_ns_lb.setText(_fromUtf8(""))
        self.context_ns_lb.setObjectName(_fromUtf8("context_ns_lb"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.context_ns_lb.sizePolicy().hasHeightForWidth())
        self.context_ns_lb.setSizePolicy(sizePolicy)
        self.context_ns_lb.setStyleSheet(
                                    "QLabel{"+\
                                    "font: 13px;"+\
                                    "padding-top : 2px;"+\
                                    "}")
        self.sub_context_vl.addWidget(self.context_ns_lb)
        self.sub_context_vl.setStretch(0,5)
        self.sub_context_vl.setStretch(1,1)

        self.sub_main_hl.addLayout(self.sub_context_vl)


        self.switch_btn = QtGui.QPushButton(Form)
        self.switch_btn.setFixedSize(50,30)
        self.switch_btn.setObjectName(_fromUtf8("switch_btn"))
        # self.set_btn_status(self.switch_btn, "disable")
        
        self.sub_main_hl.addWidget(self.switch_btn)


        self.select_btn = QtGui.QPushButton(Form)
        self.select_btn.setFixedSize(50,30)
        self.select_btn.setObjectName(_fromUtf8("select_btn"))
        self.select_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.sub_main_hl.addWidget(self.select_btn)


        self.cancel_btn = QtGui.QPushButton(Form)
        self.cancel_btn.setFixedSize(30,30)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.cancel_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.sub_main_hl.addWidget(self.cancel_btn)

        self.sub_main_hl.setStretch(0, 1)
        self.sub_main_hl.setStretch(1, 8)
        self.sub_main_hl.setStretch(2, 1)
        self.sub_main_hl.setStretch(3, 1)
        self.horizontalLayout_2.addLayout(self.sub_main_hl)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.switch_btn.setText("To cache")
        self.select_btn.setText("select")
        self.cancel_btn.setText(_translate("Form", "X", None))


    @property
    def origin_GRP(self) -> str:
        return self.origin_grp

    @origin_GRP.setter
    def origin_GRP(self, _origin_grp :str) -> None:
        self.origin_grp = _origin_grp

    @property
    def cache_GRP(self) -> str:
        return self.cache_grp

    @cache_GRP.setter
    def cache_GRP(self, _cache_grp :str) -> None:
        self.cache_grp = _cache_grp

    def get_current_swith_status(self) -> str:
        if self.switch_btn.text().lower() == "to cache":
            return "CURRENT_ORIGIN"
        elif self.switch_btn.text().lower() == "to origin":
            return "CURRENT_CACHE"

    def change_swith_btn_status(self, text :str) -> None:
        self.switch_btn.setText(text)

        if self.get_current_swith_status() == "CURRENT_CACHE":
            self.switch_btn.setStyleSheet(
                                            "QPushButton{"+\
                                            "font: 11px  ;"+\
                                            "border: 1px solid;"+\
                                            "border-radius: 10px;"+\
                                            "border-color: rgba(114, 255, 145, 0.9);"+\
                                            "background-color: rgba(114, 255, 145, 0.1);"+\
                                            "color:"+ self.style_component['font_color'] +";"+\
                                            "}"+\
                                            "QPushButton:pressed{"+\
                                            "color:"+ self.style_component['font_color_pressed'] +";"+\
                                            "border-color:" +self.style_component['background_color']+";"+\
                                            "background-color:" +self.style_component['font_color']+";"+\
                                            "}")
        else:
            self.switch_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
                
                                            


    def set_btn_status(self, tar_btn, status="enable"):
        if status == "enable":
            tar_btn.setEnabled(True)
            tar_btn.setStyleSheet(
                                    "QPushButton{"+\
                                    "font: 11px  ;"+\
                                    "border: 1px solid;"+\
                                    "border-radius: 10px;"+\
                                    "border-color:"+ self.style_component['border_color']+";"+\
                                    "background-color:"+self.style_component['button_color']+";"+\
                                    "color:"+ self.style_component['font_color'] +";"+\
                                    "}"+\
                                    "QPushButton:pressed{"+\
                                    "color:"+ self.style_component['font_color_pressed'] +";"+\
                                    "border-color:" +self.style_component['background_color']+";"+\
                                    "background-color:" +self.style_component['font_color']+";"+\
                                    "}")
        else:
            tar_btn.setEnabled(False)
            tar_btn.setStyleSheet(
                                    "QPushButton{"+\
                                    "font: 11px  ;"+\
                                    "border: 1px solid;"+\
                                    "border-radius: 10px;"+\
                                    "border-color:"+ self.style_component['border_color']+";"+\
                                    "background-color:"+self.style_component['button_color']+";"+\
                                    "color:"+ self.style_component['font_disable_color'] +";"+\
                                    "}")

    def set_info(self, _Y_INFO, _y_shortname, _ns_num):
        self.Y_NODE = _Y_INFO

        _icon_path = YFB_path_module.yeti_icon_path


        pix_map = QtGuiOrig.QPixmap(_icon_path)
        pix_map = pix_map.scaled(32,32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.img_lb.setPixmap(pix_map)
        self.context_lb.setText(_y_shortname)
        self.context_ns_lb.setText(_ns_num)

        if self.does_cache_exists(_Y_INFO) == True:
            self.set_btn_status(self.switch_btn, "enable")
        else:
            self.set_btn_status(self.switch_btn, "disable")

    def does_cache_exists(self, _Y_INFO) -> bool:
        cur_bake_dir = _Y_INFO.bake_dir.replace("<version_num>", "")
        check_tars = os.listdir(cur_bake_dir)
        if check_tars == []:
            return False

        for _check_tar in check_tars:
            if re.search(r"v\d+", _check_tar):
                return True
        
        return False

    def get_yeti_name(self):
        return str(self.context_lb.text())

    def get_yeti_info_model(self):
        return self.Y_NODE








class custom_listwidget(QtGui.QListWidget):

    def __init__(self, _parent):
        super(custom_listwidget, self).__init__(_parent)
        self.parent = _parent
        self._drop_file_list    = []
        self.real_tar_list      = []




    def reset_listwidget(self):
        self.clear()
        self._drop_file_list = []




    def add_item(self, _item):
        if _item.short_name in self._drop_file_list:
            return

        _custom_item = Item_Ui_Form()
        _yeti_shortname = _item.short_name
        _ns_num = _item.ns_num
        _custom_item.set_info(_item, _yeti_shortname, _ns_num)
        _custom_item.switch_btn.clicked.connect(self.switch_node)
        _custom_item.select_btn.clicked.connect(self.select_yeti)
        _custom_item.cancel_btn.clicked.connect(self.delete_custom_item)


        _listwidet_item = QtGui.QListWidgetItem(self)
        _listwidet_item.setSizeHint(_custom_item.sizeHint())
        _listwidet_item.setFlags(_listwidet_item.flags() )
        self.addItem(_listwidet_item)
        self.setItemWidget(_listwidet_item, _custom_item)

        self.set_yeti_info_list(_item)



    def set_yeti_info_list(self, _info):
        self._drop_file_list.extend([_info.short_name])
        self.real_tar_list.extend([_info])



    def get_yeti_info_list(self):
        return self.real_tar_list




    def get_item_from_mouse(self):
        _click_pos = self.mapFromGlobal(QtGuiOrig.QCursor.pos())
        item = self.itemAt(_click_pos)
        return item, self.itemWidget(item)



    def switch_node(self):
        item, pop_widget = self.get_item_from_mouse()

        if pop_widget.get_current_swith_status() == "CURRENT_ORIGIN":

            sel_ver_dialog = YFBSelVersionDialog(_maya_main_window())
            if sel_ver_dialog.exec_():
                sel_vernum = sel_ver_dialog.get_res()
                cur_yeti_info = pop_widget.get_yeti_info_model()
                

                cache_fullpath = get_yeti_cache_path(
                                                        cur_yeti_info.bake_dir,
                                                        cur_yeti_info.ns_num,
                                                        cur_yeti_info.short_name,
                                                        sel_vernum
                                                    )

                if does_furcache_exists(cache_fullpath) == False:
                    import maya.cmds as cmds 
                    _msg = "현재 아래 정보의 캐쉬가 아직 bake되지 않았습니다.\ncache를 먼저 bake해주십시오\n"+\
                            "Yeti Node Name : "+cur_yeti_info.short_name+""+\
                            "Bake version   : "+sel_vernum+""
                    cmds.confirmDialog(title='Warrning', message=_msg, b='확인', bgc=convert2_maya_color([242, 137, 131]))
                    return

                origin_yeti_node, cache_version_node = init_cache_structure(
                                                                                cur_yeti_info.short_name,
                                                                                cur_yeti_info.long_name,
                                                                                sel_vernum,
                                                                                cache_fullpath
                                                                            )

                pop_widget.origin_GRP = origin_yeti_node
                pop_widget.cache_GRP = cache_version_node


                set_visibility(origin_yeti_node, False)
                set_visibility(cache_version_node, True)

                pop_widget.change_swith_btn_status("To origin")


        elif pop_widget.get_current_swith_status() == "CURRENT_CACHE":

            set_visibility(pop_widget.origin_GRP, True)
            set_visibility(pop_widget.cache_GRP, False)

            pop_widget.change_swith_btn_status("To cache")



    def select_yeti(self):
        item, pop_widget = self.get_item_from_mouse()


        cur_yeti_model = pop_widget.get_yeti_info_model()
        yeti_l_name = cur_yeti_model.long_name
        select_node(yeti_l_name)
        


    def delete_custom_item(self):
        item, pop_widget = self.get_item_from_mouse()
        idx  = self.indexFromItem(item).row()
        self.takeItem(idx)

        _removed_filename = pop_widget.get_yeti_name()
        tar_idx = None
        for _idx, _name in enumerate(self._drop_file_list): 
            
            if _name == _removed_filename:
                tar_idx = _idx
                break
        self.real_tar_list.pop(tar_idx)
        self._drop_file_list.remove(_removed_filename)
        





class Ui_MainWindow(object):

    def __init__(self):
        def convert_hex_to_rgb(hex_color, out_type="str"):
            temp = []
            hex_color = hex_color.lstrip('#')
            for i in (0, 2 ,4):
                cd_int = int(hex_color[i:i+2], 16)
                if out_type =="str":
                    cd_int = str(cd_int)
                temp.append(cd_int)
            if out_type == "str":
                return "rgb({0})".format(",".join(temp))
            elif out_type == "tuple":
                return tuple(temp)
        self.style_component = {'background_color'  : '#333333',
                                'border_color'      : '#595959',
                                'font_color'        : '#D9D9D9',
                                'font_contents_color': '#A9A9A9',
                                'font_color_pressed': '#595959',
                                'button_color'      : 'rgba(70,70,70,0.5)',
                                'tabpane_color'     : 'rgb(60,60,60)'}
        for _key, _value in self.style_component.items():
            if _value.startswith("#"):
                self.style_component[_key] = convert_hex_to_rgb(_value)

        # pprint(self.style_component)
        
                            

    def setupUi(self, MainWindow):
        def move_center(main_win):
            qr = main_win.frameGeometry()
            cp = QtGui.QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            main_win.move(qr.topLeft())

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(550, 750)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        MainWindow.setStyleSheet("QMainWindow{background-color : "+self.style_component["background_color"]+";}")
        move_center(MainWindow)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.YFB_main_vl = QtGui.QVBoxLayout()
        self.YFB_main_vl.setObjectName(_fromUtf8("AB_main_vl"))
        self.YFB_targets_vl = QtGui.QVBoxLayout()
        self.YFB_targets_vl.setObjectName(_fromUtf8("AB_targets_vl"))
        self.YFB_targets_sub_hl = QtGui.QHBoxLayout()
        self.YFB_targets_sub_hl.setObjectName(_fromUtf8("AB_targets_sub_hl"))

        self.YFB_targets_sub_title_lb = QtGui.QLabel(self.centralwidget)
        self.YFB_targets_sub_title_lb.setObjectName(_fromUtf8("AB_targets_sub_title_lb"))
        self.YFB_targets_sub_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['background_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        pix_map = QtGuiOrig.QPixmap(YFB_path_module.logo_path)
        pix_map = pix_map.scaled(250,250, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.YFB_targets_sub_title_lb.setPixmap(pix_map)
        self.YFB_targets_sub_hl.addWidget(self.YFB_targets_sub_title_lb)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.YFB_targets_sub_hl.addItem(spacerItem)

        self.YFB_targets_sub_all_btn = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YFB_targets_sub_all_btn.sizePolicy().hasHeightForWidth())
        self.YFB_targets_sub_all_btn.setSizePolicy(sizePolicy)
        self.YFB_targets_sub_all_btn.setObjectName(_fromUtf8("AB_targets_sub_plus_btn"))
        self.YFB_targets_sub_all_btn.setFixedSize(40,40)
        self.YFB_targets_sub_all_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.YFB_targets_sub_hl.addWidget(self.YFB_targets_sub_all_btn)

        self.YFB_targets_sub_plus_btn = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YFB_targets_sub_plus_btn.sizePolicy().hasHeightForWidth())
        self.YFB_targets_sub_plus_btn.setSizePolicy(sizePolicy)
        self.YFB_targets_sub_plus_btn.setObjectName(_fromUtf8("AB_targets_sub_plus_btn"))
        self.YFB_targets_sub_plus_btn.setFixedSize(40,40)
        self.YFB_targets_sub_plus_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.YFB_targets_sub_hl.addWidget(self.YFB_targets_sub_plus_btn)



        # self.YFB_targets_sub_remove_btn = QtGui.QPushButton(self.centralwidget)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.YFB_targets_sub_remove_btn.sizePolicy().hasHeightForWidth())
        # self.YFB_targets_sub_remove_btn.setSizePolicy(sizePolicy)
        # self.YFB_targets_sub_remove_btn.setObjectName(_fromUtf8("AB_targets_sub_remove_btn"))
        # self.YFB_targets_sub_hl.addWidget(self.YFB_targets_sub_remove_btn)

        self.YFB_targets_sub_hl.setStretch(0, 3)
        self.YFB_targets_sub_hl.setStretch(1, 4)
        self.YFB_targets_sub_hl.setStretch(2, 1)
        self.YFB_targets_sub_hl.setStretch(3, 1)
        self.YFB_targets_sub_hl.setStretch(4, 1)
        self.YFB_targets_vl.addLayout(self.YFB_targets_sub_hl)



        # self.YFB_targets_view_lw = QtGui.QListWidget(self.centralwidget)
        self.YFB_targets_view_lw = custom_listwidget(self.centralwidget)
        self.YFB_targets_view_lw.setObjectName(_fromUtf8("AB_targets_view_lw"))
        self.YFB_targets_view_lw.setFocusPolicy(QtCore.Qt.NoFocus)
        self.YFB_targets_view_lw.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        
        self.YFB_targets_view_lw.setStyleSheet(
                                        "QListWidget{"+\
                                        "border-style: solid;"+\
                                        "border-width : 0.5px;"+\
                                        "border-color: "+ self.style_component['border_color'] +";"+\
                                        "border-radius: 5px;"+\
                                        "color : "+ self.style_component['font_color'] +";"+\
                                        "background-color:"+self.style_component['background_color']+";"+\
                                        "font: 20px;"+\
                                        "}"+\
                                        "QListWidget::item{"+\
                                        "border-bottom: 1px solid #303030;"+\
                                        "color:"+ self.style_component['font_color'] +";"+\
                                        "height : 30px;"+\
                                        "}"+\
                                        "QListWidget::branch:hover{"+\
                                        "background-color: #363636;"+\
                                        "}"+\
                                        "QListWidget::branch:selected{"+\
                                        "background-color: #363636;"+\
                                        "}"+\
                                        "QListWidget::item:hover {"+\
                                        "color: "+ self.style_component['font_color'] +";"+\
                                        "background-color: #363636;"+\
                                        "}"+\
                                        "QListWidget::item:selected{"+\
                                        "background-color: #595959;"+\
                                        "color:"+ self.style_component['font_color'] +";"+\
                                        "}"+\
                                        "QScrollBar:vertical {"+\
                                        "width: 10px;"+\
                                        "margin: 20px 0 3px 0;"+\
                                        "border-radius: 5px;"+\
                                      "}"+\
                                      "QScrollBar::handle:vertical {"+\
                                        "background-color:" + self.style_component['font_color'] +";"+\
                                        "min-height: 5px;"+\
                                        "width : 10px;"
                                        "border-radius: 5px;"+\
                                      "}"+\
                                      "QScrollBar::add-line:vertical {"+\
                                        "background-color: none;"+\
                                        "height: 45px;"+\
                                        "subcontrol-position: bottom;"+\
                                        "subcontrol-origin: margin;"+\
                                      "}"+\
                                      "QScrollBar::sub-line:vertical {"+\
                                        "background: none;"+\
                                        "height: 45px;"+\
                                        "subcontrol-position: top;"+\
                                        "subcontrol-origin: margin;"+\
                                      "}"
                                      )
        self.YFB_targets_vl.addWidget(self.YFB_targets_view_lw)


        self.YFB_targets_vl.setStretch(0, 1)
        self.YFB_targets_vl.setStretch(1, 10)
        self.YFB_main_vl.addLayout(self.YFB_targets_vl)




        # self.line = QtGui.QFrame(self.centralwidget)
        # self.line.setFrameShape(QtGui.QFrame.HLine)
        # self.line.setFrameShadow(QtGui.QFrame.Sunken)
        # self.line.setObjectName(_fromUtf8("line"))
        # self.YFB_main_vl.addWidget(self.line)
        



        self.YFB_info_widget = QtGui.QWidget(self.centralwidget)
        self.YFB_info_widget.setObjectName("YFB_info_widget")
        self.YFB_info_widget.resize(593, 409)
        self.data_info_verticalLayout_2 = QtGui.QVBoxLayout(self.YFB_info_widget)
        self.data_info_verticalLayout_2.setObjectName("data_info_verticalLayout_2")
        self.YFB_info_main_vl = QtGui.QVBoxLayout()
        self.YFB_info_main_vl.setObjectName("YFB_info_main_vl")
        self.YFB_data_info_hl = QtGui.QHBoxLayout()
        self.YFB_data_info_hl.setObjectName("YFB_data_info_hl")

        # =====================================================================
        # abc info
        # =====================================================================
        self.YFB_abc_info_tw = QtGui.QTabWidget(self.YFB_info_widget)
        self.YFB_abc_info_tw.setObjectName("YFB_abc_info_tw")
        self.YFB_abc_info_tw.setFocusPolicy(QtCore.Qt.NoFocus)
        self.YFB_abc_info_tw.setStyleSheet(
                                            "QTabWidget::pane{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "padding-top : 2px;"+\
                                            "}"+\
                                            "QTabBar::tab {"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "padding: 10px;"+\
                                            "font: bold 13px;"+\
                                            "border-top-left-radius: 6px;"+\
                                            "border-top-right-radius: 6px;"+\
                                            "width: 170px;"+\
                                            "}"+\
                                            "QTabBar::tab:selected {"+\
                                            "background-color:" +self.style_component['button_color']+";"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 15px;"+\
                                            "border-top-left-radius: 6px;"+\
                                            "border-top-right-radius: 6px;"+\
                                            "width: 170px;"+\
                                            "}"
                                            )
        self.YFB_abc_info_root = QtGui.QWidget()
        self.YFB_abc_info_root.setObjectName("YFB_abc_info_root")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.YFB_abc_info_root)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.YFB_abc_info_root_vl = QtGui.QVBoxLayout()
        self.YFB_abc_info_root_vl.setObjectName("YFB_abc_info_root_vl")
        self.YFB_abc_info_ns_hl = QtGui.QHBoxLayout()
        self.YFB_abc_info_ns_hl.setObjectName("YFB_abc_info_ns_hl")
        self.YFB_abc_info_ns_title_lb = QtGui.QLabel(self.YFB_abc_info_root)
        self.YFB_abc_info_ns_title_lb.setObjectName("YFB_abc_info_ns_title_lb")
        self.YFB_abc_info_ns_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_abc_info_ns_hl.addWidget(self.YFB_abc_info_ns_title_lb)
        self.YFB_abc_info_ns_contents_le = QtGui.QLineEdit(self.YFB_abc_info_root)
        self.YFB_abc_info_ns_contents_le.setReadOnly(True)
        self.YFB_abc_info_ns_contents_le.setObjectName("YFB_abc_info_ns_contents_le")
        self.YFB_abc_info_ns_contents_le.setFixedWidth(100)
        self.YFB_abc_info_ns_contents_le.setStyleSheet("QLineEdit{"+\
                                                "background-color:" +self.style_component['background_color']+";"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 5px;"+\
                                                "color: "+ self.style_component['font_color'] +";"+\
                                                "font: 12px;"+\
                                                "padding-top : 2px;"+\
                                                "}"
                                                )
        self.YFB_abc_info_ns_hl.addWidget(self.YFB_abc_info_ns_contents_le)
        self.YFB_abc_info_ns_hl.setStretch(0, 2)
        self.YFB_abc_info_ns_hl.setStretch(1, 3)
        self.YFB_abc_info_root_vl.addLayout(self.YFB_abc_info_ns_hl)
        self.YFB_abc_info_bmesh_hl = QtGui.QHBoxLayout()
        self.YFB_abc_info_bmesh_hl.setObjectName("YFB_abc_info_bmesh_hl")
        self.YFB_abc_info_bmesh_title_lb = QtGui.QLabel(self.YFB_abc_info_root)
        self.YFB_abc_info_bmesh_title_lb.setObjectName("YFB_abc_info_bmesh_title_lb")
        self.YFB_abc_info_bmesh_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_abc_info_bmesh_hl.addWidget(self.YFB_abc_info_bmesh_title_lb)
        self.YFB_abc_info_bmesh_contents_le = QtGui.QLineEdit(self.YFB_abc_info_root)
        self.YFB_abc_info_bmesh_contents_le.setReadOnly(True)
        self.YFB_abc_info_bmesh_contents_le.setObjectName("YFB_abc_info_bmesh_contents_le")
        self.YFB_abc_info_bmesh_contents_le.setFixedWidth(100)
        self.YFB_abc_info_bmesh_contents_le.setStyleSheet("QLineEdit{"+\
                                                "background-color:" +self.style_component['background_color']+";"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 5px;"+\
                                                "color: "+ self.style_component['font_color'] +";"+\
                                                "font: 12px;"+\
                                                "padding-top : 2px;"+\
                                                "}"
                                                )
        self.YFB_abc_info_bmesh_hl.addWidget(self.YFB_abc_info_bmesh_contents_le)
        self.YFB_abc_info_bmesh_hl.setStretch(0, 2)
        self.YFB_abc_info_bmesh_hl.setStretch(1, 3)
        self.YFB_abc_info_root_vl.addLayout(self.YFB_abc_info_bmesh_hl)
        self.verticalLayout_4.addLayout(self.YFB_abc_info_root_vl)
        self.YFB_abc_info_tw.addTab(self.YFB_abc_info_root, "")
        self.YFB_data_info_hl.addWidget(self.YFB_abc_info_tw)

        # =====================================================================
        # yeti info
        # =====================================================================
        self.YFB_yeti_info_tw = QtGui.QTabWidget(self.YFB_info_widget)
        self.YFB_yeti_info_tw.setObjectName("YFB_yeti_info_tw")
        self.YFB_yeti_info_tw.setStyleSheet(
                                            "QTabWidget::pane{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "padding-top : 2px;"+\
                                            "}"+\
                                            "QTabBar::tab {"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "padding: 10px;"+\
                                            "font: bold 13px;"+\
                                            "border-top-left-radius: 6px;"+\
                                            "border-top-right-radius: 6px;"+\
                                            "width: 100px;"+\
                                            "}"+\
                                            "QTabBar::tab:selected {"+\
                                            "background-color:" +self.style_component['button_color']+";"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 15px;"+\
                                            "border-top-left-radius: 6px;"+\
                                            "border-top-right-radius: 6px;"+\
                                            "width: 100px;"+\
                                            "}"
                                            )
        self.YFB_yeti_info_root = QtGui.QWidget()
        self.YFB_yeti_info_root.setObjectName("YFB_yeti_info_root")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.YFB_yeti_info_root)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.YFB_yeti_info_vl = QtGui.QVBoxLayout()
        self.YFB_yeti_info_vl.setObjectName("YFB_yeti_info_vl")
        self.YFB_yeti_info_grms_title_lb = QtGui.QLabel(self.YFB_yeti_info_root)
        self.YFB_yeti_info_grms_title_lb.setObjectName("YFB_yeti_info_grms_title_lb")
        self.YFB_yeti_info_grms_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_yeti_info_vl.addWidget(self.YFB_yeti_info_grms_title_lb)
        self.YFB_yeti_info_grms_contents_lv = QtGui.QListWidget(self.YFB_yeti_info_root)
        self.YFB_yeti_info_grms_contents_lv.setObjectName("YFB_yeti_info_grms_contents_lv")
        # self.YFB_yeti_info_grms_contents_lv.setFocusPolicy(QtCore.Qt.NoFocus)
        self.YFB_yeti_info_grms_contents_lv.setStyleSheet(
                                        "QListWidget{"+\
                                        "border-style: solid;"+\
                                        "border-width : 0.5px;"+\
                                        "border-color: "+ self.style_component['border_color'] +";"+\
                                        "border-radius: 5px;"+\
                                        "color : "+ self.style_component['font_color'] +";"+\
                                        "background-color:"+self.style_component['background_color']+";"+\
                                        "font: 13px;"+\
                                        "}"+\
                                        "QListWidget::item{"+\
                                        "border-bottom: 1px solid #303030;"+\
                                        "color:"+ self.style_component['font_color'] +";"+\
                                        "height : 17px;"+\
                                        "}"+\
                                        "QListWidget::branch:hover{"+\
                                        "background-color: #363636;"+\
                                        "}"+\
                                        "QListWidget::branch:selected{"+\
                                        "background-color: #363636;"+\
                                        "}"+\
                                        "QListWidget::item:hover {"+\
                                        "color: "+ self.style_component['font_color'] +";"+\
                                        "background-color: #363636;"+\
                                        "}"+\
                                        "QListWidget::item:selected{"+\
                                        "background-color: #595959;"+\
                                        "color:"+ self.style_component['font_color'] +";"+\
                                        "}"+\
                                        "QScrollBar:vertical {"+\
                                        "width: 10px;"+\
                                        "margin: 20px 0 3px 0;"+\
                                        "border-radius: 5px;"+\
                                      "}"+\
                                      "QScrollBar::handle:vertical {"+\
                                        "background-color:" + self.style_component['font_color'] +";"+\
                                        "min-height: 5px;"+\
                                        "width : 10px;"
                                        "border-radius: 5px;"+\
                                      "}"+\
                                      "QScrollBar::add-line:vertical {"+\
                                        "background-color: none;"+\
                                        "height: 45px;"+\
                                        "subcontrol-position: bottom;"+\
                                        "subcontrol-origin: margin;"+\
                                      "}"+\
                                      "QScrollBar::sub-line:vertical {"+\
                                        "background: none;"+\
                                        "height: 45px;"+\
                                        "subcontrol-position: top;"+\
                                        "subcontrol-origin: margin;"+\
                                      "}"
                                      )
        self.YFB_yeti_info_vl.addWidget(self.YFB_yeti_info_grms_contents_lv)
        self.verticalLayout_6.addLayout(self.YFB_yeti_info_vl)
        self.YFB_yeti_info_tw.addTab(self.YFB_yeti_info_root, "")
        self.YFB_data_info_hl.addWidget(self.YFB_yeti_info_tw)
        self.YFB_data_info_hl.setStretch(0,2)
        self.YFB_data_info_hl.setStretch(1,3)
        self.YFB_info_main_vl.addLayout(self.YFB_data_info_hl)

        # =====================================================================
        # bake info
        # =====================================================================
        self.YFB_bake_info_tw = QtGui.QTabWidget(self.YFB_info_widget)
        self.YFB_bake_info_tw.setObjectName("YFB_bake_info_tw")
        self.YFB_bake_info_tw.setStyleSheet(
                                            "QTabWidget::pane{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "padding-top : 2px;"+\
                                            "}"+\
                                            "QTabBar::tab {"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "padding: 10px;"+\
                                            "font: bold 13px;"+\
                                            "border-top-left-radius: 6px;"+\
                                            "border-top-right-radius: 6px;"+\
                                            "width: 100px;"+\
                                            "}"+\
                                            "QTabBar::tab:selected {"+\
                                            "background-color:" +self.style_component['button_color']+";"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 15px;"+\
                                            "border-top-left-radius: 6px;"+\
                                            "border-top-right-radius: 6px;"+\
                                            "width: 100px;"+\
                                            "}"
                                            )
        self.YFB_bake_info_root = QtGui.QWidget()
        self.YFB_bake_info_root.setObjectName("YFB_bake_info_root")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.YFB_bake_info_root)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.YFB_bake_info_root_vl = QtGui.QVBoxLayout()
        self.YFB_bake_info_root_vl.setObjectName("YFB_bake_info_root_vl")
        self.YFB_bake_info_dir_vl = QtGui.QVBoxLayout()
        self.YFB_bake_info_dir_vl.setObjectName("YFB_bake_info_dir_vl")
        self.YFB_bake_info_dir_title_lb = QtGui.QLabel(self.YFB_bake_info_root)
        self.YFB_bake_info_dir_title_lb.setObjectName("YFB_bake_info_dir_title_lb")
        self.YFB_bake_info_dir_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_bake_info_dir_vl.addWidget(self.YFB_bake_info_dir_title_lb)
        # self.YFB_bake_info_dir_contents_le = QtGui.QLineEdit(self.YFB_bake_info_root)
        self.YFB_bake_info_dir_contents_le = QLineEditWithPopup(self.YFB_bake_info_root)
        self.YFB_bake_info_dir_contents_le.setReadOnly(True)
        self.YFB_bake_info_dir_contents_le.setToolTip("클릭 : 경로열기")
        self.YFB_bake_info_dir_contents_le.setObjectName("YFB_bake_info_dir_contents_le")
        self.YFB_bake_info_dir_contents_le.setStyleSheet("QLineEdit{"+\
                                                "background-color:" +self.style_component['background_color']+";"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 5px;"+\
                                                "color: "+ self.style_component['font_contents_color'] +";"+\
                                                "font: 12px;"+\
                                                "padding-top : 2px;"+\
                                                "}"+\
                                                "QLineEdit:hover{"+\
                                                "color: "+ self.style_component['font_color'] +";"+\
                                                "}"
                                                )
        self.YFB_bake_info_dir_vl.addWidget(self.YFB_bake_info_dir_contents_le)
        self.YFB_bake_info_root_vl.addLayout(self.YFB_bake_info_dir_vl)
        # spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # self.YFB_bake_info_root_vl.addItem(spacerItem)



        # =====================================================================
        # frame info
        # =====================================================================

        self.YFB_frame_hl = QtGui.QHBoxLayout()
        self.YFB_frame_hl.setObjectName(_fromUtf8("AB_frame_hl"))


        self.YFB_vernum_vl = QtGui.QVBoxLayout()
        self.YFB_vernum_vl.setObjectName(_fromUtf8("YFB_vernum_vl"))

        self.YFB_vernum_title_lb = QtGui.QLabel(self.centralwidget)
        self.YFB_vernum_title_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.YFB_vernum_title_lb.setObjectName(_fromUtf8("YFB_vernum_title_lb"))
        self.YFB_vernum_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_vernum_vl.addWidget(self.YFB_vernum_title_lb)


        self.YFB_vernum_input_sb = customQspinBox(self.centralwidget)
        self.YFB_vernum_input_sb.setObjectName("YFB_vernum_input_sb")
        self.YFB_vernum_input_sb.set_style('updown_13')
        # self.YFB_vernum_input_sb.setStyleSheet("QSpinBox{"+\
        #                                         "background-color:" +self.style_component['background_color']+";"+\
        #                                         "border: 1px solid;"+\
        #                                         "border-color:"+ self.style_component['border_color']+";"+\
        #                                         "border-radius: 5px;"+\
        #                                         "color: "+ self.style_component['font_color'] +";"+\
        #                                         "font: 12px;"+\
        #                                         "padding-top : 2px;"+\
        #                                         "}"
        #                                         )
        self.YFB_vernum_vl.addWidget(self.YFB_vernum_input_sb)

        # self.YFB_vernum_input_le = QtGui.QLineEdit(self.centralwidget)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.YFB_vernum_input_le.sizePolicy().hasHeightForWidth())
        # self.YFB_vernum_input_le.setSizePolicy(sizePolicy)
        # self.YFB_vernum_input_le.setAlignment(QtCore.Qt.AlignCenter)
        # self.YFB_vernum_input_le.setObjectName(_fromUtf8("AB_frame_s_input_le"))
        # self.YFB_vernum_input_le.setStyleSheet("QLineEdit{"+\
        #                                         "background-color:" +self.style_component['background_color']+";"+\
        #                                         "border: 1px solid;"+\
        #                                         "border-color:"+ self.style_component['border_color']+";"+\
        #                                         "border-radius: 5px;"+\
        #                                         "color: "+ self.style_component['font_color'] +";"+\
        #                                         "font: 12px;"+\
        #                                         "padding-top : 2px;"+\
        #                                         "}"
        #                                         )
        # self.YFB_vernum_vl.addWidget(self.YFB_vernum_input_le)


        self.YFB_vernum_vl.setStretch(0, 3)
        self.YFB_vernum_vl.setStretch(1, 1)
        self.YFB_frame_hl.addLayout(self.YFB_vernum_vl)








        self.YFB_frame_s_vl = QtGui.QVBoxLayout()
        self.YFB_frame_s_vl.setObjectName(_fromUtf8("AB_frame_s_vl"))

        self.YFB_frame_s_title_lb = QtGui.QLabel(self.centralwidget)
        self.YFB_frame_s_title_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.YFB_frame_s_title_lb.setObjectName(_fromUtf8("AB_frame_s_title_lb"))
        self.YFB_frame_s_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_frame_s_vl.addWidget(self.YFB_frame_s_title_lb)




        self.YFB_frame_s_input_le = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YFB_frame_s_input_le.sizePolicy().hasHeightForWidth())
        self.YFB_frame_s_input_le.setSizePolicy(sizePolicy)
        self.YFB_frame_s_input_le.setAlignment(QtCore.Qt.AlignCenter)
        self.YFB_frame_s_input_le.setObjectName(_fromUtf8("AB_frame_s_input_le"))
        self.YFB_frame_s_input_le.setStyleSheet("QLineEdit{"+\
                                                "background-color:" +self.style_component['background_color']+";"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 5px;"+\
                                                "color: "+ self.style_component['font_color'] +";"+\
                                                "font: 12px;"+\
                                                "padding-top : 2px;"+\
                                                "}"
                                                )
        self.YFB_frame_s_vl.addWidget(self.YFB_frame_s_input_le)


        self.YFB_frame_s_vl.setStretch(0, 3)
        self.YFB_frame_s_vl.setStretch(1, 1)
        self.YFB_frame_hl.addLayout(self.YFB_frame_s_vl)
        self.YFB_frame_e_vl = QtGui.QVBoxLayout()
        self.YFB_frame_e_vl.setObjectName(_fromUtf8("AB_frame_e_vl"))


        self.YFB_frame_e_title_lb = QtGui.QLabel(self.centralwidget)
        self.YFB_frame_e_title_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.YFB_frame_e_title_lb.setObjectName(_fromUtf8("AB_frame_e_title_lb"))
        self.YFB_frame_e_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_frame_e_vl.addWidget(self.YFB_frame_e_title_lb)


        self.YFB_frame_e_input_le = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YFB_frame_e_input_le.sizePolicy().hasHeightForWidth())
        self.YFB_frame_e_input_le.setSizePolicy(sizePolicy)
        self.YFB_frame_e_input_le.setAlignment(QtCore.Qt.AlignCenter)
        self.YFB_frame_e_input_le.setObjectName(_fromUtf8("AB_frame_e_input_le"))
        self.YFB_frame_e_input_le.setStyleSheet("QLineEdit{"+\
                                                "background-color:" +self.style_component['background_color']+";"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 5px;"+\
                                                "color: "+ self.style_component['font_color'] +";"+\
                                                "font: 12px;"+\
                                                "padding-top : 2px;"+\
                                                "}"
                                                )
        self.YFB_frame_e_vl.addWidget(self.YFB_frame_e_input_le)


        self.YFB_frame_e_vl.setStretch(0, 3)
        self.YFB_frame_e_vl.setStretch(1, 1)
        self.YFB_frame_hl.addLayout(self.YFB_frame_e_vl)
        self.YFB_frame_step_vl = QtGui.QVBoxLayout()
        self.YFB_frame_step_vl.setObjectName(_fromUtf8("AB_frame_step_vl"))


        self.YFB_frame_step_title_lb = QtGui.QLabel(self.centralwidget)
        self.YFB_frame_step_title_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.YFB_frame_step_title_lb.setObjectName(_fromUtf8("AB_frame_step_title_lb"))
        self.YFB_frame_step_title_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background-color:" +self.style_component['tabpane_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YFB_frame_step_vl.addWidget(self.YFB_frame_step_title_lb)


        self.YFB_frame_step_input_le = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YFB_frame_step_input_le.sizePolicy().hasHeightForWidth())
        self.YFB_frame_step_input_le.setSizePolicy(sizePolicy)
        self.YFB_frame_step_input_le.setAlignment(QtCore.Qt.AlignCenter)
        self.YFB_frame_step_input_le.setObjectName(_fromUtf8("AB_frame_step_input_le"))
        self.YFB_frame_step_input_le.setStyleSheet("QLineEdit{"+\
                                                "background-color:" +self.style_component['background_color']+";"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 5px;"+\
                                                "color: "+ self.style_component['font_color'] +";"+\
                                                "font: 12px;"+\
                                                "padding-top : 2px;"+\
                                                "}"
                                                )
        self.YFB_frame_step_vl.addWidget(self.YFB_frame_step_input_le)


        self.YFB_frame_step_vl.setStretch(0, 3)
        self.YFB_frame_step_vl.setStretch(1, 1)
        self.YFB_frame_hl.addLayout(self.YFB_frame_step_vl)
        self.YFB_bake_info_root_vl.addLayout(self.YFB_frame_hl)



        self.YFB_bake_info_root_vl.setStretch(0, 2)
        self.YFB_bake_info_root_vl.setStretch(1, 3)
        self.verticalLayout_8.addLayout(self.YFB_bake_info_root_vl)
        self.YFB_bake_info_tw.addTab(self.YFB_bake_info_root, "")
        self.YFB_info_main_vl.addWidget(self.YFB_bake_info_tw)
        self.YFB_info_main_vl.setStretch(0, 1)
        self.YFB_info_main_vl.setStretch(1, 1)
        self.data_info_verticalLayout_2.addLayout(self.YFB_info_main_vl)

        self.YFB_abc_info_tw.setCurrentIndex(0)
        self.YFB_yeti_info_tw.setCurrentIndex(0)
        self.YFB_bake_info_tw.setCurrentIndex(0)


        self.YFB_main_vl.addWidget(self.YFB_info_widget)

        





        # self.YFB_main_vl.addLayout(self.YFB_frame_hl)
        # self.line_2 = QtGui.QFrame(self.centralwidget)
        # self.line_2.setFrameShape(QtGui.QFrame.HLine)
        # self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        # self.line_2.setObjectName(_fromUtf8("line_2"))
        # self.YFB_main_vl.addWidget(self.line_2)


        self.YFB_bake_btn = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YFB_bake_btn.sizePolicy().hasHeightForWidth())
        self.YFB_bake_btn.setSizePolicy(sizePolicy)
        self.YFB_bake_btn.setObjectName(_fromUtf8("AB_bake_btn"))
        self.YFB_bake_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px  ;"+\
                                                "border: 1px solid;"+\
                                                "border-radius: 10px;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.YFB_main_vl.addWidget(self.YFB_bake_btn)


        self.YFB_main_vl.setStretch(0, 15)
        self.YFB_main_vl.setStretch(1, 5)
        self.YFB_main_vl.setStretch(2, 3)
        # self.YFB_main_vl.setStretch(3, 1)
        # self.YFB_main_vl.setStretch(4, 3)
        self.verticalLayout_2.addLayout(self.YFB_main_vl)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Giantstep Yeti Bakery", None))
        # self.YFB_targets_sub_title_lb.setText(_translate("MainWindow", "Alembic Bakery", None))
        self.YFB_targets_sub_all_btn.setText(_translate("MainWindow", "All", None))
        self.YFB_targets_sub_plus_btn.setText(_translate("MainWindow", "추가", None))
        # self.YFB_targets_sub_remove_btn.setText(_translate("MainWindow", "제거", None))
        self.YFB_vernum_title_lb.setText("bake version")
        self.YFB_frame_s_title_lb.setText(_translate("MainWindow", "Start Frame", None))
        self.YFB_frame_e_title_lb.setText(_translate("MainWindow", "End Frame", None))
        self.YFB_frame_step_title_lb.setText(_translate("MainWindow", "Samples", None))
        self.YFB_bake_btn.setText(_translate("MainWindow", "Bake Fur Cache", None))


        self.YFB_abc_info_ns_title_lb.setText("Namespace")
        self.YFB_abc_info_bmesh_title_lb.setText("Asset name")
        self.YFB_abc_info_tw.setTabText(self.YFB_abc_info_tw.indexOf(self.YFB_abc_info_root), "Alembic Info(ANI)")
        self.YFB_yeti_info_grms_title_lb.setText("Groom nodes (선택 가능)")
        self.YFB_yeti_info_tw.setTabText(self.YFB_yeti_info_tw.indexOf(self.YFB_yeti_info_root), "Yeti Info")
        self.YFB_bake_info_dir_title_lb.setText("Bake directory path (클릭 : 경로 열기)")
        self.YFB_bake_info_tw.setTabText(self.YFB_bake_info_tw.indexOf(self.YFB_bake_info_root), "Bake Info")







    def add_targets_in_view(self, _targets_list):
        if isinstance(_targets_list, list):
            for tar in _targets_list:
                self.YFB_targets_view_lw.add_item(tar)
        else:
            tar = _targets_list
            self.YFB_targets_view_lw.add_item(tar)

    def add_targets_in_view_v02(self, tar_info):
        self.YFB_targets_view_lw.add_item(tar_info)



    def get_cur_tarlist(self):
        return self.YFB_targets_view_lw.get_yeti_info_list()


    def get_selected_yeti_info(self, selected_target :QtGui.QListWidgetItem):
        cur_custom_widget = self.YFB_targets_view_lw.itemWidget(selected_target)
        return cur_custom_widget.get_yeti_info_model()


    def set_assetname(self, assetname :str) -> None:
        self.YFB_abc_info_bmesh_contents_le.setText(assetname)

    def set_ns_info(self, ns_num :str) -> None:
        self.YFB_abc_info_ns_contents_le.setText(ns_num)

    def set_grooms_in_view(self, grm_list :list) -> None:
        self.YFB_yeti_info_grms_contents_lv.clear()
        for _idx, cur_grm in enumerate(grm_list):
            long_name = cur_grm
            short_name = cur_grm.split("|")[-1]
            short_name = re.sub(r"(Shape$|Shape\w+)", "", short_name)
            self.YFB_yeti_info_grms_contents_lv.addItem(short_name)
            self.YFB_yeti_info_grms_contents_lv.item(_idx).setData(QtCore.Qt.UserRole, long_name)




    def set_bake_dir(self, bake_dir :str):
        self.YFB_bake_info_dir_contents_le.setText(bake_dir)

    def get_bake_dir(self) -> str:
        return self.YFB_bake_info_dir_contents_le.text().replace("/<version_num>", "")


    def set_bake_vernum(self, bake_vernum :str) -> None:
        self.YFB_vernum_input_sb.setValue(bake_vernum)


    def get_bake_vernum(self) -> str:
        return self.YFB_vernum_input_sb.value()

    


    def set_to_int(func):
        def decorated(*args, **kwargs):
            if len(args) < 1:
                return
            input_num = args[1]
            input_num = int(input_num)
            input_num = str(input_num)
            func(args[0], input_num)

        return decorated


    @set_to_int
    def set_s_frame(self, s_frame):
        if not isinstance(s_frame, str):
            s_frame = str(s_frame)
        self.YFB_frame_s_input_le.setText(s_frame)

    
    def get_s_frame(self):
        return self.YFB_frame_s_input_le.text()

    @set_to_int
    def set_e_frame(self, e_frame):
        if not isinstance(e_frame, str):
            e_frame = str(e_frame)
        self.YFB_frame_e_input_le.setText(e_frame)


    def get_e_frame(self):
        return self.YFB_frame_e_input_le.text()


    @set_to_int
    def set_samples_info(self, samples_info):
        if not isinstance(samples_info, str):
            samples_info = str(samples_info)

        self.YFB_frame_step_input_le.setText(samples_info)

    def get_samples_info(self):
        return self.YFB_frame_step_input_le.text()



    def clear_info_view(self):
        self.YFB_abc_info_ns_contents_le.setText("")
        self.YFB_abc_info_bmesh_contents_le.setText("")
        self.YFB_yeti_info_grms_contents_lv.clear()



