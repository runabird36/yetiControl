from ast import main
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from functools import partial
import os
import CQT_path_module
from qt_material import apply_stylesheet
class Mcollection():
    def msg_complete(self):
        '''open complete message box popup'''

        msg_box = QtGui.QMessageBox()
        desktop_widget = QtGui.QDesktopWidget()
        msg_box.move((desktop_widget.width() / 2 - msg_box.frameGeometry().width()) / 2, (desktop_widget.height() - msg_box.frameGeometry().height()) / 2);
        answer = msg_box.warning(msg_box,"complete", "complete!", buttons = QtGui.QMessageBox.Ok, defaultButton = QtGui.QMessageBox.Cancel)


        if answer == QtGui.QMessageBox.StandardButton.FirstButton:
            return 'OK'
        else:
            return 'cancel'

    def msg_confirm_create_file(self, app_name):
        '''message box that confirm changing status'''
        msg_box = QtGui.QMessageBox()
        desktop_widget = QtGui.QDesktopWidget()
        msg_box.move((desktop_widget.width() / 2 - msg_box.frameGeometry().width()) / 2, (desktop_widget.height() - msg_box.frameGeometry().height()) / 2);

        if app_name == 'HOUDINI':
            msg_box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        else:
            msg_box.setWindowFlags(QtCore.Qt.Window)


        border_color = "#595959"
        font_weight = "15"
        font_size = "10"
        font_color = "#D9D9D9"
        font_color_pressed = "#595959"
        background_color = "#333333"
        button_color = "rgba(70,70,70,0.5)"
        msg_width = "60"
        msg_height = "18"

        msg_box.setStyleSheet(
                            "QMessageBox{"+\
                                "border-style: solid;"+\
                                "border-width : 0.5px;"+\
                                "border-color: "+ border_color +";"+\
                                "border-radius: 2px;"+\
                                "color : "+ font_color +";"+\
                                "background:" +background_color+";"+\
                                "}"
                            "QPushButton{"+\
                                "width : "+msg_width+";"+\
                                "height : "+msg_height+";"+\
                                "font: 13px  ;"+\
                                "border: 1px solid;"+\
                                "border-color:"+ border_color+";"+\
                                "border-radius: 5px;"+\
                                "background-color:"+button_color+";"+\
                                "color:"+ font_color +";"+\
                                "}"+\
                            "QPushButton:pressed{"+\
                                "width : "+msg_width+";"+\
                                "height : "+msg_height+";"+\
                                "color:"+ font_color_pressed +";"+\
                                "border-color:" +background_color+";"+\
                                "border-radius: 5px;"+\
                                "background-color:" +font_color+";"+\
                                "}"
                            )

        message_str =       "<span style=\" font-size:"+ font_size+"pt; font-weight:"+ font_weight+"; color:"+ font_color+";\">"+\
                            "Do you want to create file?"+\
                            "</span>"


        answer = msg_box.question(msg_box, "Pluto", message_str , buttons = QtGui.QMessageBox.Ok, defaultButton = QtGui.QMessageBox.Cancel)


        if answer == QtGui.QMessageBox.StandardButton.FirstButton:
            return 'OK'
        else:
            return 'cancel'

    def msg_confirm_status_change(self, app_name, old_status, new_status):
        '''message box that confirm changing status'''
        msg_box = QtGui.QMessageBox()
        desktop_widget = QtGui.QDesktopWidget()
        msg_box.move((desktop_widget.width() / 2 - msg_box.frameGeometry().width()) / 2, (desktop_widget.height() - msg_box.frameGeometry().height()) / 2);


        if app_name == 'HOUDINI':
            msg_box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        else:
            msg_box.setWindowFlags(QtCore.Qt.Window)

        border_color = "#595959"
        font_weight = "15"
        font_size = "10"
        font_color = "#D9D9D9"
        font_color_pressed = "#595959"
        background_color = "#333333"
        button_color = "rgba(70,70,70,0.5)"
        msg_width = "60"
        msg_height = "18"



        msg_box.setStyleSheet(
                            "QMessageBox{"+\
                                "border-style: solid;"+\
                                "border-width : 0.5px;"+\
                                "border-color: "+ border_color +";"+\
                                "border-radius: 2px;"+\
                                "color : "+ font_color +";"+\
                                "background:" +background_color+";"+\
                                "}"
                            "QPushButton{"+\
                                "width : "+msg_width+";"+\
                                "height : "+msg_height+";"+\
                                "font: 13px  ;"+\
                                "border: 1px solid;"+\
                                "border-color:"+ border_color+";"+\
                                "border-radius: 5px;"+\
                                "background-color:"+button_color+";"+\
                                "color:"+ font_color +";"+\
                                "}"+\
                            "QPushButton:pressed{"+\
                                "width : "+msg_width+";"+\
                                "height : "+msg_height+";"+\
                                "color:"+ font_color_pressed +";"+\
                                "border-color:" +background_color+";"+\
                                "border-radius: 5px;"+\
                                "background-color:" +font_color+";"+\
                                "}"
                            )
        self.get_old_new_color(old_status, new_status)

        message_str =       "<span style=\" font-size:"+ font_size+"pt; font-weight:"+ font_weight+"; color:"+ font_color+";\">"+\
                                "Do you want to change status" +\
                            "</span>"+\
                        "<br> "+\
                            "<span style=\" font-size:"+ font_size+"pt; font-weight:"+ font_weight+"; color:"+self.old_status_color+";\">"+\
                                old_status +\
                            "</span>"+\
                            "<span style=\" font-size:"+ font_size+"pt; font-weight:"+ font_weight+"; color:"+ font_color+";\">"+\
                                "->" +\
                            "</span>"+\
                            "<span style=\" font-size:"+ font_size+"pt; font-weight:"+ font_weight+"; color:" + self.new_status_color +";\">"+\
                                new_status +\
                            "</span>"+\
                            "<span style=\" font-size:"+ font_size+"pt; font-weight:"+ font_weight+"; color:"+ font_color+";\">"+\
                                "?" +\
                            "</span>"


        answer = msg_box.information(msg_box, "Pluto", message_str , buttons = QtGui.QMessageBox.Yes, defaultButton = QtGui.QMessageBox.No)

        if answer == QtGui.QMessageBox.StandardButton.Yes:
            return 'OK'
        else:
            return 'cancel'

    def get_old_new_color(self, old_status, new_status):
        print(old_status)
        print(new_status)
        if old_status == 'retake':
            self.old_status_color = '#f05353' #red
        elif old_status == 'ip':
            self.old_status_color = '#55f473' #green
        elif old_status == 'pub':
            self.old_status_color = '#50afff' #blue
        elif old_status == 'wtg' or old_status == 'rdy':
            self.old_status_color = '#D9D9D9' #default

        if new_status == 'retake':
            self.new_status_color = '#f05353'
        elif new_status == 'ip':
            self.new_status_color = '#55f473'
        elif new_status == 'pub':
            self.new_status_color = '#50afff'
        elif new_status == 'wtg'or old_status == 'rdy':
            self.new_status_color = '#D9D9D9'





