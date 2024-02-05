# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_exporter.ui'
#
# Created: Mon May 20 12:08:41 2019
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

class Ui_Exporter(object):
    def setupUi(self, Exporter):
        Exporter.setObjectName(_fromUtf8("Exporter"))
        Exporter.resize(446, 525)
        Exporter.setMinimumSize(QtCore.QSize(0, 130))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Exporter)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.main_vboxlayout = QtGui.QVBoxLayout()
        self.main_vboxlayout.setObjectName(_fromUtf8("main_vboxlayout"))
        self.pub_info_label = QtGui.QLabel(Exporter)
        self.pub_info_label.setMinimumSize(QtCore.QSize(0, 40))
        self.pub_info_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pub_info_label.setObjectName(_fromUtf8("pub_info_label"))
        self.main_vboxlayout.addWidget(self.pub_info_label)
        self.task_label = QtGui.QLabel(Exporter)
        self.task_label.setObjectName(_fromUtf8("task_label"))
        self.main_vboxlayout.addWidget(self.task_label)
        self.pub_files_tree_widget = QtGui.QTreeWidget(Exporter)
        self.pub_files_tree_widget.setMinimumSize(QtCore.QSize(0, 300))
        self.pub_files_tree_widget.setRootIsDecorated(False)
        self.pub_files_tree_widget.setObjectName(_fromUtf8("pub_files_tree_widget"))
        self.pub_files_tree_widget.headerItem().setText(0, _fromUtf8("1"))
        self.pub_files_tree_widget.header().setVisible(False)
        self.main_vboxlayout.addWidget(self.pub_files_tree_widget)
        self.titles_hboxlayout = QtGui.QHBoxLayout()
        self.titles_hboxlayout.setObjectName(_fromUtf8("titles_hboxlayout"))
        self.thumb_title_label = QtGui.QLabel(Exporter)
        self.thumb_title_label.setMinimumSize(QtCore.QSize(210, 0))
        self.thumb_title_label.setMaximumSize(QtCore.QSize(210, 16777215))
        self.thumb_title_label.setObjectName(_fromUtf8("thumb_title_label"))
        self.titles_hboxlayout.addWidget(self.thumb_title_label)
        self.desc_title_label = QtGui.QLabel(Exporter)
        self.desc_title_label.setObjectName(_fromUtf8("desc_title_label"))
        self.titles_hboxlayout.addWidget(self.desc_title_label)
        self.main_vboxlayout.addLayout(self.titles_hboxlayout)
        self.thumb_desc_hboxlayout = QtGui.QHBoxLayout()
        self.thumb_desc_hboxlayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.thumb_desc_hboxlayout.setObjectName(_fromUtf8("thumb_desc_hboxlayout"))
        self.thumb_label = QtGui.QLabel(Exporter)
        self.thumb_label.setMinimumSize(QtCore.QSize(210, 130))
        self.thumb_label.setMaximumSize(QtCore.QSize(210, 130))
        self.thumb_label.setObjectName(_fromUtf8("thumb_label"))
        self.thumb_desc_hboxlayout.addWidget(self.thumb_label)
        self.desc_text_edit = QtGui.QTextEdit(Exporter)
        self.desc_text_edit.setMinimumSize(QtCore.QSize(0, 130))
        self.desc_text_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.desc_text_edit.setObjectName(_fromUtf8("desc_text_edit"))
        self.thumb_desc_hboxlayout.addWidget(self.desc_text_edit)
        self.main_vboxlayout.addLayout(self.thumb_desc_hboxlayout)
        self.verticalLayout_2.addLayout(self.main_vboxlayout)

        self.retranslateUi(Exporter)
        QtCore.QMetaObject.connectSlotsByName(Exporter)

    def retranslateUi(self, Exporter):
        Exporter.setWindowTitle(_translate("Exporter", "Form", None))
        self.pub_info_label.setText(_translate("Exporter", "TextLabel", None))
        self.task_label.setText(_translate("Exporter", "TextLabel", None))
        self.thumb_title_label.setText(_translate("Exporter", "Thumbnail", None))
        self.desc_title_label.setText(_translate("Exporter", "Description", None))
        self.thumb_label.setText(_translate("Exporter", "TextLabel", None))

