# -*- coding:utf-8 -*-

import os
import sys
if sys.version_info.major == 3:
    from importlib import reload
import glob
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui

import custom_list
reload (custom_list)

import custom_list_item
reload (custom_list_item)
import thumb_lable
reload (thumb_lable)
from thumb_lable import Thumbnail


class ExportPanel(QtGui.QWidget):
    back_layout = None
    main_layout = None
    widgets = []
    spacers = []
    tex_items = []
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.style_component = {'background_color': '#333333',
                                'warn_color' : '#ffc107',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.setup()

    def setup(self):
        self.verticalLayout_2 = QtGui.QVBoxLayout(self)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.main_vboxlayout = QtGui.QVBoxLayout()
        self.pub_info_label = QtGui.QLabel(self)
        self.pub_info_label.setMinimumSize(QtCore.QSize(0, 40))
        self.pub_info_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pub_info_label.setText("Test")
        self.pub_info_label.setStyleSheet(
                                "QLabel{"+\
                                "background: "+self.style_component['background_color']+";"+\
                                "border: none;"+\
                                "font : bold 13px;"+\
                                "padding-left: 2px;"+\
                                "}")
        self.main_vboxlayout.addWidget(self.pub_info_label)
        self.pub_files_tree_widget = custom_list.CustomListWidget(self)
        self.pub_files_tree_widget.setMinimumSize(QtCore.QSize(0, 300))
        self.main_vboxlayout.addWidget(self.pub_files_tree_widget)
        spacerItem_between_listwidget_thumb_desc = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.main_vboxlayout.addItem(spacerItem_between_listwidget_thumb_desc)
        self.prepub_view_vl = QtGui.QVBoxLayout()
        self.prepub_view_title_lb = QtGui.QLabel(self)
        self.prepub_view_title_lb.setMinimumSize(QtCore.QSize(210, 0))
        self.prepub_view_title_lb.setMaximumSize(QtCore.QSize(210, 16777215))
        self.prepub_view_title_lb.setText("Do Prepub")
        self.prepub_view_title_lb.setStyleSheet(
                                        "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "font : bold 15px;"+\
                                        "padding-left: 2px;"+\
                                        "}")
        self.prepub_view_vl.addWidget(self.prepub_view_title_lb)

        self.prepub_view_check_cb = QtGui.QCheckBox()
        self.prepub_view_check_cb.setMinimumHeight(30)
        self.prepub_view_check_cb.setMaximumHeight(30)
        self.prepub_view_check_cb.setText("Is prepub data")
        self.prepub_view_check_cb.setStyleSheet(
                            "QCheckBox{"+\
                                "background: "+self.style_component['background_color']+";"+\
                                "border: none;"+\
                                "color: "+ self.style_component['font_color'] +";"+\
                                "font: 11px;"+\
                            "}")
        self.prepub_view_vl.addWidget(self.prepub_view_check_cb)
        self.main_vboxlayout.addLayout(self.prepub_view_vl)

        spacerItem_between_prepub = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.main_vboxlayout.addItem(spacerItem_between_prepub)

        self.titles_hboxlayout = QtGui.QHBoxLayout()

        self.thumb_title_label = QtGui.QLabel(self)
        self.thumb_title_label.setMinimumSize(QtCore.QSize(210, 0))
        self.thumb_title_label.setMaximumSize(QtCore.QSize(210, 16777215))
        self.thumb_title_label.setText("Thumbnail")
        self.thumb_title_label.setStyleSheet(
                                        "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "font : bold 13px;"+\
                                        "padding-left: 2px;"+\
                                        "}")

        self.titles_hboxlayout.addWidget(self.thumb_title_label)
        self.desc_title_label = QtGui.QLabel(self)
        self.desc_title_label.setText("Description")
        self.desc_title_label.setStyleSheet(
                                        "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "font : bold 13px;"+\
                                        "padding-left: 2px;"+\
                                        "}")

        self.titles_hboxlayout.addWidget(self.desc_title_label)
        self.main_vboxlayout.addLayout(self.titles_hboxlayout)

        spacerItem_between_titles_boxs = QtGui.QSpacerItem(20, 7, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.main_vboxlayout.addItem(spacerItem_between_titles_boxs)

        self.thumb_desc_hboxlayout = QtGui.QHBoxLayout()
        self.thumb_desc_hboxlayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)

        self.thumb_label = Thumbnail(self)

        self.thumb_label.setMinimumSize(QtCore.QSize(210, 220))
        self.thumb_label.setMaximumSize(QtCore.QSize(210, 220))
        if sys.platform.count("win"):
            cam_img = 'Z:/backstage/maya/publisher_v02/icon/camera.png'
        else:
            cam_img = '/usersetup/linux/module/ui_icons_md/camera.png'
        self.thumb_label.set_thumb_from_path(cam_img)
        self.thumb_desc_hboxlayout.addWidget(self.thumb_label)
        self.desc_text_edit = QtGui.QTextEdit(self)
        self.desc_text_edit.setMinimumSize(QtCore.QSize(0, 130))
        self.desc_text_edit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.desc_text_edit.setStyleSheet(
                                          "QTextEdit{"+\
                                          "border-style: solid;"+\
                                          "border-width : 0.5px;"+\
                                          "border-color: "+ self.style_component['border_color'] +";"+\
                                          "border-radius: 2px;"+\
                                          "color :"+ self.style_component['font_color'] +";"+\
                                          "background:" +self.style_component['background_color']+";"+\
                                          "border-radius: 3px;"+\
                                          "font:  11px;"+\
                                          "padding-left: 10px;"+\
                                          "}")

        self.thumb_desc_hboxlayout.addWidget(self.desc_text_edit)
        self.main_vboxlayout.addLayout(self.thumb_desc_hboxlayout)
        self.verticalLayout_2.addLayout(self.main_vboxlayout)

    def add_pub_file_item(self, file_path):
        tex_exts = [".png", ".jpg", ".jpeg", ".cin", ".dpx", ".tiff", ".tif", ".mov", ".psd", ".tga", ".ari", ".gif", ".iff", '.tx']
        ext = os.path.splitext(file_path)[-1]
        item_type = 'exporter'
        list_item=custom_list_item.CustomListItem(self.pub_files_tree_widget,item_type, file_path, 0)

        if ext in tex_exts:
            self.tex_items.append((list_item, file_path))
        return list_item


    def get_thumb(self):
        return self.thumb_label.get_thumb_path()

    def get_desc(self):
        return self.desc_text_edit.toPlainText()
    
    def set_desc(self, input_desc :str):
        self.desc_text_edit.setText(input_desc)
        

    def clear_all_items(self):
        self.pub_files_tree_widget.clear()

    def start_make_tex_thumb(self):
        for info in self.tex_items:
            item = info[0]
            file_path = info[1]
            # thumb_maker = TexThumbMaker(self, item, file_path)
            # thumb_maker.start()

    def set_info_label(self, msg, negative = False):
        if negative == True:
            self.pub_info_label.setStyleSheet(
                                    "QLabel{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "color: "+self.style_component['warn_color']+";"+\
                                    "border: none;"+\
                                    "font : bold 13px;"+\
                                    "padding-left: 2px;"+\
                                    "}")
        self.pub_info_label.setText(msg)

    def get_prepub_status(self):
        return self.prepub_view_check_cb.isChecked()

class TexThumbMaker(QtCore.QThread):

    file_path = None
    complete = QtCore.Signal(object)
    item = None

    def __init__(self, parent, item, file_path):
        QtCore.QThread.__init__(self, parent)
        self.file_path = file_path
        self.item = item

    def run(self):
        if '<UDIM>' in self.file_path:
            self.file_path = self.file_path.replace('<UDIM>', '*')
        elif '<udim>' in self.file_path:
            self.file_path = self.file_path.replace('<udim>', '*')

        tex_files = glob.glob(self.file_path)
        if len(tex_files) == 0:
            print('can not find tex file')
            print(self.file_path)
            return
        tex_file = tex_files[0]

        pix_map = QtGuiOrig.QPixmap(tex_file)
        pix_map = pix_map.scaled(32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.item.set_thumb(pix_map)
        #self.complete.emit(pix_map)
