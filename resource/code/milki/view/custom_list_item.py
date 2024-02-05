
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
import functools
from functools import partial
from importlib import reload
from traceback import print_exc

import ui_selector_custom_list_item
reload (ui_selector_custom_list_item)

import ui_exporter_custom_list_item
reload (ui_exporter_custom_list_item)

class CustomListItem(QtGui.QListWidgetItem):
    def __init__(self, parent, item_type, item_info, idx):

        super(CustomListItem, self).__init__(parent)

        
        if item_type == 'selector':
            self.selector_item_ui = ui_selector_custom_list_item.QCustomQWidget(item_info)
            self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
            self.listWidget().setItemWidget(self, self.selector_item_ui)
            self.setSizeHint(self.selector_item_ui.sizeHint())    
            # self.selector_item_ui.rm_click.connect(self.remove_item)

        elif item_type == 'exporter':
            self.exporter_item_ui = ui_exporter_custom_list_item.QCustomQWidget(item_info)
            self.setFlags(QtCore.Qt.NoItemFlags)
            self.listWidget().setItemWidget(self, self.exporter_item_ui)
            self.setSizeHint(self.exporter_item_ui.sizeHint())


    
    # def remove_item(self):
    #     list_widget = self.listWidget()
    #     if list_widget.count() < 2:
    #         return
    #     try:
    #         cursor = QtGuiOrig.QCursor()
    #         point = list_widget.mapFromGlobal(cursor.pos())
    #         item = list_widget.itemAt(point)
    #         idx  = list_widget.indexFromItem(item).row()
    #         list_widget.takeItem(idx)
    #     except Exception as e:
    #         print(str(e))

    def get_ui(self):
        return self._item_ui

    def get_label_text(self, item_type):
        if item_type == 'selector':
            return self.selector_item_ui.file_name_label.text()
        elif item_type == 'exporter':
            return self.exporter_item_ui.file_name_label.text()

    def set_label_text(self, file_name):
        self.exporter_item_ui.file_name_label.setText(file_name)

    def set_thumb(self, thumb):
        self.exporter_item_ui.file_format_icon_label.setPixmap(thumb)
