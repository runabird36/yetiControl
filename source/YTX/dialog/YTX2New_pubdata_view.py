
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from os import path, getcwd
from functools import partial
from pprint import pprint
import sys, re, yaml
from qt_material import apply_stylesheet

# if getcwd().replace("\\", "/") not in sys.path:
#     sys.path.append(getcwd().replace("\\", "/"))

from source.YC_core_module import (dragdrop_img, yeti_img, json_img, maya_img, is_windows)
# dragdrop_img    = getcwd() + "/" + "resource" + "/" + "icons" + "/" + "dragdrop_img.png"
# test_thumb      = getcwd() + "/" + "resource" + "/" + "icons" + "/" + "pgYeti_icon.png"



def load_yaml_file(yaml_path):
    try:
        with open(yaml_path) as f:
            load_yml = yaml.safe_load(f)
        return load_yml
    except Exception as e:
        print(str(e))
        return

def mask_image(img_fullpath, size = 128):
    img_path = img_fullpath
    _path, imgtype = path.splitext(img_path)
    img_data = open(img_path, "rb").read()


    if "." in imgtype:
        imgtype = imgtype.replace(".", "")
    # Load image
    image = QtGuiOrig.QImage.fromData(img_data, imgtype)
  
    # convert image to 32-bit ARGB (adds an alpha
    # channel ie transparency factor):
    image.convertToFormat(QtGuiOrig.QImage.Format_ARGB32)
  
    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QtCore.QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
     )
    
    image = image.copy(rect)
  
    # Create the output image with the same dimensions 
    # and an alpha channel and make it completely transparent:
    out_img = QtGuiOrig.QImage(imgsize, imgsize, QtGuiOrig.QImage.Format_ARGB32)
    out_img.fill(QtCore.Qt.transparent)
  
    # Create a texture brush and paint a circle 
    # with the original image onto the output image:
    brush = QtGuiOrig.QBrush(image)
  
    # Paint the output image
    painter = QtGuiOrig.QPainter(out_img)
    painter.setRenderHint(QtGuiOrig.QPainter.Antialiasing, True)
    painter.setBrush(brush)
  
    # Don't draw an outline
    painter.setPen(QtCore.Qt.NoPen)
  
    # drawing circle
    painter.drawEllipse(0, 0, imgsize, imgsize)
  
    # closing painter event
    painter.end()
  
    # Convert the image to a pixmap and rescale it. 
    pr = QtGuiOrig.QWindow().devicePixelRatio()
    pm = QtGuiOrig.QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, QtCore.Qt.KeepAspectRatio, 
                               QtCore.Qt.SmoothTransformation)
  
    # return back the pixmap data
    return pm


