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

class Ui_ProgressbarUI(QtGui.QDialog):
    progress_window = None
    style_component ={}
    def __init__(self, _parent=None):

        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
        # self.progress_window = QtGui.QDialog()
        super(Ui_ProgressbarUI, self).__init__(_parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.show()

        self.IS_CANCEL = False



    def setupUi(self, ProgressbarUI):
        ProgressbarUI.setObjectName(_fromUtf8("ProgressbarUI"))
        ProgressbarUI.resize(600, 140)
        ProgressbarUI.setStyleSheet("background : "+self.style_component['background_color']+";}")
        self.horizontalLayout = QtGui.QVBoxLayout(ProgressbarUI)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.ATX_fname_lb = QtGui.QLabel(ProgressbarUI)
        self.ATX_fname_lb.setObjectName(_fromUtf8("ATX_fname_lb"))
        # self.ATX_fname_lb.setText('aa')
        self.ATX_fname_lb.setFixedWidth(550)
        self.ATX_fname_lb.setFixedHeight(70)
        self.ATX_fname_lb.setStyleSheet(
                                            "QLabel{"+\
                                            "background:" +self.style_component['background_color']+";"+\
                                            "border-radius: 2px;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "font:  13px;"+\
                                            "padding-top : 2px;"+\
                                            "}")
        self.horizontalLayout.addWidget(self.ATX_fname_lb)

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
                                                    "background: #4E7AC7;"+\
                                                    "border-radius: 5px;"+\
                                                    "border: none;"+\
                                        "}")
        self.horizontalLayout.addWidget(self.blackhole_pb)

        self.retranslateUi(ProgressbarUI)
        QtCore.QMetaObject.connectSlotsByName(ProgressbarUI)

    def retranslateUi(self, ProgressbarUI):
        ProgressbarUI.setWindowTitle(_translate("ProgressbarUI", "Form", None))


    def closeEvent(self, _event):
        # super(Ui_ProgressbarUI, self).closeEvent()
        # print(_event)
        self.IS_CANCEL = True


    def update_value(self, from_value, to_value):
        for num in range(from_value, to_value):
            self.blackhole_pb.setValue(num)
            QtGui.QApplication.processEvents()


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     ProgressbarUI = QtGui.QWidget()
#     ui = Ui_ProgressbarUI()
#     ui.setupUi(ProgressbarUI)
#     ProgressbarUI.show()
#     sys.exit(app.exec_())
