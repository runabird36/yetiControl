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
    def setupUi(self, Milki):
        Milki.setObjectName(_fromUtf8("Milki"))
        Milki.resize(430, 683)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Milki)
        self.verticalLayout_2.setMargin(2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.main_vboxlayout = QtGui.QVBoxLayout()
        self.main_vboxlayout.setSpacing(2)
        self.main_vboxlayout.setObjectName(_fromUtf8("main_vboxlayout"))
        self.item_title_vboxlayout = QtGui.QHBoxLayout()
        self.item_title_vboxlayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.item_title_vboxlayout.setObjectName(_fromUtf8("item_title_vboxlayout"))


        self.main_vboxlayout.addLayout(self.item_title_vboxlayout)
        spacerItem = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.main_vboxlayout.addItem(spacerItem)
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setProperty("value", 16)
        self.progressbar.setTextVisible(False)
        self.progressbar.setObjectName(_fromUtf8("progressbar"))
        self.main_vboxlayout.addWidget(self.progressbar)
        spacerItem1 = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)

        self.main_vboxlayout.addItem(spacerItem1)
        self.center_vboxlayout = QtGui.QVBoxLayout()
        self.center_vboxlayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.center_vboxlayout.setObjectName(_fromUtf8("center_vboxlayout"))
        self.main_vboxlayout.addLayout(self.center_vboxlayout)
        
        self.continue_pushbutton = QtGui.QPushButton()
        self.continue_pushbutton.setMinimumSize(QtCore.QSize(0, 50))
        self.continue_pushbutton.setObjectName(_fromUtf8("continue_pushbutton"))

        self.main_vboxlayout.addWidget(self.continue_pushbutton)
        self.verticalLayout_2.addLayout(self.main_vboxlayout)

        self.retranslateUi(Milki)

      

    def retranslateUi(self, Milki):
        Milki.setWindowTitle(_translate("Milki", "Milki", None))
        self.continue_pushbutton.setText(_translate("Milki", "Continue", None))

