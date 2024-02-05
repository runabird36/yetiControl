

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from functools import partial


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




class YFBSelModeDialog(QtGui.QDialog):
    def __init__(self, _parent=None):
        super(YFBSelModeDialog, self).__init__(None)
        self._parent = _parent


        self.style_component = {'background_color': '#3C3C3C',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}

        self.cb_list = []
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
        self.YTX2_main_vl = QtGui.QVBoxLayout()
        self.YTX2_main_vl.setObjectName(_fromUtf8("YTX2_main_vl"))

        self.YTX2_contents_lb = QtGui.QLabel(Dialog)
        self.YTX2_contents_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.YTX2_contents_lb.setObjectName(_fromUtf8("YTX2_contents_lb"))
        self.YTX2_contents_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background:" +self.style_component['background_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font: bold 13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.YTX2_main_vl.addWidget(self.YTX2_contents_lb)

        # self.YTX2_count_hl = QtGui.QHBoxLayout()
        # self.YTX2_count_hl.setObjectName(_fromUtf8("YTX2_count_hl"))

        # spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # self.YTX2_count_hl.addItem(spacerItem)

        # self.YTX2_select_mode_wg = QtGui.QWidget(Dialog)
        # self.YTX2_select_mode_wg.setObjectName("YTX2_select_mode_wg")
        # self.YTX2_select_mode_wg.resize(400, 74)
        # self.horizontalLayout = QtGui.QHBoxLayout(self.YTX2_select_mode_wg)
        # self.horizontalLayout.setObjectName("horizontalLayout")
        # self.YTX2_grm_mode_cb = QtGui.QCheckBox(self.YTX2_select_mode_wg)
        # self.YTX2_grm_mode_cb.setObjectName("YTX2_grm_mode_cb")
        # self.YTX2_grm_mode_cb.setStyleSheet(
        #                                     "QCheckBox{"+\
        #                                     "background-color:" +self.style_component['background_color']+";"+\
        #                                     "color: "+ self.style_component['font_color'] +";"+\
        #                                     "font: bold 15px;"+\
        #                                     "padding-top : 2px;"+\
        #                                     "}"+\
        #                                     "QCheckBox::indicator {"+\
        #                                     "width: 11px;"+\
        #                                     "height: 11px;"+\
        #                                     "border-radius: 5px;"+\
        #                                     "}"+\
        #                                     "QCheckBox::indicator::unchecked{"+\
        #                                     "border: 1px solid; "+\
        #                                     "width: 11px;"+\
        #                                     "height: 11px;"+\
        #                                     "border-color:"+ self.style_component['border_color']+";"+\
        #                                     "border-radius: 5px;"+\
        #                                     "background:" +self.style_component['button_color']+";"+\
        #                                     "}"+\
        #                                     "QCheckBox::indicator::checked{"+\
        #                                     "border: 1px solid; "+\
        #                                     "width: 11px;"+\
        #                                     "height: 11px;"+\
        #                                     "border-color:"+ self.style_component['border_color']+";"+\
        #                                     "border-radius: 5px;"+\
        #                                     "background:" +self.style_component['font_color']+";"+\
        #                                     "}")
        # self.horizontalLayout.addWidget(self.YTX2_grm_mode_cb)
        # self.YTX2_fur_mode_cb = QtGui.QCheckBox(self.YTX2_select_mode_wg)
        # self.YTX2_fur_mode_cb.setObjectName("YTX2_fur_mode_cb")
        # self.YTX2_fur_mode_cb.setStyleSheet(
        #                                     "QCheckBox{"+\
        #                                     "background-color:" +self.style_component['background_color']+";"+\
        #                                     "color: "+ self.style_component['font_color'] +";"+\
        #                                     "font: bold 15px;"+\
        #                                     "padding-top : 2px;"+\
        #                                     "}"+\
        #                                     "QCheckBox::indicator {"+\
        #                                     "width: 11px;"+\
        #                                     "height: 11px;"+\
        #                                     "border-radius: 5px;"+\
        #                                     "}"+\
        #                                     "QCheckBox::indicator::unchecked{"+\
        #                                     "border: 1px solid; "+\
        #                                     "width: 11px;"+\
        #                                     "height: 11px;"+\
        #                                     "border-color:"+ self.style_component['border_color']+";"+\
        #                                     "border-radius: 5px;"+\
        #                                     "background:" +self.style_component['button_color']+";"+\
        #                                     "}"+\
        #                                     "QCheckBox::indicator::checked{"+\
        #                                     "border: 1px solid; "+\
        #                                     "width: 11px;"+\
        #                                     "height: 11px;"+\
        #                                     "border-color:"+ self.style_component['border_color']+";"+\
        #                                     "border-radius: 5px;"+\
        #                                     "background:" +self.style_component['font_color']+";"+\
        #                                     "}")
        # self.horizontalLayout.addWidget(self.YTX2_fur_mode_cb)
        # self.horizontalLayout.setStretch(0, 1)
        # self.horizontalLayout.setStretch(1, 1)



        # # self.YTX2_count_sb = customQspinBox(Dialog)
        # # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        # # sizePolicy.setHorizontalStretch(0)
        # # sizePolicy.setVerticalStretch(0)
        # # sizePolicy.setHeightForWidth(self.YTX2_count_sb.sizePolicy().hasHeightForWidth())
        # # self.YTX2_count_sb.setFixedHeight(26)
        # # self.YTX2_count_sb.setSizePolicy(sizePolicy)
        # # self.YTX2_count_sb.setObjectName(_fromUtf8("YTX2_count_sb"))
        # # self.YTX2_count_sb.setAlignment(QtCore.Qt.AlignCenter)
        # # self.YTX2_count_sb.setMinimum(1)
        # # self.YTX2_count_sb.set_style('updown')
        # self.YTX2_count_hl.addWidget(self.YTX2_select_mode_wg)


        # spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # self.YTX2_count_hl.addItem(spacerItem1)


        # self.YTX2_count_hl.setStretch(0, 1)
        # self.YTX2_count_hl.setStretch(1, 5)
        # self.YTX2_count_hl.setStretch(2, 1)
        # self.YTX2_main_vl.addLayout(self.YTX2_count_hl)

        # spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # self.YTX2_main_vl.addItem(spacerItem2)

        self.YTX2_btn_hl = QtGui.QHBoxLayout()
        self.YTX2_btn_hl.setObjectName(_fromUtf8("YTX2_btn_hl"))

        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.YTX2_btn_hl.addItem(spacerItem3)

        self.YTX2_ok_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YTX2_ok_btn.sizePolicy().hasHeightForWidth())
        self.YTX2_ok_btn.setSizePolicy(sizePolicy)
        self.YTX2_ok_btn.setObjectName(_fromUtf8("YTX2_ok_btn"))
        self.YTX2_ok_btn.setStyleSheet(
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
        self.YTX2_btn_hl.addWidget(self.YTX2_ok_btn)

        self.YTX2_cancel_btn = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YTX2_cancel_btn.sizePolicy().hasHeightForWidth())
        self.YTX2_cancel_btn.setSizePolicy(sizePolicy)
        self.YTX2_cancel_btn.setObjectName(_fromUtf8("YTX2_cancel_btn"))
        self.YTX2_cancel_btn.setStyleSheet(
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
        self.YTX2_btn_hl.addWidget(self.YTX2_cancel_btn)

        self.cb_list.append(self.YTX2_grm_mode_cb)
        self.cb_list.append(self.YTX2_fur_mode_cb)

        self.YTX2_btn_hl.setStretch(0, 3)
        self.YTX2_btn_hl.setStretch(1, 1)
        self.YTX2_btn_hl.setStretch(2, 1)
        self.YTX2_main_vl.addLayout(self.YTX2_btn_hl)
        self.YTX2_main_vl.setStretch(0, 1)
        self.YTX2_main_vl.setStretch(1, 2)
        # self.YTX2_main_vl.setStretch(2, 1)
        self.YTX2_main_vl.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.YTX2_main_vl)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.set_link()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.YTX2_contents_lb.setText( u"가져올 cache 타입을 선택해주십시오.")
        # self.YTX2_grm_mode_cb.setText(".grm (Asset)")
        # self.YTX2_fur_mode_cb.setText(".fur (Shot)")
        self.YTX2_ok_btn.setText(u"확인")
        self.YTX2_cancel_btn.setText( u"취소")


    def set_link(self):
        self.YTX2_ok_btn.clicked.connect(self.set_add_count)
        self.YTX2_cancel_btn.clicked.connect(self.cancel_and_close)
        # for _cb in self.cb_list:
        #     _cb.clicked.connect(partial(self.check_checked, _cb))




    def set_add_count(self):
        self.accept()



    def cancel_and_close(self):
        self.reject()


    # def check_checked(self, cur_cb :QtGui.QCheckBox) -> None:
    #     for _ch in self.cb_list:
    #         if _ch.text() == cur_cb.text():
    #             _ch.setChecked(True)
    #         else:
    #             _ch.setChecked(False)


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





    def get_res(self) -> None:
        # for _cb in self.cb_list:
        #     if _cb.isChecked() == True:
        #         return _cb.text()
            
        return None