# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\taiyoung.song\Desktop\ui_custom_listwidget_item.ui'
#
# Created: Tue Jun  4 12:41:08 2019
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui
import sys
import os

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

class QCustomQWidget(QtGui.QWidget):
    def __init__ (self, item_info, parent =None):
        super(QCustomQWidget, self).__init__(parent)
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
        self.setupUi(self)
        self.set_data(item_info)
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(424, 22)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textQVBoxLayout.setObjectName(_fromUtf8("textQVBoxLayout"))
        self.file_format_icon_label = QtGui.QLabel(Form)
        self.file_format_icon_label.setText(_fromUtf8(""))
        self.file_format_icon_label.setObjectName(_fromUtf8("file_format_icon_label"))
        self.file_format_icon_label.setStyleSheet("QLabel{"+\
                                         "background:" +self.style_component['background_color']+";"+\
                                         "color: "+ self.style_component['font_color'] +";"+\
                                         "font: bold 11px;"+\
                                         "padding-left: 5px;"+\
                                         "}")
        self.horizontalLayout.addWidget(self.file_format_icon_label)
        self.file_name_label = QtGui.QLabel(Form)
        self.file_name_label.setText(_fromUtf8(""))
        self.file_name_label.setObjectName(_fromUtf8("file_name_label"))
        self.file_name_label.setStyleSheet("QLabel{"+\
                                         "background:" +self.style_component['background_color']+";"+\
                                         "color: "+ self.style_component['font_color'] +";"+\
                                         "font: bold 11px;"+\
                                         "padding: 0px 0px 0px 5px;"+\
                                         "}")
        self.textQVBoxLayout.addWidget(self.file_name_label)
        self.file_format_label = QtGui.QLabel(Form)
        self.file_format_label.setText(_fromUtf8(""))
        self.file_format_label.setObjectName(_fromUtf8("file_name_label"))
        self.file_format_label.setStyleSheet("QLabel{"+\
                                         "background:" +self.style_component['background_color']+";"+\
                                         "color: "+ self.style_component['font_color'] +";"+\
                                         "font: 10px;"+\
                                         "padding: 0px 0px 0px 6px;"+\
                                         "}")#top, right, bottom, left
        self.textQVBoxLayout.addWidget(self.file_format_label)
        self.horizontalLayout.addLayout(self.textQVBoxLayout)
        self.ischecked_icon_label = QtGui.QLabel(Form)
        self.ischecked_icon_label.setText(_fromUtf8(""))
        self.ischecked_icon_label.setObjectName(_fromUtf8("ischecked_icon_label"))
        self.ischecked_icon_label.setStyleSheet("QLabel{"+\
                                         "padding-right: 35px;"+\
                                         "}")
        self.horizontalLayout.addWidget(self.ischecked_icon_label)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 9)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

    def set_data(self, file_path):
        print("file_path : " + str(file_path))
        file_name = os.path.basename(file_path)
        self.file_name_label.setText(file_name)
        ext = os.path.splitext(file_name)[-1]
        ext = ext.lower()
        info_dict = {}
        if sys.platform.count("win"):
            prePath = "Z:/backstage/maya/milki/icons/"
        else:
            prePath = "/usersetup/linux/module/ui_icons_md/milki/"
        info_dict['.abc'] = {'format': 'alembic cache', 'icon': prePath + 'alembic_black_icon_6_34.png'}
        info_dict['.mov'] = {'format': 'quick time video', 'icon': prePath + 'mov_icon_6_30.png'}
        info_dict['.ma'] = {'format': 'Maya ASCII', 'icon': prePath + 'maya_icon_new_2.png'}
        info_dict['.mb'] = {'format': 'Maya Binary', 'icon': prePath + 'maya_icon_new_2.png'}
        info_dict['.hichy'] = {'format': 'Mesh hirarchy data', 'icon': prePath + 'hichy_icon_2.png'}
        info_dict['.mtlx'] = {'format': 'Material X', 'icon': prePath + 'MaterialX_2_28.png'}
        info_dict['.ass'] = {'format': 'ASS', 'icon': prePath + 'ass_icon_resize.png'}
        info_dict['.usd'] = {'format': 'USD', 'icon': prePath + 'USD_logo_resized.png'}
        info_dict['.grm'] = {'format': 'GRM', 'icon': prePath + 'pgYeti_icon.png'}
        info_dict['.fur'] = {'format': 'GRM', 'icon': prePath + 'pgYeti_icon.png'}
        tex_exts = [".png", ".jpg", ".jpeg", ".cin", ".dpx", ".tiff", ".tif", ".mov", ".psd", ".tga", ".ari", ".gif", ".iff", '.tx']

        if ext in info_dict:
            info = info_dict[ext]
            self.file_format_label.setText(info['format'])
            self.file_format_icon_label.setPixmap(info['icon'])
            return

        if ext == ".exr":
            exr_icon = prePath + 'exr_icon.png'
            self.file_format_label.setText('Texture')
            self.file_format_icon_label.setPixmap(exr_icon)
            return
        if ext in tex_exts:
            tex_icon = prePath + 'tex_img_2_30.png'
            self.file_format_label.setText('Texture')
            self.file_format_icon_label.setPixmap(tex_icon)
            return

    def set_thumb(self, thumb):
        print(thumb)


class TexThumbMaker(QtCore.QThread):
    file_path = None
    complete = QtCore.Signal(object)

    def __init__(self, file_path):
        QtCore.QThread.__init__(self)
        self.file_path = file_path
        print(self.file_path)

    def run(self):
        if '<UDIM>' in self.file_path:
            self.file_path = self.file_path.replace('<UDIM>', '*')
        elif '<udim>' in self.file_path:
            self.file_path = self.file_path.replace('<udim>', '*')
        print(self.file_path)
