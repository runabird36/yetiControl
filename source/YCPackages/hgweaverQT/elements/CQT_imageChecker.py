# from PyQt5 import QtCore, QtGui, QtGui
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from traceback import print_exc
from os import path
from CQT_path_module import dragdrop_img, dragdrop_img_w, dragdrop_img_h

# import PySide2.QtCore as QtCore
# import PySide2.QtGui as QtGui
# import PySide2.QtGui as QtGui


class imageChecker(QtGui.QWidget):
    
    
    
    file_dropped    = QtCore.Signal()
    reset_ui        = QtCore.Signal()
    rect_rounded    = 5

    __mouse_pose = QtCore.QPoint(0, 0)
    __bg_rect = QtCore.QRect(0, 0, 0, 0)


    def __init__(self, _parent=None, edge_color: list=[], brush_color: list=[]) -> None:
        super(imageChecker, self).__init__(_parent)

        if edge_color   == []:
            self.edge_color = [66, 135, 245, 100]
        else:
            self.edge_color     = edge_color

        if brush_color  == []:
            self.brush_color = [245, 132, 66, 100]
        else:
            self.brush_color    = brush_color

        self.font_size = 30

        self.device_width   :int = 0
        self.device_height  :int = 0

        self.cur_image: str = "" 

        self.is_dragged = False                 # when in dragMoveEvent, value is True. and when in dropEvent, value is False
        self.is_dropped = False                 # when in dropEvent, value is True. and when animation ends, value is False 

        self.is_drawing = False

        self.is_painted = False

        self.is_left    = True
        

        self.setAcceptDrops(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        


        self.anim = QtCore.QPropertyAnimation(self, b'handle_bg_rect', self)
        self.anim.setDuration(350)
        self.anim.finished.connect(self.set_finished_attr)

        
        

        self.file_dropped.connect(self.set_drop_background_aim)
        self.reset_ui.connect(self.dragLeaveEvent)

        
        

    

    @property
    def edge_color(self) -> QtGuiOrig.QPen:
        return self.__pen

    @edge_color.setter
    def edge_color(self, pen_color: list) -> None:
        print(pen_color)
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



    @property
    def font_size(self):
        return self.__fontsize

    @font_size.setter
    def font_size(self, font_size) -> None:
        self.__fontsize = font_size






    @QtCore.Property(QtCore.QRect)
    def handle_bg_rect(self) -> QtCore.QRect:
        return self.__bg_rect

    @handle_bg_rect.setter
    def handle_bg_rect(self, rect: QtCore.QRect) -> None:
        self.__bg_rect = rect
        self.update()



    @QtCore.Property(QtCore.QPoint)
    def mouse_pose(self) -> QtCore.QPoint:
        return self.__mouse_pose

    @mouse_pose.setter
    def mouse_pose(self, mousepose: QtCore.QPoint) -> None:
        self.__mouse_pose = mousepose
        self.update()



    def set_finished_attr(self) -> None:
        self.is_dragged = False
        self.is_dropped = False
        self.is_drawing = False



    def get_init_rect(self) -> QtCore.QRect:
        rect_size = 120
        center_pos = self.mouse_pose
        return QtCore.QRect(center_pos.x()-int(rect_size/2), center_pos.y()-int(rect_size/2), rect_size, rect_size)

    def set_drop_background_aim(self):
        
        print("start! anim")
        print("dragged : ", self.is_dragged)
        print("dropped : ", self.is_dropped)
        
        if self.is_dragged == False and self.is_dropped == True:
            self.is_drawing = True
            self.anim.setStartValue(self.get_init_rect())
            self.anim.setEndValue(QtCore.QRect(0,0, self.device_width, self.device_height))
            self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.anim.start()


    def draw_moving_rect(self, painter: QtGuiOrig.QPainter) -> None:
        rect_size = 120
        center_pos = self.mouse_pose
        
        painter.drawRoundedRect(self.get_init_rect(), self.rect_rounded, self.rect_rounded)


    def draw_img(self, painter: QtGuiOrig.QPainter, bg_rect: QtCore.QRect, img_path: str) -> None:
        painter.drawRoundedRect(bg_rect, self.rect_rounded, self.rect_rounded)

        # print("is drawing : ", self.is_drawing)
        if self.is_drawing == False and path.exists(img_path) == True:
            padding = 20
            file_img = QtGuiOrig.QPixmap(img_path)
            img_width   = file_img.rect().width()
            img_height  = file_img.rect().height()

            painter_center = bg_rect.center()
            



            

            if img_width > self.device_width:
                to_scaled_width     = self.device_width - padding
            else:
                to_scaled_width     = img_width         - padding
            if img_height > self.device_height:
                to_scaled_height    = self.device_height - padding
            else:
                to_scaled_height    = img_height         - padding


            real_img_x = painter_center.x() - to_scaled_width/2
            real_img_y = painter_center.y() - to_scaled_height/2
            
            # self.setFixedHeight(to_scaled_height)
            scaled_img = file_img.scaled(to_scaled_width, to_scaled_height, QtCore.Qt.KeepAspectRatio)






            painter.drawPixmap(int(real_img_x), int(real_img_y), to_scaled_width, to_scaled_height, scaled_img)
            self.is_painted = True
    
    
    def draw_file_inputinform_rect(self, e: QtGuiOrig.QPaintEvent, painter: QtGuiOrig.QPainter) -> None:
        painter.eraseRect(e.rect())
        painter.setPen(QtGuiOrig.QPen(QtGuiOrig.QColor(0, 0, 0), 10,QtCore.Qt.DotLine))
        painter.setBrush(QtGuiOrig.QBrush(QtGuiOrig.QColor(255,255,255,0)))
        cur_font = QtGuiOrig.QFont()
        cur_font.setPixelSize(self.font_size)
        painter.setFont(cur_font)
        painter.drawRoundedRect(QtCore.QRect(0, 0, self.device_width, self.device_height), self.rect_rounded, self.rect_rounded)
        painter.drawText(int(self.device_width/2)-90, int(self.device_height/2)+dragdrop_img_h/2+10, "Drag and Drop")
        file_img = QtGuiOrig.QPixmap(dragdrop_img)
        # scaled_img = file_img.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        painter.drawPixmap(int(self.device_width/2)-int(dragdrop_img_w/2), int(self.device_height/2)-int(dragdrop_img_h/2), file_img)
            

    def paintEvent(self, e: QtGuiOrig.QPaintEvent=None) -> None:
        def init_painter(edge_color, brush_color,_painter):
            _painter.setRenderHint(QtGuiOrig.QPainter.Antialiasing)
            _painter.setPen(edge_color)
            _painter.setBrush(brush_color)

            self.device_width   = _painter.device().width()
            self.device_height  = _painter.device().height()
        
        painter = QtGuiOrig.QPainter(self)
        init_painter(self.edge_color, self.brush_color, painter)

        
        

        if self.is_dragged == True and self.is_dropped == False:
            self.draw_moving_rect(painter)
        
        
        if self.is_dropped == True and self.cur_image == "":
            self.draw_file_inputinform_rect(e, painter)

        if self.is_left == True:
            self.draw_file_inputinform_rect(e, painter)
        
        if (self.is_dragged == True and self.is_painted == True):
            r = QtCore.QRect(-1, -1, 2, 2)
            painter.setWindow(r)
        
        if self.is_drawing == True and self.is_dropped == True and self.is_dragged == False:
            next_x = self.handle_bg_rect.x() - 1
            next_y = self.handle_bg_rect.y() - 1
            next_w = self.handle_bg_rect.width() + 1
            next_h = self.handle_bg_rect.height() + 1
            self.handle_bg_rect = QtCore.QRect(next_x, next_y, next_w, next_h)
            self.draw_img(painter, self.handle_bg_rect, self.cur_image)
        else:
            self.draw_img(painter, self.handle_bg_rect, self.cur_image)

        painter.end()
        


    def dragEnterEvent(self, event: QtGuiOrig.QDragEnterEvent) -> None:
        self.is_left = False
        has_urls = event.mimeData().hasUrls()
        if has_urls == True:
            event.setAccepted(True)


        return super().dragEnterEvent(event)

    def dragMoveEvent(self, event: QtGuiOrig.QDragMoveEvent) -> None:
        # print(event)
        # print("type : ", type(event))
        # print("Pos  : ", event.pos())
        # print("="*50)
        if self.is_dropped == True:
            self.is_dropped = False

        has_urls = event.mimeData().hasUrls()
        if has_urls == True:
            self.is_dragged = True
            self.mouse_pose = event.pos()
        else:
            self.is_dragged = False
        return super().dragMoveEvent(event)



    def dropEvent(self, event: QtGuiOrig.QDropEvent) -> None:
        
        if self.is_dragged == True:
            self.is_dragged = False

        has_urls = event.mimeData().hasUrls()
        
        urls = event.mimeData().urls()
        first_url = urls[0]
        first_url_str = first_url.toString()
        
        if first_url_str == None or first_url_str == "":
            self.reject()
        if first_url_str.startswith("file://"):
            self.is_dropped = True


            first_url_str = first_url_str.replace("file://", "")
            self.cur_image = first_url_str
            self.file_dropped.emit()
        
        return super().dropEvent(event)


    def dragLeaveEvent(self, a0: QtGuiOrig.QDragLeaveEvent=None) -> None:
        self.is_left = True
        self.is_dragged = False                 
        self.is_dropped = False

        self.is_drawing = False

        self.is_painted = False
        self.update()
        return super().dragLeaveEvent(a0)






# class PowerBar(QtGui.QWidget):
#     """
#     Custom Qt Widget to show a power bar and dial.
#     Demonstrating compound and custom-drawn widget.
#     """

#     def __init__(self, _parent=None):
#         super(PowerBar, self).__init__(_parent)
#         self.resize(800, 500)
        


#         layout = QtGui.QHBoxLayout()
        
#         self.custom_w = imageChecker(self)
#         layout.addWidget(self.custom_w)

#         # self.pushButton_2 = QtGui.QPushButton(self)
#         # self.pushButton_2.setObjectName("pushButton_2")
#         # self.pushButton_2.setText("Red")
#         # layout.addWidget(self.pushButton_2)

#         # self.pushButton_3 = QtGui.QPushButton(self)
#         # self.pushButton_3.setObjectName("pushButton_3")
#         # self.pushButton_3.setText("Yellow")
#         # layout.addWidget(self.pushButton_3)

#         # self.pushButton_5 = QtGui.QPushButton(self)
#         # self.pushButton_5.setObjectName("pushButton_2")
#         # self.pushButton_5.setText("Green")
#         # layout.addWidget(self.pushButton_5)


#         # self._dial = QtGui.QDial()
#         # layout.addWidget(self._dial)

#         # layout.setStretch(0,1)
#         # layout.setStretch(1,1)
#         # layout.setStretch(2,1)
#         # layout.setStretch(3,1)

#         self.setLayout(layout)





# app = QtGui.QApplication([])
# volume = PowerBar()
# volume.show()
# app.exec_()





















# class AppMainUI(QtGui.QMainWindow):
#     def __init__(self, parent=None):
#         QtGui.QMainWindow.__init__(self, parent)

#         pass

#         self.edge_color = [66, 135, 245, 100]
#         self.brush_color = [245, 132, 66, 100]

#     # def paintEvent(self,event):
#     #     painter = QtGui.QPainter(self)
#     #     painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
#     #     scaled_pix = self.pixmap.scaled(self.size().width(), self.size().height(), Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
#     #     point = QtCore.QPoint(0,0)
#     #     point.setX((self.size().width()-scaled_pix.width())/2)
#     #     point.setY((self.size().height()-scaled_pix.height())/2-10)
#     #     painter.drawPixmap(point, scaled_pix)



#     @property
#     def edge_color(self) -> QtGui.QPen:
#         return self.__pen

#     @edge_color.setter
#     def edge_color(self, pen_color: list) -> None:
#         self.__pen = QtGui.QPen()
#         self.__pen.setColor(QtGui.QColor(pen_color[0], pen_color[1], pen_color[2], pen_color[3]))


#     @property
#     def brush_color(self) -> QtGui.QBrush:
#         return self.__brush


#     @brush_color.setter
#     def brush_color(self, brush_color: list) -> None:
        
#         self.__brush = QtGui.QBrush()
#         self.__brush.setColor(QtGui.QColor(brush_color[0], brush_color[1], brush_color[2], brush_color[3]))
#         self.__brush.setStyle(QtCore.Qt.SolidPattern)


#     # def paintEvent(self, event):
#     #     path = QtGui.QPainterPath()
#     #     path.addRoundedRect(QtCore.QRectF(self.rect()), float(12.0), float(12.0))
#     #     mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
#     #     self.setMask(mask)

#     def paintEvent(self, e: QtGui.QPaintEvent=None) -> None:
#         print(222222222222222)
#         painter = QtGui.QPainter(self)
#         painter.setRenderHint(QtGui.QPainter.Antialiasing)
#         painter.setPen(self.edge_color)
#         painter.setBrush(self.brush_color)
#         painter.drawEllipse(100, 100, 30, 30)
#         painter.end()
        

#         return super().paintEvent(e)

# if __name__=='__main__':
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     main = AppMainUI()
#     main.show()
#     sys.exit(app.exec_())