class DragDropWidget(QtGui.QWidget):
    def __init__(self, _parent=None, edge_color: list=[], brush_color: list=[]) -> None:
        super(DragDropWidget, self).__init__(_parent)
        if edge_color   == []:
            self.edge_color = [66, 135, 245, 100]
        else:
            self.edge_color     = edge_color

        if brush_color  == []:
            self.brush_color = [245, 132, 66, 100]
        else:
            self.brush_color    = brush_color

        self.font_size      :int = 30
        self.rect_rounded   :int = 5
        self.device_width   :int = 0
        self.device_height  :int = 0
        self.init_data()


    @property
    def edge_color(self) -> QtGuiOrig.QPen:
        return self.__pen

    @edge_color.setter
    def edge_color(self, pen_color: list) -> None:
        self.__pen = QtGuiOrig.QPen()
        self.__pen.setColor(QtGuiOrig.QColor(pen_color[0], pen_color[1], pen_color[2], pen_color[3]))

    @property
    def brush_color(self) -> QtGuiOrig.QBrush:
        return self.__brush

    @brush_color.setter
    def brush_color(self, brush_color: list) -> None:
        self.__brush = QtGuiOrig.QBrush()
        self.__brush.setColor(QtGuiOrig.QColor(brush_color[0], brush_color[1], brush_color[2], brush_color[3]))
        self.__brush.setStyle(QtCore.Qt.SolidPattern)

    def init_data(self) -> None:
        img_data = open(dragdrop_img, "rb").read()
        _path, img_type = path.splitext(dragdrop_img)
        if "." in img_type:
            img_type = img_type.replace(".", "")

        # Load image
        image = QtGuiOrig.QImage.fromData(img_data, img_type)

        self.dragdrop_img_w = image.width()
        self.dragdrop_img_h = image.height()


    def draw_file_inputinform_rect(self, e: QtGuiOrig.QPaintEvent, painter: QtGuiOrig.QPainter) -> None:
        painter.eraseRect(e.rect())
        painter.setPen(QtGuiOrig.QPen(QtGuiOrig.QColor(0, 0, 0), 10,QtCore.Qt.DotLine))
        painter.setBrush(QtGuiOrig.QBrush(QtGuiOrig.QColor(255,255,255,0)))
        cur_font = QtGuiOrig.QFont()
        cur_font.setPixelSize(self.font_size)
        painter.setFont(cur_font)
        painter.drawRoundedRect(QtCore.QRect(0, 0, self.device_width, self.device_height), self.rect_rounded, self.rect_rounded)
        painter.drawText(int(self.device_width/2)-90, int(self.device_height/2)+self.dragdrop_img_h/2+10, "Drag and Drop")
        file_img = QtGuiOrig.QPixmap(dragdrop_img)
        painter.drawPixmap(int(self.device_width/2)-int(self.dragdrop_img_w/2), int(self.device_height/2)-int(self.dragdrop_img_h/2), file_img)
          

    def paintEvent(self, event: QtGuiOrig.QPaintEvent) -> None:
        def init_painter(edge_color, brush_color,_painter):
            _painter.setRenderHint(QtGuiOrig.QPainter.Antialiasing)
            _painter.setPen(edge_color)
            _painter.setBrush(brush_color)

            self.device_width   = _painter.device().width()
            self.device_height  = _painter.device().height()
        _p = QtGuiOrig.QPainter(self)
        init_painter(self.edge_color, self.brush_color, _p)

        self.draw_file_inputinform_rect(event, _p)

        _p.end()


class StatusLabel(QtGui.QLabel):
    def __init__(self, _parent=None) -> None:
        super(StatusLabel, self).__init__(_parent)

    @property
    def CUR_STATUS(self) -> bool:
        return self.__cur_status__

    @CUR_STATUS.setter
    def CUR_STATUS(self, _status :bool) -> None:
        self.__cur_status__ = _status
        self.repaint()

    def paintEvent(self, e: QtGuiOrig.QPaintEvent) -> None:
        cur_p = QtGuiOrig.QPainter(self)
        cur_p.setRenderHint(QtGuiOrig.QPainter.Antialiasing)
        if self.CUR_STATUS == True:
            cur_p.setPen(QtGuiOrig.QPen(QtGuiOrig.QColor(0,255,0,200)))
            cur_p.setBrush(QtGuiOrig.QBrush(QtGuiOrig.QColor(0,255,0,200)))
        else:
            cur_p.setPen(QtGuiOrig.QPen(QtGuiOrig.QColor(255,0,0,200)))
            cur_p.setBrush(QtGuiOrig.QBrush(QtGuiOrig.QColor(255,0,0,200)))

        
        radius = 7
        cur_p.drawEllipse(QtCore.QPoint(7,15), radius, radius)
        
        cur_p.end()


class RoundCheckBox(QtGui.QCheckBox):
    def __init__(self, parent=None):
        super(RoundCheckBox, self).__init__(parent)
        # self.setCheckable(True)
        self.setStyleSheet('''
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: none;
            }
            QCheckBox::indicator::unchecked {
                border-radius: 10px;
                background-color: #b2496d;
            }
            QCheckBox::indicator::checked {
                border-radius: 10px;
                background-color: #578a68;
            }
        ''')

