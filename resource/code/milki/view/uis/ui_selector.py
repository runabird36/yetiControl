# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_selector.ui'
#
# Created: Thu May 16 12:36:27 2019
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(434, 512)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.checkBox_3 = QtGui.QCheckBox(Form)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.horizontalLayout_2.addWidget(self.checkBox_3)
        self.checkBox_2 = QtGui.QCheckBox(Form)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.checkBox = QtGui.QCheckBox(Form)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "TextLabel", None))
        self.label_2.setText(_translate("Form", "TextLabel", None))
        self.checkBox_3.setText(_translate("Form", "CheckBox", None))
        self.checkBox_2.setText(_translate("Form", "CheckBox", None))
        self.checkBox.setText(_translate("Form", "CheckBox", None))

