
import sys
from os import path
_module_path = "/usersetup/linux/module"
if _module_path not in sys.path:
    sys.path.append(path.realpath(_module_path))
import maya.cmds as cmds
from maya_md import neon
from PySide2.QtWidgets import (
                                QApplication, QDialog, QHBoxLayout, QVBoxLayout,
                                QLabel, QPushButton, QCheckBox, QFrame, QSpacerItem,
                                QSizePolicy, QRadioButton, QButtonGroup, QMessageBox,
                                QWidget, QTabWidget, QListWidget, QLineEdit, QSpinBox
                            )
from PySide2.QtCore import Qt
from qt_material import apply_stylesheet







def show_msg_box(_msg :str) -> None:
    info_box = QMessageBox()
    info_box.setWindowTitle("ToggleAll")
    info_box.setText(_msg)
    info_box.setStandardButtons(QMessageBox.Ok)
    apply_stylesheet(info_box, "dark_purple.xml")
    info_box.exec_()

def connect_trs(from_node :str, to_node :str) -> None:
    cmds.connectAttr(f"{from_node}.translate", f"{to_node}.translate")
    cmds.connectAttr(f"{from_node}.rotate", f"{to_node}.rotate")
    # cmds.connectAttr(f"{from_node}.scale", f"{to_node}.scale")

def disconnect_trs(from_node :str, to_node :str) -> None:
    cmds.disconnectAttr(f"{from_node}.translate", f"{to_node}.translate")
    cmds.disconnectAttr(f"{from_node}.rotate", f"{to_node}.rotate")
    # cmds.disconnectAttr(f"{from_node}.scale", f"{to_node}.scale")
    cmds.setAttr(f"{to_node}.translateX", 0)
    cmds.setAttr(f"{to_node}.translateY", 0)
    cmds.setAttr(f"{to_node}.translateZ", 0)

    cmds.setAttr(f"{to_node}.rotateX", 0)
    cmds.setAttr(f"{to_node}.rotateY", 0)
    cmds.setAttr(f"{to_node}.rotateZ", 0)

def is_connected(from_node :str, to_node :str) -> bool:
    print(f"{from_node}.translate")
    print(f"{to_node}.translate")
    return neon.is_connected(f"{from_node}.translate", f"{to_node}.translate")



def find_all_yetiGRPs() -> None:
    def get_yeti_trf(root_trf :str) -> str:
        child_list = cmds.listRelatives(root_trf, c=True, f=True)
        for child in child_list:
            if "|yeti" in child:
                return child
        return ""
    def get_anim_trf(root_trf :str) -> str:
        child_list = cmds.listRelatives(root_trf, c=True, f=True)
        for child in child_list:
            if "|geo" in child:
                return cmds.listRelatives(child, c=True, f=True)[0]
        return ""
    
    res_list = []
    all_yetiGRPs = cmds.ls("*_yetiGRP", l=True, type="transform")
    for yetiGRP in all_yetiGRPs:
        yeti_trf = get_yeti_trf(yetiGRP)
        anim_trf = get_anim_trf(yetiGRP)
        # print(f"{anim_trf} -> {yeti_trf}")
        res_list.append((anim_trf, yeti_trf))
    
    return res_list

    

def run(do_connect_all :bool) -> None:
    pair_list = find_all_yetiGRPs()

    if do_connect_all == True:
        for from_node, to_node in pair_list:
            con_res = is_connected(from_node, to_node)
            if con_res == False:
                connect_trs(from_node, to_node)
                
    elif do_connect_all == False:
        for from_node, to_node in pair_list:
            con_res = is_connected(from_node, to_node)
            if con_res == True:
                disconnect_trs(from_node, to_node)
            

        