class custom_file_item(QtGui.QWidget):
    def __init__(self, _parent=None) -> None:
        super(custom_file_item, self).__init__(_parent)
        self.setupUi()

    def setupUi(self) -> None:

        self.file_type_thumb_lb = QtGui.QLabel()
        self.file_name_lb       = QtGui.QLabel()
        self.check_exists_lb    = StatusLabel() 
        
        
        self.main_hl = QtGui.QHBoxLayout()
        self.main_hl.addWidget(self.file_type_thumb_lb)
        self.main_hl.addWidget(self.file_name_lb)
        self.main_hl.addWidget(self.check_exists_lb)
        self.main_hl.setStretch(0, 1)
        self.main_hl.setStretch(1, 5)
        self.main_hl.setStretch(2, 1)
        self.setLayout(self.main_hl)
        self.setMinimumSize(300, 50)
        
    def set_info(self, input_path :str) -> None:
        _path, _ext = path.splitext(input_path)
        file_name = path.basename(input_path)
        if _ext == ".grm":
            icon_path = yeti_img
        elif _ext == ".json":
            icon_path = json_img
        elif _ext in [".mb", ".ma"]:
            icon_path = maya_img

        size = 32
        pr = QtGuiOrig.QWindow().devicePixelRatio()
        type_pixmap = QtGuiOrig.QPixmap(icon_path)
        type_pixmap.setDevicePixelRatio(pr)
        size *= pr
        type_pixmap = type_pixmap.scaled(size, size, QtCore.Qt.KeepAspectRatio, 
                                                     QtCore.Qt.SmoothTransformation)
        
        self.file_type_thumb_lb.setPixmap(type_pixmap)

        self.file_name_lb.setText(file_name)
        
        if path.exists(input_path) == True:
            self.check_exists_lb.CUR_STATUS = True
        else:
            self.check_exists_lb.CUR_STATUS = False




class custom_listwidget(QtGui.QListWidget):
    def __init__(self, _parent=None) -> None:
        super(custom_listwidget, self).__init__(_parent)
        self.setMinimumSize(300, 200)
        

    def add_item(self, input_path :str) -> None:
        
        _custom_item = custom_file_item()
        _custom_item.set_info(input_path)
        
    
        _listwidet_item = QtGui.QListWidgetItem(self)
        _listwidet_item.setSizeHint(_custom_item.sizeHint())
        _listwidet_item.setFlags(_listwidet_item.flags() & ~QtCore.Qt.ItemIsDragEnabled)
        self.addItem(_listwidet_item)
        self.setItemWidget(_listwidet_item, _custom_item)

