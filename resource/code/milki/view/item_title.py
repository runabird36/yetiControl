import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui
from functools import partial

class ItemTitle(QtGui.QWidget):
    item_clicked = QtCore.Signal(int)
    title = None
    title_btn = None
    icon = None
    is_on = False
 

    def __init__(self, parent , title, item_num):
        QtGui.QWidget.__init__(self, parent)
        self.title = title
        self.title_btn = None
        self.setMinimumSize(QtCore.QSize(140, 40))
        self.title_vboxlayout = QtGui.QVBoxLayout(self)
        self.title_vboxlayout.setMargin(0)
        self.title_btn = QtGui.QPushButton(self)
        self.title_btn.setText(self.title)
        self.title_btn.setStyleSheet(
                                        "QPushButton{"+\
                                        "background: #333333;"+\
                                        "border-color: white;"+\
                                        "font : 11px;"+\
                                        "color : #4f4f4f;" +\
                                        "text-align: center;"
                                        "}")
        self.title_btn.clicked.connect(partial(self.emit_item_clicked, item_num))
        self.title_vboxlayout.setAlignment(self.title_btn, QtCore.Qt.AlignCenter)
        self.title_vboxlayout.addWidget(self.title_btn)
        self.title_btn.setEnabled(False)

    
    def emit_item_clicked(self, itm_num):
        self.item_clicked.emit(itm_num)
    
    def toggle(self, status):
        if status == True:
            self.title_btn.setEnabled(True)
            self.title_btn.setStyleSheet(
                                "QPushButton{"+\
                                "background: #00b67f;"+\
                                "border-color: white;"+\
                                "font : 11px;"+\
                                "color :  #22252b;" +\
                                "text-align: center;"
                                "}")

        else:
            self.title_btn.setStyleSheet(
                                "QPushButton{"+\
                                "background: #333333;"+\
                                "border-color: white;"+\
                                "font : 11px;"+\
                                "color : #D1D1D1;" +\
                                "text-align: center;"
                                "}")
