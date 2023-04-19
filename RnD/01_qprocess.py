
import os, sys
sys.path.append(os.getcwd())



from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget)
from PyQt5.QtCore import QProcess
import sys
from source.YCPackages.hgweaverQT import core

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.btn = QPushButton("Execute")
        self.btn.pressed.connect(self.start_process)
        self.btn_close = QPushButton("Cancel")
        self.btn_close.pressed.connect(self.finish_process)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        l = QVBoxLayout()
        l.addWidget(self.btn)
        l.addWidget(self.btn_close)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)



    def start_process(self):
        # We'll run our process here.
        self.p = QProcess()
        self.p.start("C:/Python39/python.exe", [os.getcwd()+"/RnD/dummy_script.py"])

    def finish_process(self):
        self.p.close()

app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()