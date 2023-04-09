# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\YC_milki_main_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


# from PyQt5 import QtCore, QtGui, QtGui
from importlib import reload
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from source.milki.view import YC_thumb_lb
from source.milki.view import YC_custom_widgets
reload(YC_thumb_lb)
reload(YC_custom_widgets)
from source.YC_core_module import cam_img



class Ui_YC_main_view(QtCore.QObject):
    

    @QtCore.Property(int)
    def main_geometry(self) -> int:
        return self._parent.width()
    
    @main_geometry.setter
    def main_geometry(self, _input_width) -> None:
        self._parent.setFixedWidth(_input_width)

    @QtCore.Property(int)
    def child_geometry(self) -> int:
        return self.YC_check_log_container_wg.width()
    
    @child_geometry.setter
    def child_geometry(self, _input_width) -> None:
        self.YC_check_log_container_wg.setFixedWidth(_input_width)

    def setupUi(self, YC_main_view :QtGui.QMainWindow):
        self.lineedit_list = []
        self.cur_check_item = ""
        
        self.child_anim_start_value = 0
        self.child_anim_end_value   = 300

        self.main_anim_start_value  = 720
        self.main_anim_end_value    = self.main_anim_start_value + self.child_anim_end_value

        self._parent = YC_main_view
        YC_main_view.setObjectName("YC_main_view")
        YC_main_view.setFixedSize(self.main_anim_start_value, 690)
        YC_main_view.setWindowOpacity(1.0)
        # YC_main_view.setStyleSheet("{"+\
        #                                     "border: 3px solid;"+\
        #                                     "border-radius: 5px;"+\
        #                                     "}")
        YC_main_view.setWindowFlags(YC_main_view.windowFlags() | QtCore.Qt.FramelessWindowHint)
        
        self.centralwidget = QtGui.QWidget(YC_main_view)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.YC_asset_info_container_wg = QtGui.QWidget(self.centralwidget)
        self.YC_asset_info_container_wg.setObjectName("YC_asset_info_container_wg")
        self.YC_asset_info_container_wg.setFixedWidth(250)
        self.YC_asset_info_container_wg.setStyleSheet("QWidget{"+\
                                                "background:#0e356e;"+\
                                                "}")
        
        self.verticalLayout = QtGui.QVBoxLayout(self.YC_asset_info_container_wg)
        self.verticalLayout.setObjectName("verticalLayout")

        top_spacer = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(top_spacer)
        # self.YC_thumb_info_lb = QtGui.QLabel(self.YC_asset_info_container_wg)
        # self.YC_thumb_info_lb.setObjectName("YC_thumb_info_lb")
        self.YC_thumb_info_lb = YC_thumb_lb.Thumbnail(YC_main_view)
        # self.YC_thumb_info_lb.setFixedSize(155,100)
        self.YC_thumb_info_lb.setMaximumWidth(230)
        # sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        # self.YC_thumb_info_lb.setSizePolicy(sizePolicy)
        self.YC_thumb_info_lb.set_thumb_from_path(cam_img)


        self.verticalLayout.addWidget(self.YC_thumb_info_lb)
        self.YC_name_info_hl = QtGui.QHBoxLayout()
        self.YC_name_info_hl.setObjectName("YC_name_info_hl")
        self.YC_name_info_title_lb = QtGui.QLabel(self.YC_asset_info_container_wg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YC_name_info_title_lb.sizePolicy().hasHeightForWidth())
        self.YC_name_info_title_lb.setSizePolicy(sizePolicy)
        self.YC_name_info_title_lb.setMinimumSize(QtCore.QSize(100, 0))
        self.YC_name_info_title_lb.setMaximumSize(QtCore.QSize(100, 16777215))
        self.YC_name_info_title_lb.setObjectName("YC_name_info_title_lb")
        self.YC_name_info_hl.addWidget(self.YC_name_info_title_lb)
        self.YC_name_info_contents_le = QtGui.QLineEdit(self.YC_asset_info_container_wg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YC_name_info_contents_le.sizePolicy().hasHeightForWidth())
        self.YC_name_info_contents_le.setSizePolicy(sizePolicy)
        self.YC_name_info_contents_le.setMinimumSize(QtCore.QSize(0, 0))
        self.YC_name_info_contents_le.setObjectName("YC_name_info_contents_le")
        self.YC_name_info_contents_le.setReadOnly(True)
        self.lineedit_list.append(self.YC_name_info_contents_le)
        # self.YC_name_info_contents_le.setStyleSheet("QLineEdit{"+\
        #                                         "border: none;"+\
        #                                         "}")
        self.YC_name_info_hl.addWidget(self.YC_name_info_contents_le)
        self.YC_name_info_hl.setStretch(0, 2)
        self.YC_name_info_hl.setStretch(1, 3)
        self.verticalLayout.addLayout(self.YC_name_info_hl)
        self.YC_variant_info_hl = QtGui.QHBoxLayout()
        self.YC_variant_info_hl.setObjectName("YC_variant_info_hl")
        self.YC_variant_info_title_lb = QtGui.QLabel(self.YC_asset_info_container_wg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YC_variant_info_title_lb.sizePolicy().hasHeightForWidth())
        self.YC_variant_info_title_lb.setSizePolicy(sizePolicy)
        self.YC_variant_info_title_lb.setMinimumSize(QtCore.QSize(100, 0))
        self.YC_variant_info_title_lb.setMaximumSize(QtCore.QSize(100, 16777215))
        self.YC_variant_info_title_lb.setObjectName("YC_variant_info_title_lb")
        self.YC_variant_info_hl.addWidget(self.YC_variant_info_title_lb)
        self.YC_variant_info_contents_le = QtGui.QLineEdit(self.YC_asset_info_container_wg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YC_variant_info_contents_le.sizePolicy().hasHeightForWidth())
        self.YC_variant_info_contents_le.setSizePolicy(sizePolicy)
        self.YC_variant_info_contents_le.setObjectName("YC_variant_info_contents_le")
        self.lineedit_list.append(self.YC_variant_info_contents_le)
        self.YC_variant_info_hl.addWidget(self.YC_variant_info_contents_le)
        self.YC_variant_info_hl.setStretch(0, 2)
        self.YC_variant_info_hl.setStretch(1, 3)
        self.verticalLayout.addLayout(self.YC_variant_info_hl)
        self.YC_vernum_info_hl = QtGui.QHBoxLayout()
        self.YC_vernum_info_hl.setObjectName("YC_vernum_info_hl")
        self.YC_vernum_info_title_lb = QtGui.QLabel(self.YC_asset_info_container_wg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.YC_vernum_info_title_lb.sizePolicy().hasHeightForWidth())
        self.YC_vernum_info_title_lb.setSizePolicy(sizePolicy)
        self.YC_vernum_info_title_lb.setMinimumSize(QtCore.QSize(100, 0))
        self.YC_vernum_info_title_lb.setMaximumSize(QtCore.QSize(100, 16777215))
        self.YC_vernum_info_title_lb.setObjectName("YC_vernum_info_title_lb")
        self.YC_vernum_info_hl.addWidget(self.YC_vernum_info_title_lb)
        self.YC_vernum_info_contents_le = QtGui.QLineEdit(self.YC_asset_info_container_wg)
        self.YC_vernum_info_contents_le.setObjectName("YC_vernum_info_contents_le")
        self.lineedit_list.append(self.YC_vernum_info_contents_le)
        self.YC_vernum_info_hl.addWidget(self.YC_vernum_info_contents_le)
        self.YC_vernum_info_hl.setStretch(0, 2)
        self.YC_vernum_info_hl.setStretch(1, 3)
        self.verticalLayout.addLayout(self.YC_vernum_info_hl)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.YC_pub_btn_list_hl = QtGui.QHBoxLayout()
        self.YC_pub_btn_list_hl.setObjectName("YC_pub_btn_list_hl")
        # spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # self.YC_pub_btn_list_hl.addItem(spacerItem3)
        self.YC_publish_btn = QtGui.QPushButton(self.YC_asset_info_container_wg)
        self.YC_publish_btn.setObjectName("YC_publish_btn")
        self.YC_pub_btn_list_hl.addWidget(self.YC_publish_btn)
        self.YC_pub_cancel_btn = QtGui.QPushButton(self.YC_asset_info_container_wg)
        self.YC_pub_cancel_btn.setObjectName("YC_pub_cancel_btn")
        self.YC_pub_btn_list_hl.addWidget(self.YC_pub_cancel_btn)
        self.verticalLayout.addLayout(self.YC_pub_btn_list_hl)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout.setStretch(4, 2)
        self.verticalLayout.setStretch(5, 10)
        self.verticalLayout.setStretch(6, 1)
        self.horizontalLayout.addWidget(self.YC_asset_info_container_wg)
        self.YC_pub_container_hl = QtGui.QHBoxLayout()
        self.YC_pub_container_hl.setSpacing(0)
        self.YC_pub_container_hl.setObjectName("YC_pub_container_hl")
        self.YC_pub_body_container_wg = QtGui.QWidget(self.centralwidget)
        self.YC_pub_body_container_wg.setObjectName("YC_pub_body_container_wg")
        # self.YC_pub_body_container_wg.setStyleSheet("QWidget{"+\
        #                                         "margin-left: 10px;"+\
        #                                         "margin-right: 10px;"+\
        #                                         "}")
        # self.YC_pub_body_container_wg.setFixedWidth(300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.YC_pub_body_container_wg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.YC_pub_check_title_lb = QtGui.QLabel(self.YC_pub_body_container_wg)
        self.YC_pub_check_title_lb.setObjectName("YC_pub_check_title_lb")
        self.verticalLayout_2.addWidget(self.YC_pub_check_title_lb)

        # self.YC_pub_check_contents_lw = QtGui.QListWidget(self.YC_pub_body_container_wg)
        self.YC_pub_check_contents_lw = YC_custom_widgets.custom_listwidget(self.YC_pub_body_container_wg)
        self.YC_pub_check_contents_lw.setViewMode(QtGui.QListView.IconMode)
        
        self.YC_pub_check_contents_lw.setObjectName("YC_pub_check_contents_lw")
        self.YC_pub_check_contents_lw.setStyleSheet("QListWidget{"+\
                                                "background:#31363b;"+\
                                                "}")
        self.verticalLayout_2.addWidget(self.YC_pub_check_contents_lw)



        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.YC_pub_path_info_hl = QtGui.QHBoxLayout()
        self.YC_pub_path_info_hl.setObjectName("YC_pub_path_info_hl")
        self.YC_pub_path_info_title_lb = QtGui.QLabel(self.YC_pub_body_container_wg)
        self.YC_pub_path_info_title_lb.setObjectName("YC_pub_path_info_title_lb")
        self.YC_pub_path_info_hl.addWidget(self.YC_pub_path_info_title_lb)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.YC_pub_path_info_hl.addItem(spacerItem2)
        self.YC_pub_path_info_set_btn = QtGui.QPushButton(self.YC_pub_body_container_wg)
        self.YC_pub_path_info_set_btn.setObjectName("YC_pub_path_info_set_btn")
        self.YC_pub_path_info_set_btn.setFixedHeight(25)
        self.YC_pub_path_info_hl.addWidget(self.YC_pub_path_info_set_btn)
        self.verticalLayout_2.addLayout(self.YC_pub_path_info_hl)
        # self.YC_pub_path_contents_le = QtGui.QLineEdit(self.YC_pub_body_container_wg) 
        self.YC_pub_path_contents_le = YC_custom_widgets.QLineEditWithPopup(self.YC_pub_body_container_wg)
        self.YC_pub_path_contents_le.setObjectName("YC_pub_path_contents_le")
        self.YC_pub_path_contents_le.setReadOnly(True)
        self.YC_pub_path_contents_le.setToolTip("Click : open directory")
        self.YC_pub_path_contents_le.setStyleSheet(
                                                "QLineEdit:hover{"+\
                                                "color: #D9D9D9;"+\
                                                "}")
        self.verticalLayout_2.addWidget(self.YC_pub_path_contents_le)
        self.YC_pub_datum_title_lb = QtGui.QLabel(self.YC_pub_body_container_wg)
        self.YC_pub_datum_title_lb.setObjectName("YC_pub_datum_title_lb")
        self.verticalLayout_2.addWidget(self.YC_pub_datum_title_lb)
        # self.YC_pub_datum_contents_lw = QtGui.QListWidget(self.YC_pub_body_container_wg)
        self.YC_pub_datum_contents_lw = YC_custom_widgets.custom_pubitems_listwidget(self.YC_pub_body_container_wg)
        self.YC_pub_datum_contents_lw.setObjectName("YC_pub_datum_contents_lw")

        self.verticalLayout_2.addWidget(self.YC_pub_datum_contents_lw)
        self.YC_pub_desc_title_lb = QtGui.QLabel(self.YC_pub_body_container_wg)
        self.YC_pub_desc_title_lb.setObjectName("YC_pub_desc_title_lb")
        self.verticalLayout_2.addWidget(self.YC_pub_desc_title_lb)
        self.YC_pub_desc_contents_te = QtGui.QTextEdit(self.YC_pub_body_container_wg)
        self.YC_pub_desc_contents_te.setObjectName("YC_pub_desc_contents_te")
        self.YC_pub_desc_contents_te.setPlaceholderText("Input publish description")
        self.verticalLayout_2.addWidget(self.YC_pub_desc_contents_te)
        
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 3)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 2)
        self.verticalLayout_2.setStretch(5, 1)
        self.verticalLayout_2.setStretch(6, 6)
        self.verticalLayout_2.setStretch(7, 1)
        self.verticalLayout_2.setStretch(8, 3)
        # self.verticalLayout_2.setStretch(9, 1)
        self.YC_pub_container_hl.addWidget(self.YC_pub_body_container_wg)
        self.YC_check_log_container_wg = QtGui.QWidget(self.centralwidget)
        self.YC_check_log_container_wg.setObjectName("YC_check_log_container_wg")
        self.YC_check_log_container_wg.setFixedWidth(self.child_anim_start_value)
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.YC_check_log_container_wg)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.YC_check_log_title_lb = QtGui.QLabel(self.YC_check_log_container_wg)
        self.YC_check_log_title_lb.setObjectName("YC_check_log_title_lb")
        self.verticalLayout_3.addWidget(self.YC_check_log_title_lb)
        self.YC_check_log_contents_lw = QtGui.QListWidget(self.YC_check_log_container_wg)
        self.YC_check_log_contents_lw.setObjectName("YC_check_log_contents_lw")
        self.verticalLayout_3.addWidget(self.YC_check_log_contents_lw)
        self.YC_pub_container_hl.addWidget(self.YC_check_log_container_wg)
        self.YC_pub_container_hl.setStretch(0, 3)
        self.YC_pub_container_hl.setStretch(1, 2)
        self.horizontalLayout.addLayout(self.YC_pub_container_hl)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        YC_main_view.setCentralWidget(self.centralwidget)

        self.lineedit_set_stylesheet()
        self.retranslateUi(YC_main_view)
        QtCore.QMetaObject.connectSlotsByName(YC_main_view)

    def retranslateUi(self, YC_main_view):
        _translate = QtCore.QCoreApplication.translate
        YC_main_view.setWindowTitle(_translate("YC_main_view", "Milki"))
        # self.YC_thumb_info_lb.setText(_translate("YC_main_view", "Thumbnail"))
        self.YC_name_info_title_lb.setText(_translate("YC_main_view", "Asset Name"))
        self.YC_variant_info_title_lb.setText(_translate("YC_main_view", "Variant Name"))
        self.YC_vernum_info_title_lb.setText(_translate("YC_main_view", "Version Number"))
        self.YC_pub_check_title_lb.setText(_translate("YC_main_view", "Check List"))
        self.YC_pub_path_info_title_lb.setText(_translate("YC_main_view", "Export Info - path"))
        self.YC_pub_path_info_set_btn.setText(_translate("YC_main_view", "select path"))
        self.YC_pub_datum_title_lb.setText(_translate("YC_main_view", "Export Info - data list"))
        self.YC_pub_desc_title_lb.setText(_translate("YC_main_view", "Export Info - description"))
        self.YC_publish_btn.setText(_translate("YC_main_view", "Publish"))
        self.YC_pub_cancel_btn.setText(_translate("YC_main_view", "Close"))
        self.YC_check_log_title_lb.setText(_translate("YC_main_view", "Check log"))

    def set_current_check_item(self, cur_item :str) -> None:
        self.cur_check_item = cur_item

    def current_check_item(self) -> str:
        return self.cur_check_item

    def init_anim(self) -> None:
        self._ANIM_STATUS_ = False

        self.main_geo_anim = QtCore.QPropertyAnimation(self, b"main_geometry")
        self.main_geo_anim.setStartValue(self.main_anim_start_value)
        self.main_geo_anim.setEndValue(self.main_anim_end_value)
        self.main_geo_anim.setDuration(300)

        self.child_geo_anim = QtCore.QPropertyAnimation(self, b"child_geometry")
        self.child_geo_anim.setStartValue(self.child_anim_start_value)
        self.child_geo_anim.setEndValue(self.child_anim_end_value)
        self.child_geo_anim.setDuration(300)

        self.total_anim = QtCore.QParallelAnimationGroup()
        self.total_anim.addAnimation(self.main_geo_anim)
        self.total_anim.addAnimation(self.child_geo_anim)
        
    def start_anim(self, input_check_title :str) -> None:
        if self.current_check_item() == "":
            self.set_current_check_item(input_check_title)

        self.total_anim.stop()
        if self._ANIM_STATUS_ == False:
            self.set_current_check_item(input_check_title)
            self._ANIM_STATUS_ = True
            self.total_anim.setDirection(QtCore.QAbstractAnimation.Forward)
            self.total_anim.start()
        elif self._ANIM_STATUS_ == True and (self.current_check_item() != input_check_title):
            self.set_current_check_item(input_check_title)
            print(111111)
        elif self._ANIM_STATUS_ == True:
            self._ANIM_STATUS_ = False
            self.total_anim.setDirection(QtCore.QAbstractAnimation.Backward)
            self.total_anim.start()
            
    def set_log_item_info(self, check_title :str, check_log :list) -> None:
        self.YC_pub_check_contents_lw.add_item(check_title, check_log)
        
    def set_error_view(self, check_title :str, check_log :list) -> None:
        self.YC_check_log_contents_lw.clear()
        error_prefix = ""
        if check_title == "Name":
            error_prefix = "Name Convention Error : "
            for _log in check_log:
                _log_item = QtGui.QListWidgetItem(error_prefix+_log)
                _log_item.setWhatsThis(_log)
                self.YC_check_log_contents_lw.addItem(_log_item)

    def set_assetname(self, input_name :str) -> None:
        self.YC_name_info_contents_le.setText(input_name)

    def set_variantname(self, input_name :str="") -> None:
        if input_name == "":
            self.YC_variant_info_contents_le.setText("default")
        else:
            self.YC_variant_info_contents_le.setText(input_name)

    def set_vernum(self, input_name :str="") -> None:
        if input_name == "":
            self.YC_vernum_info_contents_le.setText("v001")
        else:
            self.YC_vernum_info_contents_le.setText(input_name)

    def get_assetname(self) -> str:
        return self.YC_name_info_contents_le.text()
    
    def get_variantname(self) -> str:
        return self.YC_variant_info_contents_le.text()
    
    def get_vernum(self) -> str:
        return self.YC_vernum_info_contents_le.text()

    def get_pub_dirname(self) -> str:
        return self.YC_pub_path_contents_le.text().replace('\\', '/')

    def set_pub_path(self, input_dir :str) -> None:
        self.YC_pub_path_contents_le.setText(input_dir)


    def set_pub_item_view(self, pub_items :list) -> None:
        self.YC_pub_datum_contents_lw.clear()

        for _pub_path in pub_items:
            self.YC_pub_datum_contents_lw.add_item(_pub_path)


    def lineedit_set_stylesheet(self) -> None:
        for _lineedit in self.lineedit_list:
            _lineedit.setStyleSheet(
                                    "QLineEdit{"+\
                                            "font: 14px  ;"+\
                                            "}"
                                    )
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    YC_main_view = QtGui.QMainWindow()
    ui = Ui_YC_main_view()
    ui.setupUi(YC_main_view)
    YC_main_view.show()
    sys.exit(app.exec_())
