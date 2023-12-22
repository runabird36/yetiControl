from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class RoundCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super(RoundCheckBox, self).__init__(parent)
        self.setCheckable(True)
        self.setStyleSheet('''
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
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

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(QColor(255, 255, 255))
    #     painter.drawEllipse(1, 1, 18, 18)
    #     if self.isChecked():
    #         painter.setBrush(QColor(0, 255, 0))
    #     else:
    #         painter.setBrush(QColor(255, 0, 0))
    #     painter.drawEllipse(4, 4, 12, 12)
    #     painter.end()

if __name__ == '__main__':
    app = QApplication([])
    widget = QWidget()
    checkbox = RoundCheckBox(widget)
    checkbox.setGeometry(50, 50, 50, 50)
    widget.show()
    app.exec_()
