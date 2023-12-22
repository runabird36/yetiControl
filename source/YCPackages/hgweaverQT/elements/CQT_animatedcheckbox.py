# -*- coding: utf-8 -*-


# try:
#     from PySide import QtGui, QtCore
#     from shiboken import wrapInstance
#
# except:
#     import PySide2.QtCore as QtCore
#     import PySide2.QtGui as QtGui
#     import PySide2.QtWidgets as QtGuiWidgets
#     from shiboken2 import wrapInstance
#     QtGuiOrig = QtGui
#     QtGui = QtGuiWidgets





import time

from PySide2.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF, QObject,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    pyqtSlot, pyqtProperty)




from PySide2.QtWidgets import QCheckBox
from PySide2.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter, QFont
class AnimatedToggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _font_pen = QPen(Qt.black)
    _light_grey_pen = QPen(Qt.lightGray)
    # bar_color=Qt.gray,
    def __init__(self,
        parent=None,
        bar_color="#FF8B00",
        checked_color="#00B0FF",
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE",
        checked_text="",
        unchecked_text=""
        ):
        super(AnimatedToggle, self).__init__(parent)

        turn_on_color = "#74b938"
        turn_off_color ="#c9c9c9"
        text_color = "#ffffff"
        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(QColor(bar_color).lighter())
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(QColor(bar_color))
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))


        self._turn_on_brush = QBrush(QColor(turn_on_color))
        self._turn_off_brush = QBrush(QColor(turn_off_color))
        self._text_brush = QBrush(QColor(text_color))
        self._text_pen = QPen(QColor(text_color))

        self.checked_msg = checked_text
        self.unchecked_msg = unchecked_text


        # Setup the rest of the widget.

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self._pulse_radius = 0

        _anim_speed = 500
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.OutBounce )
        self.animation.setDuration(_anim_speed)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(_anim_speed)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())


        p = QPainter(self)
        p.setRenderHint(QPainter.HighQualityAntialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._turn_on_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._text_brush)

        else:
            p.setBrush(self._turn_off_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            # p.setPen(self._light_grey_pen)
            p.setBrush(self._text_brush)



        p.setPen(self._text_pen)
        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(9)
        p.setFont(font)

        _h_diff = 5
        _w_diff = 2
        if self.isChecked():
            p.drawText(barRect.x()+_w_diff+2, barRect.y()+barRect.height()-_h_diff, "On")
        else:
           p.drawText(barRect.x()+barRect.width()-30-_w_diff, barRect.y()+barRect.height()-_h_diff, "Off")





        p.setPen(self._transparent_pen)
        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)



        p.end()



    def get_handle_position(self): return self._handle_position
    def set_handle_position(self, _h_pos): self._handle_position = _h_pos; self.update()
    handle_position = pyqtProperty(float, get_handle_position, set_handle_position)

    def get_pulse_radius(self): return self._pulse_radius
    def set_pulse_radius(self, _p_radius): self._pulse_radius = _p_radius; self.update()
    pulse_radius = pyqtProperty(float, get_pulse_radius, set_pulse_radius)

















