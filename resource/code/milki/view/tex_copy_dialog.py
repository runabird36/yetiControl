import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
import os

class TexCopyDialog(QtGui.QDialog):
    copy_tree = None
    items = []
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.main_vboxlayout = QtGui.QVBoxLayout(self)

        self.main_vboxlayout.setMargin(0)
        self.setMinimumSize(QtCore.QSize(500, 100))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.copy_tree = QtGui.QTreeWidget(self)
        self.copy_tree.setHeaderLabels(['file', 'size', 'status'])
        self.copy_tree.setColumnWidth(0,280)
        self.copy_tree.setColumnWidth(1,100)
        self.copy_tree.setColumnWidth(1,80)
        #self.title_vboxlayout.setAlignment(self.title_btn, QtCore.Qt.AlignCenter)
        self.main_vboxlayout.addWidget(self.copy_tree)

    def clear_items(self):
        self.copy_tree.clear()

    def add_item(self, src, file_path):
        file_name = os.path.basename(file_path)
        file_size = self.conv_byte(os.path.getsize(src))

        copy_item = QtGui.QTreeWidgetItem(self.copy_tree)
        copy_item.setText(0, file_name)
        copy_item.setText(1, file_size)
        copy_item.setText(2, "copying...")
        copy_item.setForeground(2, QtGuiOrig.QBrush(QtGuiOrig.QColor('#e8d210')))
        self.items.append(copy_item)

    def change_item(self, idx, res):
        item = self.items[idx]
        if res == True:
            item.setText(2, "complete")
            item.setForeground(2, QtGuiOrig.QBrush(QtGuiOrig.QColor('#21ce60')))
        else:
            item.setText(2, "error")
            item.setForeground(2, QtGuiOrig.QBrush(QtGuiOrig.QColor('#ba2116')))



    def conv_byte(self, B):
        'Return the given bytes as a human friendly KB, MB, GB, or TB string'
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2) # 1,048,576
        GB = float(KB ** 3) # 1,073,741,824
        TB = float(KB ** 4) # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} kb'.format(B/KB)
        elif MB <= B < GB:
            return '{0:.2f} mb'.format(B/MB)
        elif GB <= B < TB:
            return '{0:.2f} gb'.format(B/GB)
        elif TB <= B:
            return '{0:.2f} tb'.format(B/TB)
