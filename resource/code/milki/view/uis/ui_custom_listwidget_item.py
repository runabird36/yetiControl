# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\taiyoung.song\Desktop\ui_custom_listwidget_item.ui'
#
# Created: Tue Jun  4 12:41:08 2019
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
        Form.resize(424, 70)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.draggable_icon_label = QtGui.QLabel(Form)
        self.draggable_icon_label.setText(_fromUtf8(""))
        self.draggable_icon_label.setObjectName(_fromUtf8("draggable_icon_label"))
        self.horizontalLayout.addWidget(self.draggable_icon_label)
        self.file_format_icon_label = QtGui.QLabel(Form)
        self.file_format_icon_label.setText(_fromUtf8(""))
        self.file_format_icon_label.setObjectName(_fromUtf8("file_format_icon_label"))
        self.horizontalLayout.addWidget(self.file_format_icon_label)
        self.file_name_label = QtGui.QLabel(Form)
        self.file_name_label.setText(_fromUtf8(""))
        self.file_name_label.setObjectName(_fromUtf8("file_name_label"))
        self.horizontalLayout.addWidget(self.file_name_label)
        self.ischecked_icon_label = QtGui.QLabel(Form)
        self.ischecked_icon_label.setText(_fromUtf8(""))
        self.ischecked_icon_label.setObjectName(_fromUtf8("ischecked_icon_label"))
        self.horizontalLayout.addWidget(self.ischecked_icon_label)
        self.checkBox = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout.addWidget(self.checkBox)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 5)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

