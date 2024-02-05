# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\pipeline\playground\tools\BlackHole\common\view\ui_progressbar.ui'
#
# Created: Mon Oct  7 12:01:05 2019
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

# from PyQt4 import QtCore, QtGui
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

class Ui_ProgressbarUI(object):
    progress_window = None
    style_component ={}
    def __init__(self):
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
        self.progress_window = QtGui.QDialog()
        self.progress_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self.progress_window)
        self.progress_window.show()



    def setupUi(self, ProgressbarUI):
        ProgressbarUI.setObjectName(_fromUtf8("ProgressbarUI"))
        ProgressbarUI.resize(386, 49)
        ProgressbarUI.setStyleSheet("background : "+self.style_component['background_color']+";}")
        self.horizontalLayout = QtGui.QHBoxLayout(ProgressbarUI)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.blackhole_pb = QtGui.QProgressBar(ProgressbarUI)
        self.blackhole_pb.setProperty("value", 24)
        self.blackhole_pb.setObjectName(_fromUtf8("blackhole_pb"))
        self.blackhole_pb.setStyleSheet("QProgressBar{"+\
                                                    "border: none;"+\
                                                    "padding: 0px;"+\
                                                    "border-radius: 5px;"+\
                                                    "background: #000000;"+\
                                                    "text-align: center;"+\
                                                    "height: 5px;"+\
                                                "}"+\
                                        "QProgressBar::chunk{"+\
                                                    "background: #6748D9;"+\
                                                    "border-radius: 5px;"+\
                                                    "border: none;"+\
                                        "}")
        self.horizontalLayout.addWidget(self.blackhole_pb)

        self.retranslateUi(ProgressbarUI)
        QtCore.QMetaObject.connectSlotsByName(ProgressbarUI)

    def retranslateUi(self, ProgressbarUI):
        ProgressbarUI.setWindowTitle(_translate("ProgressbarUI", "Form", None))


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     ProgressbarUI = QtGui.QWidget()
#     ui = Ui_ProgressbarUI()
#     ui.setupUi(ProgressbarUI)
#     ProgressbarUI.show()
#     sys.exit(app.exec_())
