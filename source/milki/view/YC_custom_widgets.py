import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from functools import partial
from subprocess import Popen
import os
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
from source.YC_core_module import (get_open_dir_cmd, is_windows, __HGWEAVER_RESOURCE_PATH__)



class QLineEditWithPopup(QtGui.QLineEdit):
    def __init__(self, parent) -> None:
        super(QLineEditWithPopup, self).__init__(parent)

    def contextMenuEvent(self, arg__1: QtGuiOrig.QContextMenuEvent) -> None:
        return super().contextMenuEvent(arg__1)

    def mousePressEvent(self, arg__1: QtGuiOrig.QMouseEvent) -> None:
        open_cmd    = get_open_dir_cmd()
        open_target = self.get_path()
        try:
            print("{0} {1}".format(open_cmd, open_target))
            Popen([open_cmd, open_target])
        except Exception as e:
            print(str(e))
        return super().mousePressEvent(arg__1)

    def get_path(self) -> str:
        if is_windows() == True:
            return self.text().replace('/', '\\')
        else:
            return self.text()

class custom_pubitems_widget(QtGui.QWidget):
    def __init__ (self, parent =None):
        super(custom_pubitems_widget, self).__init__(parent)
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
        self.setupUi(self)
        
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
        # self.file_format_icon_label.setStyleSheet("QLabel{"+\
        #                                  "padding-left: 5px;"+\
        #                                  "}")
        self.horizontalLayout.addWidget(self.file_format_icon_label)
        self.file_name_label = QtGui.QLabel(Form)
        self.file_name_label.setText(_fromUtf8(""))
        self.file_name_label.setObjectName(_fromUtf8("file_name_label"))
        # self.file_name_label.setStyleSheet("QLabel{"+\
        #                                  "padding: 0px 0px 0px 5px;"+\
        #                                  "}")
        self.textQVBoxLayout.addWidget(self.file_name_label)
        self.file_format_label = QtGui.QLabel(Form)
        self.file_format_label.setText(_fromUtf8(""))
        self.file_format_label.setObjectName(_fromUtf8("file_name_label"))
        # self.file_format_label.setStyleSheet("QLabel{"+\
        #                                  "padding: 0px 0px 0px 6px;"+\
        #                                  "}")#top, right, bottom, left
        self.textQVBoxLayout.addWidget(self.file_format_label)
        self.horizontalLayout.addLayout(self.textQVBoxLayout)
        self.ischecked_icon_label = QtGui.QLabel(Form)
        self.ischecked_icon_label.setText(_fromUtf8(""))
        self.ischecked_icon_label.setObjectName(_fromUtf8("ischecked_icon_label"))
        # self.ischecked_icon_label.setStyleSheet("QLabel{"+\
        #                                  "padding-right: 35px;"+\
        #                                  "}")
        self.horizontalLayout.addWidget(self.ischecked_icon_label)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 9)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        
        QtCore.QMetaObject.connectSlotsByName(Form)

    # def retranslateUi(self, Form):
    #     Form.setWindowTitle(_translate("Form", "Form", None))

    def set_data(self, file_path):
        print("file_path : " + str(file_path))
        file_name = os.path.basename(file_path)
        self.file_name_label.setText(file_name)
        ext = os.path.splitext(file_name)[-1]
        ext = ext.lower()
        info_dict = {}
        
        pre_path = __HGWEAVER_RESOURCE_PATH__ + "/" + "icons" + "/"
        info_dict['.abc'] = {'format': 'alembic cache', 'icon': pre_path + 'alembic_black_icon_6_34.png'}
        info_dict['.mov'] = {'format': 'quick time video', 'icon': pre_path + 'mov_icon_6_30.png'}
        info_dict['.ma'] = {'format': 'Maya ASCII', 'icon': pre_path + 'maya_icon_new_2.png'}
        info_dict['.mb'] = {'format': 'Maya Binary', 'icon': pre_path + 'maya_icon_new_2.png'}
        info_dict['.hichy'] = {'format': 'Mesh hirarchy data', 'icon': pre_path + 'hichy_icon_2.png'}
        info_dict['.mtlx'] = {'format': 'Material X', 'icon': pre_path + 'MaterialX_2_28.png'}
        info_dict['.ass'] = {'format': 'ASS', 'icon': pre_path + 'ass_icon_resize.png'}
        info_dict['.grm'] = {'format': 'GRM', 'icon': pre_path + 'pgYeti_icon.png'}
        info_dict['.fur'] = {'format': 'GRM', 'icon': pre_path + 'pgYeti_icon.png'}
        tex_exts = [".png", ".jpg", ".jpeg", ".cin", ".dpx", ".tiff", ".tif", ".mov", ".psd", ".tga", ".ari", ".gif", ".iff", '.tx']

        if ext in info_dict:
            info = info_dict[ext]
            self.file_format_label.setText(info['format'])
            self.file_format_icon_label.setPixmap(info['icon'])
            return

        if ext == ".exr":
            exr_icon = pre_path + 'exr_icon.png'
            self.file_format_label.setText('Texture')
            self.file_format_icon_label.setPixmap(exr_icon)
            return
        if ext in tex_exts:
            tex_icon = pre_path + 'tex_img_2_30.png'
            self.file_format_label.setText('Texture')
            self.file_format_icon_label.setPixmap(tex_icon)
            return

    def set_thumb(self, thumb):
        print(thumb)

