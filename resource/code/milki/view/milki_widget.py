
import sys
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from importlib import reload
import ui_milki
reload (ui_milki)
from ui_milki import Ui_Milki

import milki_window_adaptor
reload (milki_window_adaptor)

import item_title
reload(item_title)
from item_title import ItemTitle

import pannel_supply
reload (pannel_supply)
from pannel_supply import PannelSupply

import msgbox_collector

import progress_dialog
reload (progress_dialog)
from progress_dialog import ProgressDialog

class MilkiWidget(QtGui.QWidget):

    continue_step = QtCore.Signal(str)

    _ui = None
    current_panel = None
    p_supply = None
    continue_button = None
    controller = None
    progressbar = None
    progressdialog = None
    _item_titles = []

    def __init__(self, controller, app_name):
        self._app_name = app_name
        self.controller = controller
        try:
            adaptor = milki_window_adaptor
            window_parent = adaptor.get_parent(app_name)
        except Exception as e:
            print(str(e))
            return

        # window_parent = self.get_parent()
        QtGui.QWidget.__init__(self, window_parent)
        self._ui = Ui_Milki()
        self.setWindowFlags(QtCore.Qt.Window)
        self.p_supply = PannelSupply()


    def setup(self):
        self._ui.setupUi(self)
        self.continue_button = self._ui.continue_pushbutton
        self.continue_button.clicked.connect(self.controller.continue_step)
        self.progressbar = self._ui.progressbar


    def get_progress_dialog(self):
        self.progressdialog = ProgressDialog(self)
        return self.progressdialog


    def swap_center_item(self, item):
        if not self.current_panel is None:
            panel = self._ui.center_vboxlayout.takeAt(0)

            self._ui.center_vboxlayout.removeWidget(panel.widget())
            panel.widget().hide()


        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self._ui.main_vboxlayout.insertItem(2, spacerItem)
        panel = self.p_supply.get_item_pannel(item)
        if panel is None:
            return

        self.current_panel = panel
        self.current_panel.clear_all_items()
        self.current_panel.show()
        self.set_item_panel(item, panel)
        self._ui.main_vboxlayout.removeItem(spacerItem)
        self._ui.center_vboxlayout.addWidget(panel)

        self._ui.center_vboxlayout.invalidate()
        self._ui.center_vboxlayout.update()
        self._ui.main_vboxlayout.invalidate()
        self.repaint()


    def set_item_panel(self, item, panel):
        item.set_panel(panel)
        if item.get_type() == "Selector" and item.get_title() == "Shot MDL Options":
            item.set_select_widgets(item.get_items())
            item.set_siganls()
            return
        if item.get_type() == "Selector":
            item.set_select_widgets(item.get_items())


    def put_titles(self, titles):
        self._item_titles = []

        for i in reversed(range(self._ui.item_title_vboxlayout.count())):
            self._ui.item_title_vboxlayout.itemAt(i).widget().setParent(None)

        for idx, title in enumerate(titles):
            item_title = ItemTitle(self, title, idx)
            self._ui.item_title_vboxlayout.addWidget(item_title)
            self._item_titles.append(item_title)

        return self._item_titles

    def get_item_title(self, idx):

        if len(self._item_titles)-1 < idx-1:
            return
        return self._item_titles[idx-1]

    def change_progress(self, value):
        self.progressbar.setValue(value)


    def show_error_popup_dialog(self, error_text):
        '''error dialog function
            input: string : error content'''
        border_color = "#595959"
        font_weight = "15"
        font_size = "10"
        font_color = "#D9D9D9"
        font_color_pressed = "#595959"
        background_color = "#333333"
        button_color = "rgba(70,70,70,0.5)"
        msg_width = "60"
        msg_height = "18"
        if sys.platform.count("win"):
            prePath = "/usersetup/linux/scripts/maya_sc/milki/icons/"
        else:
            prePath = "/usersetup/linux/scripts/maya_sc/milki/icons/"
        self.error_window = msgbox_collector.CustomConfirmDialog('Milki', error_text, ['ok'])
        self.error_window.setStyleSheet(
                                        "QDialog{"+\
                                        "image: url(" + prePath + "error_img_resize.png);"+\
                                        "image-position: top;"+\
                                        "padding-top: 11px;"+\
                                        "border-style: solid;"+\
                                        "border-width : 0.5px;"+\
                                        "border-color: "+ border_color +";"+\
                                        "border-radius: 2px;"+\
                                        "color : "+ font_color +";"+\
                                        "background:" +background_color+";"+\
                                        "}"+\
                                        "QLabel{"+\
                                        "color : "+font_color+";"+\
                                        "font-size : 15px;"+\
                                        "qproperty-alignment: AlignCenter;"+\
                                        "padding-bottom: 2px;"+\
                                        "}"+\
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
                                            "font: 11px;"+\
                                            "color:"+ font_color_pressed +";"+\
                                            "border-color:" +background_color+";"+\
                                            "border-radius: 5px;"+\
                                            "background-color:" +font_color+";"+\
                                            "}"
                                        )
        self.error_window.show()

    def show_complete_dialog(self):


        msg_box = QtGui.QMessageBox()
        desktop_widget = QtGui.QDesktopWidget()
        msg_box.move((desktop_widget.width() / 2 - msg_box.frameGeometry().width()) / 2, (desktop_widget.height() - msg_box.frameGeometry().height()) / 2);
        answer = msg_box.warning(msg_box,"complete", "complete!", buttons = QtGui.QMessageBox.Ok, defaultButton = QtGui.QMessageBox.Cancel)

        self.hide()
        self.close()

    def show_complete_popup_dialog(self, error_text):
        '''error dialog function
            input: string : error content'''
        border_color = "#595959"
        font_weight = "15"
        font_size = "10"
        font_color = "#D9D9D9"
        font_color_pressed = "#595959"
        background_color = "#333333"
        button_color = "rgba(70,70,70,0.5)"
        msg_width = "60"
        msg_height = "18"
        if sys.platform.count("win"):
            prePath = "Z:/backstage/multi/pluto/icons/"
        else:
            prePath = "/usersetup/linux/scripts/maya_sc/milki/icons/"
        self.complete_window = msgbox_collector.CustomConfirmDialog('Milki', error_text, ['Open pub folder', 'Version Up', 'Ok'], 400, 150)
        self.complete_window.setStyleSheet(
                                        "QDialog{"+\
                                        "image: url(" + prePath + "check_img.png);"+\
                                        "image-position: top;"+\
                                        "padding-top: 11px;"+\
                                        "border-style: solid;"+\
                                        "border-width : 0.5px;"+\
                                        "border-color: "+ border_color +";"+\
                                        "border-radius: 2px;"+\
                                        "color : "+ font_color +";"+\
                                        "background:" +background_color+";"+\
                                        "}"+\
                                        "QLabel{"+\
                                        "color : "+font_color+";"+\
                                        "font-size : 15px;"+\
                                        "qproperty-alignment: AlignCenter;"+\
                                        "padding-bottom: 2px;"+\
                                        "}"+\
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
                                            "font: 11px;"+\
                                            "color:"+ font_color_pressed +";"+\
                                            "border-color:" +background_color+";"+\
                                            "border-radius: 5px;"+\
                                            "background-color:" +font_color+";"+\
                                            "}"
                                        )

        self.complete_window.show()
        self.complete_window.exec_()
        try:
            answer = self.complete_window.selectedBtn
            return answer
        except:
            return ""