class PubSpecWidget(QtGui.QWidget):
    def __init__(self, _parent=None) -> None:
        super(PubSpecWidget, self).__init__(_parent)
        self.content_widgets = []
        self.pub_infos       = {}
        self.setupUi()

    

    def setupUi(self) -> None:
        self.thumb_lb = QtGui.QLabel()
        # thumb_pixmap = mask_image(test_thumb, 64)
        # self.thumb_lb.setPixmap(thumb_pixmap)
        self.thumb_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.thumb_lb.setStyleSheet('''
                                        QLabel {
                                            background-color: transparent;
                                            border: none;
                                            margin: 10;
                                        }
                                    ''')

        self.assetname_lb = QtGui.QLabel("Asset Name")
        self.assetname_lb.setStyleSheet('''QLabel{padding-left : 1px;}''')
        self.assetanem_contents_lb = QtGui.QLabel("...")

        self.variant_lb = QtGui.QLabel("Variant")
        self.variant_lb.setStyleSheet('''QLabel{padding-left : 1px;}''')
        self.variant_contents_lb = QtGui.QLabel("...")

        self.version_lb = QtGui.QLabel("Version")
        self.version_lb.setStyleSheet('''QLabel{padding-left : 1px;}''')
        self.version_contents_lb = QtGui.QLabel("...")

        self.desc_lb = QtGui.QLabel("Description")
        self.desc_lb.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.desc_lb.setStyleSheet('''QLabel{padding-top : 7px;}''')
        self.desc_contents_te = QtGui.QTextBrowser()
        self.desc_contents_te.setText("...")

        self.content_widgets.append(self.assetanem_contents_lb)
        self.content_widgets.append(self.variant_contents_lb)
        self.content_widgets.append(self.version_contents_lb)
        self.content_widgets.append(self.desc_contents_te)

        self.pub_info_gl = QtGui.QGridLayout()
        self.pub_info_gl.addWidget(self.assetname_lb, 0, 0)
        self.pub_info_gl.addWidget(self.assetanem_contents_lb, 0, 1)
        self.pub_info_gl.addWidget(self.variant_lb, 1, 0)
        self.pub_info_gl.addWidget(self.variant_contents_lb, 1, 1)
        self.pub_info_gl.addWidget(self.version_lb, 2, 0)
        self.pub_info_gl.addWidget(self.version_contents_lb, 2, 1)
        self.pub_info_gl.addWidget(self.desc_lb, 3, 0)
        self.pub_info_gl.addWidget(self.desc_contents_te, 3, 1)
        self.pub_info_gl.setColumnStretch(0, 1)
        self.pub_info_gl.setColumnStretch(1, 3)
        self.pub_info_gl.setRowStretch(0,1)
        self.pub_info_gl.setRowStretch(1,1)
        self.pub_info_gl.setRowStretch(2,1)
        self.pub_info_gl.setRowStretch(3,3)
        self.left_sub_vl = QtGui.QVBoxLayout()
        self.left_sub_vl.addWidget(self.thumb_lb)
        self.left_sub_vl.addLayout(self.pub_info_gl)
        self.left_sub_vl.setStretch(0,2)
        self.left_sub_vl.setStretch(1,5)
        



        self.file_check_lw = custom_listwidget()


        self.right_sub_vl = QtGui.QVBoxLayout()
        self.right_sub_vl.addWidget(self.file_check_lw)

        self.contents_main_hl = QtGui.QHBoxLayout()
        self.contents_main_hl.addLayout(self.left_sub_vl)
        self.contents_main_hl.addLayout(self.right_sub_vl)

        self.setLayout(self.contents_main_hl)
        self.setMinimumSize(300, 300)
        self.set_contents_stylesheet()

    def set_contents_stylesheet(self) -> None:
        background_color    = "#232629"
        border_color        = "#232629"
        for _widget in self.content_widgets:
            if isinstance(_widget, QtGui.QLabel):
                _widget.setStyleSheet(f'''
                                        QLabel{{
                                            background-color : {background_color};
                                            border           : {border_color};
                                            border-radius    : 15px;
                                            padding-left     : 5px;
                                        }}
                                        ''')

    def get_pub_info(self) -> dict:
        return self.pub_infos

    def set_info_from_pubpath(self, dropped_path :str) -> None:
        
        def make_exists_fullpath(pub_path :str, search_path :str, rel_path :str) -> str:
            check_path = path.join(search_path, rel_path)
            if path.exists(check_path) == True:
                return check_path
            else:
                pub_dirpath = path.dirname(pub_path)
                return path.join(pub_dirpath, rel_path)

        def get_realpath(pub_path :str, pub_info :dict) -> set:
            search_path         = pub_info["SEARCH_PATH"]
            
            grm_relpaths        = pub_info["PUBS"]["GRMS"]
            attr_json_relpath   = pub_info["PUBS"]["ATTR_JSON"].replace("\\", "/")
            main_json_relpath   = pub_info["PUBS"]["MAIN_JSON"].replace("\\", "/")
            maya_relpath        = pub_info["PUBS"]["MAYA"].replace("\\", "/")

            grm_fullpath_list   = []
            for grm_relpath in grm_relpaths: grm_fullpath_list.append(make_exists_fullpath(pub_path, search_path, grm_relpath))
            attr_json_fullpath  = make_exists_fullpath(pub_path, search_path, attr_json_relpath)
            main_json_fullpath  = make_exists_fullpath(pub_path, search_path, main_json_relpath)
            maya_fullpath       = make_exists_fullpath(pub_path, search_path, maya_relpath)
            return grm_fullpath_list, attr_json_fullpath, main_json_fullpath, maya_fullpath
        
        pub_info = load_yaml_file(dropped_path)
        grm_fullpath_list, attr_json_path, main_json_path, maya_path = get_realpath(dropped_path, pub_info)
        for grm_path in grm_fullpath_list: self.file_check_lw.add_item(grm_path)
        self.file_check_lw.add_item(attr_json_path)
        self.file_check_lw.add_item(main_json_path)
        self.file_check_lw.add_item(maya_path)

        self.pub_infos["MAIN_JSON"] = main_json_path
        self.pub_infos["ATTR_JSON"] = attr_json_path
        self.pub_infos["MAYA"]      = maya_path
        self.pub_infos["GROOMS"]    = grm_fullpath_list



        # Set String Information
        thumb_path      = pub_info["THUMBNAIL"].replace("\\", "/")
        asset_name      = pub_info["ASSETNAME"]
        variant_name    = pub_info["VARIANT"]
        version_num     = pub_info["VERSION"]
        desc            = pub_info["DESC"]

        masked_pixmap = mask_image(thumb_path)
        self.thumb_lb.setPixmap(masked_pixmap)

        self.assetanem_contents_lb.setText(asset_name)
        self.variant_contents_lb.setText(variant_name)
        self.version_contents_lb.setText(version_num)
        self.desc_contents_te.setText(desc)

        self.pub_infos["VERSION"] = version_num