class custom_pubitems_listwidget(QtGui.QListWidget):
    def __init__(self, parent, ):

        super(custom_pubitems_listwidget, self).__init__(parent)

        
        
        


    def get_ui(self):
        return self._item_ui

    def get_label_text(self, item_type):
        return self.exporter_item_ui.file_name_label.text()

    def set_label_text(self, file_name):
        self.exporter_item_ui.file_name_label.setText(file_name)

    def set_thumb(self, thumb):
        self.exporter_item_ui.file_format_icon_label.setPixmap(thumb)

    def add_item(self, pub_full_path):

        _custom_item = custom_pubitems_widget()
        _custom_item.set_data(pub_full_path)
        

        _listwidet_item = QtGui.QListWidgetItem(self)
        _listwidet_item.setSizeHint(_custom_item.sizeHint())
        _listwidet_item.setFlags(_listwidet_item.flags() )
        self.addItem(_listwidet_item)
        self.setItemWidget(_listwidet_item, _custom_item)

        

    # def add_item(self, item_type, item_info, idx) -> None:
    #     self.exporter_item_ui = custom_pubitems_widget(item_info)
    #     self.setFlags(QtCore.Qt.NoItemFlags)
    #     self.listWidget().setItemWidget(self, self.exporter_item_ui)
    #     self.setSizeHint(self.exporter_item_ui.sizeHint())


class Item_Ui_Form(QtGui.QWidget):
    
    def __init__(self, _parent=None):
        super(Item_Ui_Form, self).__init__(_parent)
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_disable_color': '#797979',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}

        self.setupUi(self)

        self.check_status = False

    def setupUi(self, Form):
        # Form.setObjectName(_fromUtf8("Form"))
        # Form.resize(300, 300)
        self.setFixedSize(100, 100)
        # self.setAcceptDrops(False)
        
        self.title_lb = QtGui.QLabel(self)
        self.title_lb.setObjectName(_fromUtf8("img_lb"))
        self.title_lb.setText("aa")
        self.title_lb.move(5, 70)

        self.count_lb = QtGui.QLabel(self)
        self.count_lb.setObjectName(_fromUtf8("img_lb"))
        self.count_lb.setText("aa")
        self.count_lb.move(80, 70)
        
    def paintEvent(self, paint_event):
        
        painter = QtGuiOrig.QPainter(self)
        painter.setRenderHint(QtGuiOrig.QPainter.Antialiasing)

        if self.check_status == True:
            brush = QtGuiOrig.QBrush(QtGuiOrig.QColor(255, 255, 255))
        else:
            brush = QtGuiOrig.QBrush(QtGuiOrig.QColor(186, 39, 49))
        painter.setBrush(brush)

        # Set the pen color to transparent
        pen = QtGuiOrig.QPen(QtGuiOrig.QColor(0, 0, 0, 0))
        painter.setPen(pen)

        # Draw the circle
        painter.drawEllipse(10, 10, 13, 13)

    # def mousePressEvent(self, event) -> None:
    #     print(1111111111)
    #     return super().mousePressEvent(event)
    
    # def mouseReleaseEvent(self, event) -> None:
    #     print(2222222222)
    #     return super().mouseReleaseEvent(event)

    def set_info(self, check_title :str, error_count :int) -> None:
        self.title_lb.setText(check_title)
        self.count_lb.setText(str(error_count))
        if error_count == 0:
            self.check_status = True
        else:
            self.check_status = False
        
        self.update()


    # def flags(self):
    #     return QtCore.Qt.ItemIsSelectable

    
class custom_listwidget(QtGui.QListWidget):
    _CHECK_CONVETION_SIGNAL_ = QtCore.Signal(object)
    def __init__(self, _parent):
        super(custom_listwidget, self).__init__(_parent)
        self.parent = _parent
        self._drop_file_list    = []
        self.real_tar_list      = []
        self.setIconSize(QtCore.QSize(100, 100))
        self.setFixedHeight(130)

        


    def reset_listwidget(self):
        self.clear()
        self._drop_file_list = []




    def add_item(self, check_title :str, error_contents :list):

        error_count = len(error_contents)
        _custom_item = Item_Ui_Form()
        _custom_item.set_info(check_title, error_count)
        
    
        _listwidet_item = QtGui.QListWidgetItem(self)
        _listwidet_item.setFlags(_listwidet_item.flags() & ~QtCore.Qt.ItemIsDragEnabled) 
        _listwidet_item.setIcon(QtGuiOrig.QIcon(_custom_item.grab()))
        _listwidet_item.setData(QtCore.Qt.UserRole, [check_title, error_count, error_contents])
        self.addItem(_listwidet_item)
        


    def contextMenuEvent(self, event) -> None:
        r_menu = QtGui.QMenu(self)
        r_menu_action = QtGui.QAction("Check Convention", self)
        r_menu_action.triggered.connect(partial(self._CHECK_CONVETION_SIGNAL_.emit, self.itemAt(self.mapFromGlobal(QtGuiOrig.QCursor.pos()))))
        r_menu.addAction(r_menu_action)

        r_menu.popup(QtGuiOrig.QCursor.pos())
        return super().contextMenuEvent(event)


    def delete_custom_item(self):
        item, pop_widget = self.get_item_from_mouse()
        idx  = self.indexFromItem(item).row()
        self.takeItem(idx)

        _removed_filename = pop_widget.get_yeti_name()
        tar_idx = None
        for _idx, _name in enumerate(self._drop_file_list): 
            
            if _name == _removed_filename:
                tar_idx = _idx
                break
        self.real_tar_list.pop(tar_idx)
        self._drop_file_list.remove(_removed_filename)
        

