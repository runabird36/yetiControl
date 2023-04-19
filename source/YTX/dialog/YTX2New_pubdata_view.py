
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from os import path, getcwd
import sys
from qt_material import apply_stylesheet

# from source.YC_core_module import dragdrop_img
dragdrop_img    = getcwd() + "/" + "resource" + "/" + "icons" + "/" + "dragdrop_img.png"
test_thumb      = getcwd() + "/" + "resource" + "/" + "icons" + "/" + "pgYeti_icon.png"





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


class custom_file_item(QtGui.QWidget):
    def __ini__(self, _parent=None) -> None:
        super(custom_file_item, self).__init__()
        self.setupUi()

    def setupUi(self) -> None:

        self.main_

        self.setLayout()


class custom_listwidget(QtGui.QListWidget):
    def __init__(self, _parent=None) -> None:
        super(custom_listwidget, self).__init__(_parent)

    def add_item(self, input_path :str) -> None:
        
        _custom_item = QtGui.UploadProcess_item()
        _custom_item.set_info(input_path)
        
    
        _listwidet_item = QtGui.QListWidgetItem(self)
        _listwidet_item.setSizeHint(_custom_item.sizeHint())
        _listwidet_item.setFlags(_listwidet_item.flags() & ~QtCore.Qt.ItemIsDragEnabled)
        self.addItem(_listwidet_item)
        self.setItemWidget(_listwidet_item, _custom_item)



class PubView(QtGui.QDialog):
    def __init__(self, _parent=None) -> None:
        super(PubView, self).__init__(_parent)
        self.setupUi()

    def setupUi(self):

        self.drag_drop_wg = DragDropWidget()

        self.thumb_lb = QtGui.QLabel()
        thumb_pixmap = mask_image(test_thumb, 64)
        self.thumb_lb.setPixmap(thumb_pixmap)
        self.thumb_lb.setStyleSheet('''
                                        QLabel {
                                            background-color: transparent;
                                            border: none;
                                            padding-left: 50;
                                            margin: 0;
                                        }
                                    ''')

        self.assetname_lb = QtGui.QLabel("Asset Name")
        self.assetanem_contents_lb = QtGui.QLabel("...")

        self.variant_lb = QtGui.QLabel("Variant")
        self.variant_contents_lb = QtGui.QLabel("...")

        self.version_lb = QtGui.QLabel("Version")
        self.version_contents_lb = QtGui.QLabel("...")

        self.desc_lb = QtGui.QLabel("Description")
        self.desc_contents_te = QtGui.QTextBrowser()
        self.desc_contents_te.setText("...")

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
        self.left_sub_vl = QtGui.QVBoxLayout()
        self.left_sub_vl.addWidget(self.thumb_lb)
        self.left_sub_vl.addLayout(self.pub_info_gl)
        

        self.right_sub_vl = QtGui.QVBoxLayout()

        self.contents_main_hl = QtGui.QHBoxLayout()
        self.contents_main_hl.addLayout(self.left_sub_vl)
        self.contents_main_hl.addLayout(self.right_sub_vl)


        self.contents_wg = QtGui.QWidget()
        self.contents_wg.setLayout(self.contents_main_hl)

        self.main_tb = QtGui.QTabWidget()
        self.main_tb.setStyleSheet("QTabBar::tab { border: 0; height: 0px;}")
        self.main_tb.addTab(self.drag_drop_wg, "Tab 1")
        self.main_tb.addTab(self.contents_wg, "Tab 2")

        self.main_vl = QtGui.QVBoxLayout()
        self.main_vl.addWidget(self.main_tb)
        
        self.setLayout(self.main_vl)


        self.main_tb.setCurrentIndex(1)
        self.resize(600, 400)

        apply_stylesheet(self, "dark_blue.xml")





app = QtGui.QApplication(sys.argv)

w = PubView()
w.show()

app.exec_()