class PubView(QtGui.QDialog):
    def __init__(self, _parent=None) -> None:
        super(PubView, self).__init__(_parent)

        self.CUR_STEP = "CHECK_FILE"
        self.setupUi()

    def setupUi(self):

        self.drag_drop_wg = DragDropWidget()

        self.pub_spec_wg = PubSpecWidget()

        self.main_tb = QtGui.QTabWidget()
        self.main_tb.setStyleSheet("QTabBar::tab { border: 0; height: 0px;}")
        self.main_tb.addTab(self.drag_drop_wg, "Tab 1")
        self.main_tb.addTab(self.pub_spec_wg, "Tab 2")


        h_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.assign_btn = QtGui.QPushButton("Assign")
        self.assign_btn.clicked.connect(partial(self.set_res, True))
        self.cancel_btn = QtGui.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(partial(self.set_res, False))

        self.btn_hl = QtGui.QHBoxLayout()
        self.btn_hl.addItem(h_spacer)
        self.btn_hl.addWidget(self.assign_btn)
        self.btn_hl.addWidget(self.cancel_btn)
        self.btn_hl.setStretch(0,5)
        self.btn_hl.setStretch(1,1)
        self.btn_hl.setStretch(2,1)

        self.main_vl = QtGui.QVBoxLayout()
        self.main_vl.addWidget(self.main_tb)
        
        
        self.setLayout(self.main_vl)


        self.main_tb.setCurrentIndex(0)
        self.setMinimumSize(750, 450)
        self.setAcceptDrops(True)

        apply_stylesheet(self, "dark_blue.xml")


    def after_drop_setupUi(self) -> None:
        self.main_vl.addLayout(self.btn_hl)

    def dragEnterEvent(self, event: QtGuiOrig.QDragEnterEvent) -> None:
        if self.CUR_STEP != "CHECK_FILE":
            event.ignore()

        if event.mimeData().hasUrls():
            target_path = event.mimeData().urls()[0]
            target_path = target_path.toString()
            _path, _ext = path.splitext(target_path)
            
            if _ext == ".yaml":
                event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QtGuiOrig.QDragMoveEvent) -> None:
        pass

    def dropEvent(self, event: QtGuiOrig.QDropEvent) -> None:
        pub_path = event.mimeData().urls()[0]
        pub_path = pub_path.toString()
        if is_windows() == True:
            pub_path = re.sub(r"file:///", "", pub_path)
            self.pub_spec_wg.set_info_from_pubpath(pub_path)
            self.switch_view()

    def switch_view(self, to_type :str="PUB_SPEC") -> None:
        if to_type == "CHECK_FILE":
            self.main_tb.setCurrentIndex(0)
        else:
            self.main_tb.setCurrentIndex(1)
            self.after_drop_setupUi()

    def set_res(self, status :bool) -> None:
        if status == True:
            self.accept()
        else:
            self.reject()

    def get_pub_infos(self) -> dict:
        return self.pub_spec_wg.get_pub_info()

# app = QtGui.QApplication(sys.argv)

# w = PubView()
# w.show()

# app.exec_()