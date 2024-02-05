
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui




class QCustomQWidget (QtGui.QWidget):
    
    def __init__ (self, item_info,item_img_info_list, parent =None):
        super(QCustomQWidget, self).__init__(parent)

        # self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.file_name_label    = QtGui.QLabel()
        # self.textQVBoxLayout.addWidget(self.textUpQLabel)

        self.allQHBoxLayout  = QtGui.QHBoxLayout()

        self.icon_draggable_label = QtGui.QLabel()
        # self.icon_draggable_btn = QtGui.QPushButton()
        self.icon_format_label    = QtGui.QLabel()
        self.icon_draggable_label.setCursor(QtCore.Qt.OpenHandCursor)
        self.icon_success_label   = QtGui.QLabel()


        self.allQHBoxLayout.addWidget(self.icon_draggable_label, 0)
        self.allQHBoxLayout.addWidget(self.icon_format_label, 1)
        self.allQHBoxLayout.addWidget(self.file_name_label , 2)
        # self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 2)
        self.allQHBoxLayout.addWidget(self.icon_success_label, 3)

        self.setLayout(self.allQHBoxLayout)
        print item_info
        self.set_data(item_info, item_img_info_list)

    

    def set_data(self, item_info, item_img_info_list):
        print item_info
        print 'custom item init'
        self.file_name_label.setText(item_info)
        self.icon_draggable_label.setPixmap(QtGuiOrig.QPixmap(item_img_info_list[0]))
        self.icon_format_label.setPixmap(QtGuiOrig.QPixmap(item_img_info_list[1]))
        self.icon_success_label.setPixmap(QtGuiOrig.QPixmap(item_img_info_list[2]))
