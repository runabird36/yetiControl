# -*- coding:utf-8 -*-

import os
import sys
import time
import tempfile
import PySide2.QtCore as QtCore
from PySide2 import QtWidgets, QtGui, QtCore

class ScreenGrabber(QtWidgets.QDialog):
    SCREEN_GRAB_CALLBACK = None

    def __init__(self, parent=None):
        super(ScreenGrabber, self).__init__(parent)
        self._opacity = 1
        self._click_pos = None
        self._capture_rect = QtCore.QRect()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.setMouseTracking(True)
        desktop = QtWidgets.QApplication.desktop()
        desktop.resized.connect(self._fit_screen_geometry)
        desktop.screenCountChanged.connect(self._fit_screen_geometry)

    @property
    def capture_rect(self):
        return self._capture_rect

#===============================================================================
# mouse dragging, paint Update
#===============================================================================
    def paintEvent(self, event):
        # Convert click and current mouse positions to local space.
        mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        click_pos = None
        if self._click_pos is not None:
            click_pos = self.mapFromGlobal(self._click_pos)
        painter = QtGui.QPainter(self)
        # Draw background. Aside from aesthetics, this makes the full
        # tool region accept mouse events.
        painter.setBrush(QtGui.QColor(0, 42, 34, self._opacity))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRect(event.rect())
        # Clear the capture area
        if click_pos is not None:
            capture_rect = QtCore.QRect(click_pos, mouse_pos)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
            painter.drawRect(capture_rect)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 64), 1, QtCore.Qt.DashDotDotLine)
        painter.setPen(pen)
        # Draw cropping markers at click position
        if click_pos is not None:
            painter.drawLine(event.rect().left(), click_pos.y(),
                             event.rect().right(), click_pos.y())
            painter.drawLine(click_pos.x(), event.rect().top(),
                             click_pos.x(), event.rect().bottom())
        # Draw cropping markers at current mouse position
        painter.drawLine(event.rect().left(), mouse_pos.y(),
                         event.rect().right(), mouse_pos.y())
        painter.drawLine(mouse_pos.x(), event.rect().top(),
                         mouse_pos.x(), event.rect().bottom())
        if sys.platform.count("win"):
            prePath = "Z:/backstage/maya/loader/icon/"
        else:
            prePath = "/usersetup/linux/module/ui_icons_md/"
        logoImage = QtGui.QImage(prePath + "giantLogo.png")
        painter.drawImage(QtCore.QRectF(mouse_pos.x() + 10, mouse_pos.y() + 10, 128, 20), logoImage)


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # Begin click drag operation
            self._click_pos = event.globalPos()


    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self._click_pos is not None:
            # End click drag operation and commit the current capture rect
            self._capture_rect = QtCore.QRect(self._click_pos, event.globalPos()).normalized()
            self._click_pos = None
        self.close()


    def mouseMoveEvent(self, event):
        self.repaint()


    @classmethod
    def screen_capture(cls):
        if cls.SCREEN_GRAB_CALLBACK:
            # use an external callback for screen grabbing
            return cls.SCREEN_GRAB_CALLBACK()
        else:
            # on windows, just use the QT solution.
            tool = ScreenGrabber()
            tool.exec_()
            return get_desktop_pixmap(tool.capture_rect)


    def showEvent(self, event):
        self._fit_screen_geometry()
        return
        # Start fade in animation
        try:
            fade_anim = QtCore.QPropertyAnimation(self, "opacity", self)
            fade_anim.setStartValue(self._opacity)
            fade_anim.setEndValue(128)
            fade_anim.setDuration(300)
            fade_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            fade_anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
        except:
            pass


    def _set_opacity(self, value):
        self._opacity = value
        self.repaint()


    def _get_opacity(self):
        return self._opacity
        try:
            _opacity_anim_prop = QtCore.pyqtProperty(int, _get_opacity, _set_opacity)
        except:
            _opacity_anim_prop = QtCore.Property(int, _get_opacity, _set_opacity)


    def _fit_screen_geometry(self):
        # Compute the union of all screen geometries, and resize to fit.
        desktop = QtWidgets.QApplication.desktop()
        workspace_rect = QtCore.QRect()
        for i in range(desktop.screenCount()):
            workspace_rect = workspace_rect.united(desktop.screenGeometry(i))
        self.setGeometry(workspace_rect)


def get_desktop_pixmap(rect):
    desktop = QtWidgets.QApplication.desktop()
    grm = QtGui.QPixmap.grabWindow(int(desktop.winId()), int(rect.x()), int(rect.y()), int(rect.width()), int(rect.height()))
    return grm

screen_capture = ScreenGrabber.screen_capture


