


import os, sys
from PyQt5.QtWidgets import QApplication
sys.path.append(os.getcwd())
from source.YCPackages.hgweaverQT import core
app = QApplication(sys.argv)
loading = core.get_loadingDialog()
loading.show()
loading.start_anim()

app.exec_()