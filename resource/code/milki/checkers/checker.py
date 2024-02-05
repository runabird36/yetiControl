import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui

import basic_item
# reload (basic_item)
from basic_item import BasicItem

class Checker(BasicItem):

    warnings = []
    normals = []

    def __init__(self):
        print('check init')

        self.set_type("Checker")


    def add_warnning(self, target, message, status, sel_target = None):
        panel = self.get_panel()
        if panel is None:
            return
        res_item = panel.add_item(target, message, status)

        if sel_target:
            res_item.setWhatsThis(0, sel_target)

    def add_clear_item(self, target, message, sel_target = None):
        panel = self.get_panel()
        if panel is None:
            return

        res_item = panel.add_item(target, message, 'error')

        if sel_target:
            res_item.setWhatsThis(0, sel_target)

    def add_item(self, target, message, status, sel_target = None):
        panel = self.get_panel()
        if panel is None:
            return

        res_item = panel.add_item(target, message, status)

        if sel_target:
            res_item.setWhatsThis(0, sel_target)

    def add_items(self, error_list):
        panel = self.get_panel()
        if panel is None:
            return
        panel.add_items(error_list)


    def is_all_clear(self):
        raise NotImplementedError("is_all_clear is must to be implemented")

    def execute(self, targets):
        raise NotImplementedError("execute is must to be implemented")