def screen_capture_file(output_path=None):
    if output_path is None:
        output_path = tempfile.NamedTemporaryFile(suffix=".png",
                                                  prefix="screencapture_",
                                                  delete=False).name
    pixmap = screen_capture()
    pixmap.save(output_path)
    print("Out {0}".format(output_path))
    return output_path        
    
class Thumbnail(QtWidgets.QLabel):
    try:
        screen_grabbed = QtCore.pyqtSignal(object)
        _do_screengrab = QtCore.pyqtSignal()
        gifCreated = QtCore.pyqtSignal(str)
    except:
        screen_grabbed = QtCore.Signal(object)
        _do_screengrab = QtCore.Signal()
        gifCreated = QtCore.Signal(str)
    thumbBaseDir = "{home}/Temp/publishThumbs".format(home=os.environ["HOME"])
    parent = None

    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        self.setStyleSheet('''QLabel{
                                    background-color: #242424;
                                    color:white;
                                    qproperty-alignment: AlignCenter;
                                    }''')
        #_multiple_values allows to display indicator that the summary thumbnail is not applied to all items
        self._multiple_values = False
        self._thumbnail = None
        self._enabled = True
        self.setAutoFillBackground(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        if sys.platform.count("win"):
            prePath = "Z:/backstage/maya/publisher_v02/icon/"
        else:
            prePath = "/usersetup/linux/module/ui_icons_md/"
        self.camImg = prePath + 'camera.png'
        self._no_thumb_pixmap = QtGui.QPixmap(self.camImg)
        size = QtCore.QSize(1000, 1500)
        self._no_thumb_pixmap = self._no_thumb_pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        # self.update()
        self._do_screengrab.connect(self._on_screengrab)
        self.thumb_file = None
        self.parent = parent


    def setEnabled(self, enabled):
        self._enabled = enabled
        if enabled:
            self.setCursor(QtCore.Qt.PointingHandCursor)
        else:
            self.unsetCursor()


    def set_thumbnail(self, pixmap):
        if pixmap is None:
            self._set_screenshot_pixmap(self._no_thumb_pixmap)
        else:
            self._set_screenshot_pixmap(pixmap)


    def mousePressEvent(self, event):
        QtWidgets.QLabel.mousePressEvent(self, event)
        if self._enabled:
            pass


    def mouseReleaseEvent(self, event):
        QtWidgets.QLabel.mouseReleaseEvent(self, event)
        if self._enabled:
            pos_mouse = event.pos()
            if self.rect().contains(pos_mouse):
                self._do_screengrab.emit()
                 
                
    def _on_screengrab(self):
        self.window().hide()
        try:
            pixmap = ScreenGrabber.screen_capture()
        finally:
            self.window().show()

        if pixmap:
            currentTime = time.localtime(time.time())
            cTime = "{0:0=4}{1:0=2}{2:0=2}{3:0=2}{4:0=2}{5:0=2}".format(currentTime.tm_year
                                                                ,currentTime.tm_mon
                                                                ,currentTime.tm_mday
                                                                , currentTime.tm_hour
                                                                ,currentTime.tm_min
                                                                ,currentTime.tm_sec)
            
            thumbDir = self.thumbBaseDir
            if not os.path.exists(thumbDir):
                os.makedirs(thumbDir)
            self.thumb_file = "{0}/thumb_{1}.png".format(thumbDir, cTime)
            pixmap.save(self.thumb_file)
            self._multiple_values = False
            self._set_screenshot_pixmap(pixmap)
            self.screen_grabbed.emit(pixmap)


    def _set_multiple_values_indicator(self, is_multiple_values):
        self._multiple_values = is_multiple_values


    def paintEvent(self, paint_event):
        # paint multiple values indicator
        if self._multiple_values == True:
            p = QtGui.QPainter(self)
            p.drawPixmap(0,0,self.width(),self.height(),self._no_thumb_pixmap,0,0,self._no_thumb_pixmap.width(),self._no_thumb_pixmap.height())
            p.fillRect(0,0,self.width(),self.height(), QtGui.QColor(42,42,42,237))
        else:
           QtWidgets.QLabel.paintEvent(self, paint_event)


    def _set_screenshot_pixmap(self, pixmap):
        self._thumbnail = pixmap
        thumb = self._thumbnail.scaled(self.width(),
                                       self.height(),
                                       QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)
        self.setPixmap(thumb)
        QtWidgets.QApplication.processEvents()


    def set_thumb_from_path(self, path):    
        pixMap = QtGui.QPixmap(path)
        if not pixMap.isNull():
            self.set_thumbnail(pixMap)
            return None  


    def get_thumb_path(self):
        return self.thumb_file
