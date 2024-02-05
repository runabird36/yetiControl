
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui


def _maya_main_window():
   '''
   Get the maya main window as a QMainWindow instance
   '''
   import maya.cmds as cmds
   import maya.OpenMayaUI as mui
   from shiboken2 import wrapInstance
   ptr = mui.MQtUtil.mainWindow()
   if ptr is not None:
        return wrapInstance(int(ptr),QtGui.QWidget)



def _nuke_main_window():
    """Returns Nuke's main window"""
    for obj in QtGui.qApp.topLevelWidgets():
        if (obj.inherits('QMainWindow') and
                obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
            return obj
    else:
        raise RuntimeError('Could not find DockMainWindow instance')


def _houdini_main_window():
    return None

def get_parent(app_name):
    """Returns Nuke's main window"""
    parent = None
    if app_name == 'MAYA':
        parent = _maya_main_window()
    elif app_name == 'NUKE':
        parent = _nuke_main_window()
    elif app_name == 'HOUDINI':
        parent = _houdini_main_window()
    else: 
        return
    return parent

