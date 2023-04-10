# -*- coding:utf-8 -*-

from importlib import reload
import PySide2.QtWidgets as QtGui
from . import CQT_path_module
reload(CQT_path_module)

try:
    from .elements import (CQT_trafficlight, CQT_msgbox_collector, CQT_imageChecker, CQT_loadingwidget)
except:
    import traceback
    traceback.print_exc()
reload(CQT_trafficlight)
reload(CQT_msgbox_collector)




def get_trafficlight_widget(parent=None, lightball_size: int=50, light_connected: bool=True, alpha: int=15) -> CQT_trafficlight.trafficLight:
    trafficlight_widget = CQT_trafficlight.trafficLight(parent, lightball_size=lightball_size, alpha=alpha)
    trafficlight_widget.set_connect_light_mode(light_connected)
    return trafficlight_widget


def get_confirm_dialog(_parent=None, title: str="", msg: str="", status: str="clear", btn_list: list=[]):
    """
    In this case,
    CustomConfirmDialog include show() function

    Just, make instance.
    """
    return CQT_msgbox_collector.CustomConfirmDialog(_parent, title, msg, status, btn_list, dialog_dis_type="show")

def get_confirm_dialog_with_exec(_parent=None, title: str="", msg: str="", status: str="clear", btn_list: list=[]):
    """
    In this case,
    CustomConfirmDialog do not include show() function

    first, make instance. and Second, do exec_() fucntion.
    """
    return CQT_msgbox_collector.CustomConfirmDialog(_parent, title, msg, status, btn_list, dialog_dis_type="exec")

def get_ImageChecker(_parent, edge_color: list, brush_color: list) -> QtGui.QWidget:
    return CQT_imageChecker.imageChecker(_parent, edge_color, brush_color)



def get_loadingWidget(_parent=None):
    return CQT_loadingwidget.QtWaitingSpinner(parent=_parent)

def get_loadingDialog(_parent=None):
    return CQT_loadingwidget.loadingDialog(parent=_parent)


def get_animatedCheckbox(_parent :str=""):
    return


