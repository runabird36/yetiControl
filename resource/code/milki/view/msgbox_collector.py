import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from functools import partial



def show_complete_dialog():
    '''open complete message box popup'''

    msg_box = QtGui.QMessageBox()
    desktop_widget = QtGui.QDesktopWidget()
    msg_box.move((desktop_widget.width() / 2 - msg_box.frameGeometry().width()) / 2, (desktop_widget.height() - msg_box.frameGeometry().height()) / 2);
    answer = msg_box.warning(msg_box,"complete", "complete!", buttons = QtGui.QMessageBox.Ok, defaultButton = QtGui.QMessageBox.Cancel)


    if answer == QtGui.QMessageBox.StandardButton.FirstButton:
        return 'OK'
    else:
        return 'cancel'

class CustomConfirmDialog(QtGui.QDialog):
    def __init__(self, title = None, message= None, button = None, width = None, height = None):
        QtGui.QDialog.__init__(self)

        self.resize(260, 180)
        if width is not None or height is not None:
            self.resize(width, height)

        if not title == None:
            self.setWindowTitle(title)
        #Label, Edit, Button Control

        if not message == None:
            message_label = QtGui.QLabel(message)

        self.currnentIndex = -1
        #Layout
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(message_label,1, QtCore.Qt.AlignBottom)


        if not button == None:
            btnLayout = QtGui.QHBoxLayout()
            for index, btnTitle in enumerate(button):
                pushButton = QtGui.QPushButton(btnTitle)
                pushButton.clicked.connect(partial(self.btnClicked, btnTitle))
                btnLayout.addWidget(pushButton)

        mainLayout.addLayout(btnLayout)
        #Designation Layout at Dialog

        self.setLayout(mainLayout)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def btnClicked(self, btnTitle):
        self.selectedBtn = btnTitle
        self.hide()
