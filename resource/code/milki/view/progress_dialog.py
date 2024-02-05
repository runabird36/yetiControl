import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
import milki_window_adaptor 

class ProgressDialog(QtGui.QWidget):

    icon_label = None
    msg_label = None

    def __init__(self, parent):
        window_parent = milki_window_adaptor.get_parent("MAYA")
        QtGui.QWidget.__init__(self, window_parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.main_hboxlayout = QtGui.QHBoxLayout(self)
        #self.setModal(True)
        self.main_hboxlayout.setMargin(2)
        self.setMinimumSize(QtCore.QSize(250, 50))
        self.setMaximumSize(QtCore.QSize(250, 50))

        # self.icon_label = QtGui.QLabel(self)
        # self.icon_label.setText("Icon Test")
        self.msg_label = QtGui.QLabel(self)
        self.msg_label.setText("MSG Test")

        # self.main_hboxlayout.addWidget(self.icon_label)
        self.main_hboxlayout.addWidget(self.msg_label)
    
    def set_message(self, msg):
        self.msg_label.setText(msg)
    


