# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_milki.ui'
#
# Created: Tue May 14 14:12:32 2019
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui




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

class Ui_Milki(object):
    def __init__(self):
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
    def setupUi(self, Milki):
        def move_center(main_win):
            qr = main_win.frameGeometry()
            cp = QtGui.QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            main_win.move(qr.topLeft())

        Milki.setObjectName(_fromUtf8("Milki"))
        # Milki.resize(500, 700)
        Milki.resize(750, 700)
        move_center(Milki)
        Milki.setStyleSheet("background : "+self.style_component['background_color']+";}")

        self.verticalLayout_2 = QtGui.QVBoxLayout(Milki)
        self.verticalLayout_2.setMargin(2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.main_vboxlayout = QtGui.QVBoxLayout()
        self.main_vboxlayout.setSpacing(2)
        self.main_vboxlayout.setObjectName(_fromUtf8("main_vboxlayout"))
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setProperty("value", 70)
        self.progressbar.setFixedHeight(6)
        self.progressbar.setTextVisible(False)
        self.progressbar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressbar.setStyleSheet("QProgressBar{"+\
                                                    "border: none;"+\
                                                    "padding: 0px;"+\
                                                    "border-radius: 3px;"+\
                                                    "background: #000000"+\
                                                "}"+\
                                        "QProgressBar::chunk{"+\
                                                    "background: #00b67f;"+\
                                                    "border-radius: 3px;"+\
                                                    "border: none;"+\
                                        "}")
        self.main_vboxlayout.addWidget(self.progressbar)

        self.item_title_vboxlayout = QtGui.QHBoxLayout()
        self.item_title_vboxlayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.item_title_vboxlayout.setObjectName(_fromUtf8("item_title_vboxlayout"))
        self.main_vboxlayout.addLayout(self.item_title_vboxlayout)


        # spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        # self.main_vboxlayout.addItem(spacerItem)


        # spacerItem1 = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        # self.main_vboxlayout.addItem(spacerItem1)

        self.center_vboxlayout = QtGui.QVBoxLayout()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        #self.center_vboxlayout.setSizePolicy(sizePolicy)
        self.center_vboxlayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.center_vboxlayout.setObjectName(_fromUtf8("center_vboxlayout"))
        self.main_vboxlayout.addLayout(self.center_vboxlayout)

        spacerItem_between_thumb_desc_btn = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.main_vboxlayout.addItem(spacerItem_between_thumb_desc_btn)

        self.continue_pushbutton = QtGui.QPushButton()
        self.continue_pushbutton.setMinimumSize(QtCore.QSize(0, 50))
        self.continue_pushbutton.setObjectName(_fromUtf8("continue_pushbutton"))
        self.continue_pushbutton.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px ;"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")

        self.main_vboxlayout.addWidget(self.continue_pushbutton)
        self.verticalLayout_2.addLayout(self.main_vboxlayout)

        self.retranslateUi(Milki)



    def retranslateUi(self, Milki):
        Milki.setWindowTitle(_translate("Milki", "Milki", None))
        self.continue_pushbutton.setText(_translate("Milki", "Continue", None))
