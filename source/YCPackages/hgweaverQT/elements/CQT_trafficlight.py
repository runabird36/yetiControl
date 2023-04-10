# from PyQt5 import QtCore, QtGui, QtWidgets


import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets


class lightBall(QtWidgets.QWidget):
    
    
    
    light_status_changed = QtCore.Signal(bool)

    def __init__(self, _parent=None, brush_color: list=[255, 69, 56, 0], x: int=0, y: int=0, semi_diameter: int=5) -> None:
        super(lightBall, self).__init__(_parent)

        self.__brush = None
        self.__pen   = None
        self.__on    = False

        self.brush_color    = brush_color
        self.light_color    = brush_color
        self.border_color   = [255, 255, 255, 0]
        self.x              = x
        self.y              = y
        self.w              = semi_diameter
        self.h              = semi_diameter
        self.default_alpha_val = brush_color[3]
        self._handle_alpha  = brush_color[3]

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)


        self.anim = QtCore.QPropertyAnimation(self, b'handle_alpha', self)
        self.anim.setDuration(1000)

        
        

        self.light_status_changed.connect(self.set_lightball_anim)


    @QtCore.Property(bool)
    def light_on(self) -> bool:
        return self.__on
        
    @light_on.setter
    def light_on(self, is_on: bool) -> None:
        if self.__on != is_on:
            self.__on = is_on
            self.light_status_changed.emit(is_on)


    @QtCore.Property(int)
    def handle_alpha(self) -> int:
        return self._handle_alpha

    @handle_alpha.setter
    def handle_alpha(self, alpha: int) -> None:
        self._handle_alpha = alpha
        self.update()




    @property
    def border_color(self) -> QtGui.QPen:
        return self.__pen

    @border_color.setter
    def border_color(self, pen_color: list) -> None:
        if len(pen_color) == 3:
            alpha = 0
        else:
            alpha = pen_color[3]
        self.__pen = QtGui.QPen()
        self.__pen.setColor(QtGui.QColor(pen_color[0], pen_color[1], pen_color[2], alpha))


    @property
    def light_color(self) -> QtGui.QBrush:
        return self.__brush


    @light_color.setter
    def light_color(self, brush_color: list) -> None:
        
        self.__brush = QtGui.QBrush()
        self.__brush.setColor(QtGui.QColor(brush_color[0], brush_color[1], brush_color[2], brush_color[3]))
        self.__brush.setStyle(QtCore.Qt.SolidPattern)





    def set_lightball_anim(self, is_on):
        if is_on == False:
            self.anim.setStartValue(255)
            self.anim.setEndValue(self.default_alpha_val)
            self.anim.setEasingCurve(QtCore.QEasingCurve.OutBounce)
        else:
            self.anim.setStartValue(self.default_alpha_val)
            self.anim.setEndValue(255)
            self.anim.setEasingCurve(QtCore.QEasingCurve.InBounce)

        self.anim.start()



    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(self.border_color)
        self.brush_color[3] = self.handle_alpha
        self.light_color = self.brush_color
        painter.setBrush(self.light_color)
        painter.drawEllipse(self.x, self.y, self.w, self.h)
        painter.end()
        

        return super().paintEvent(e)



class trafficLight(QtWidgets.QWidget):
    def __init__(self, _parent=None, lightball_size: int=35, alpha: int=15) -> None:
        super(trafficLight, self).__init__(_parent)
        self.semi_diameter = lightball_size
        self.default_off_alpha = alpha
        self.padding_between_balls = 25
        self.light_connected = False
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("Form")
        # self.resize(400, 85)
        self.setFixedSize((self.semi_diameter+self.padding_between_balls)*3, self.semi_diameter+25)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")



        self.red_lightball = lightBall(self, [246, 103, 100, self.default_off_alpha], semi_diameter=self.semi_diameter)
        self.horizontalLayout.addWidget(self.red_lightball)

        self.yellow_lightball = lightBall(self, [254, 191, 77, self.default_off_alpha], semi_diameter=self.semi_diameter)
        self.horizontalLayout.addWidget(self.yellow_lightball)

        self.green_lightball = lightBall(self, [65, 198, 91, self.default_off_alpha], semi_diameter=self.semi_diameter)
        self.horizontalLayout.addWidget(self.green_lightball)

        

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("traffic light")
        # self.pushButton_2.setText(_translate("Form", "PushButton"))
        # self.pushButton.setText(_translate("Form", "PushButton"))
        # self.label.setText(_translate("Form", "TextLabel"))


    @property
    def red_light(self) -> bool:
        return self.red_lightball.light_on

    @red_light.setter
    def red_light(self, status: bool=False) -> None:
        if self.light_connected == True and self.yellow_light == True:
            self.yellow_light = False
        if self.light_connected == True and self.green_light == True:
            self.green_light = False
        self.red_lightball.light_on = status

    @property
    def yellow_light(self) -> bool:
        return self.yellow_lightball.light_on

    @yellow_light.setter
    def yellow_light(self, status: bool=False) -> None:
        if self.light_connected == True and self.red_light == True:
            self.red_light = False
        if self.light_connected == True and self.green_light == True:
            self.green_light = False
        self.yellow_lightball.light_on = status

    @property
    def green_light(self) -> bool:
        return self.green_lightball.light_on

    @green_light.setter
    def green_light(self, status: bool=False) -> None:
        if self.light_connected == True and self.yellow_light == True:
            self.yellow_light = False
        if self.light_connected == True and self.red_light == True:
            self.red_light = False
        self.green_lightball.light_on = status


    def set_connect_light_mode(self, light_status_connected: bool=False) -> None:
        self.light_connected = light_status_connected


