

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from qt_material import apply_stylesheet
import sys, re
from os import (path, getcwd)
try:
    from source.YC_core_module import (dragdrop_img, yeti_img, json_img, maya_img, is_windows)
except:
    if getcwd() not in sys.path:
        sys.path.append(getcwd())
    from source.YC_core_module import (dragdrop_img, yeti_img, json_img, maya_img, is_windows)


class DragDropWidget(QtGui.QWidget):
    __DROPPED__ = QtCore.Signal(str)
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

        self.setAcceptDrops(True)


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


    def dragEnterEvent(self, event: QtGuiOrig.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            target_path = event.mimeData().urls()[0]
            target_path = target_path.toString()
            _path, _ext = path.splitext(target_path)
            
            if _ext == ".json":
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
            self.__DROPPED__.emit(pub_path)



class InfoWidget(QtGui.QWidget):
    def __init__(self, _parent=None) -> None:
        super(InfoWidget, self).__init__(_parent)

        self.message_label = QtGui.QLabel("Would you like to do Save rest pose with dropped file ?")

        self.ok_btn = QtGui.QPushButton("Ok")
        self.cancel_btn = QtGui.QPushButton("Cancel")

        self.btn_hl = QtGui.QHBoxLayout()
        self.btn_hl.addWidget(self.ok_btn)
        self.btn_hl.addWidget(self.cancel_btn)

        self.main_vl = QtGui.QVBoxLayout()
        self.main_vl.addWidget(self.message_label)
        self.main_vl.addLayout(self.btn_hl)

        self.setLayout(self.main_vl)
        

class SelectView(QtGui.QDialog):
    def __init__(self, _parent=None) -> None:
        super(SelectView, self).__init__(_parent)


        self.target_path = ""

        self.select_wg = DragDropWidget()
        self.select_wg.__DROPPED__.connect(self.switch_view)

        
        self.info_wg = InfoWidget()
        self.info_wg.ok_btn.clicked.connect(self.start_save_restPose)
        self.info_wg.cancel_btn.clicked.connect(self.cancel_view)
        

        self.main_tb = QtGui.QTabWidget()
        self.main_tb.setStyleSheet("QTabBar::tab { border: 0; height: 0px;}")
        self.main_tb.addTab(self.select_wg, "Tab 1")
        self.main_tb.addTab(self.info_wg, "Tab 2")
        self.main_tb.setCurrentIndex(0)

        self.main_vl = QtGui.QVBoxLayout()
        self.main_vl.addWidget(self.main_tb)

        self.setLayout(self.main_vl)
        self.resize(350, 250)
        self.setWindowTitle("Save Guide Restpose")

        apply_stylesheet(self, "dark_blue.xml")

    def switch_view(self, drop_path :str) -> None:
        self.target_path = drop_path

        self.main_tb.setCurrentIndex(1)


    def start_save_restPose(self) -> None:
        self.accept()

    def cancel_view(self) -> None:
        self.reject()

    def get_dropped_path(self) -> str:
        return self.target_path



    

# app = QtGui.QApplication(sys.argv)

# w = SelectView()
# if w.exec_():
#     print(w.get_dropped_path())
# else:
#     print(1111111)

# app.exec_()