class CustomConfirmDialog(QtGui.QDialog):
    def __init__(self, _parent=None, title = None, message= None, status="clear", button = None, width = None, height = None, dialog_dis_type="show"):
        # QtGui.QDialog.__init__(self)
        super(CustomConfirmDialog, self).__init__(_parent)
        
        # self.btn_clicked        = QtCore.pyqtSignal()

        self.selected_btn_str   = ""
        
        if width == None or height == None:
            self.resize(260, 180)
        else:
            self.resize(width, height)

        if not title == None:
            self.setWindowTitle(title)
        #Label, Edit, Button Control

        self.icon_label = QtGui.QLabel()

        if not message == None:
            message_label = QtGui.QLabel(message)
            # message_label.setAlignment(QtCore.Qt.AlignCenter)

        self.currnentIndex = -1
        #Layout
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.icon_label , 0, QtCore.Qt.AlignCenter)
        # mainLayout.addWidget(message_label,1, QtCore.Qt.AlignBottom)
        mainLayout.addWidget(message_label,1, QtCore.Qt.AlignCenter)


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
        self.set_status_icon(status)
        apply_stylesheet(self, CQT_path_module.get_theme())

        if dialog_dis_type == "show":
            self.show()
    def set_status_icon(self, status: str) -> None:
        
        if status   == "clear":
            _path   = CQT_path_module.check_img
        elif status == "error":
            _path   = CQT_path_module.error_img
        elif status == "warnning":
            _path   = CQT_path_module.warnning_img
        _size = 100
        pix_map = QtGuiOrig.QPixmap(_path)
        _w = pix_map.width()
        _h = pix_map.height()
        pix_map = pix_map.scaled(_size,_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.icon_label.setPixmap(pix_map)


    def btnClicked(self, btnTitle):
        self.selected_btn_str = btnTitle
        self.hide()
        self.accept()

    def get_selection(self) -> str:
        return self.selected_btn_str
        


    @property
    def selected_btn(self) -> str:
        return self.selected_btn_str



