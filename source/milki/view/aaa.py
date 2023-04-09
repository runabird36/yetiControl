from PyQt5.QtGui import QPainter, QBrush, QPen, QImage, QPixmap, QPainterPath, QRegion
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
import sys

class CircularLabel(QLabel):
    def __init__(self, parent=None):
        super(CircularLabel, self).__init__(parent)
        self.setFixedSize(100, 100)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw a circle
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(self.rect())
        
        # Draw the label's pixmap on top of the circle
        if not self.pixmap():
            return
        pixmap = self.pixmap().scaled(self.size(), Qt.KeepAspectRatioByExpanding, transformMode=Qt.SmoothTransformation)
        painter.setClipPath(painter.clipPath().intersected(self.shape()))
        painter.drawPixmap(self.rect(), pixmap)
        
    def shape(self):
        # Return the shape of the circle
        path = QPainterPath()
        path.addEllipse(self.rect())
        return path
    
    def setPixmap(self, pixmap):
        # Crop the pixmap to the shape of the circle
        mask = QBitmap(self.size())
        mask.clear()
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(self.rect())
        mask = mask.toImage().convertToFormat(QImage.Format_ARGB32)
        image = pixmap.toImage().convertToFormat(QImage.Format_ARGB32)
        image.setAlphaChannel(mask.createHeuristicMask())
        pixmap = QPixmap.fromImage(image)
        super(CircularLabel
