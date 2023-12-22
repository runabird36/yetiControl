
import maya.cmds as cmds
from maya_md import neon
from PySide2.QtWidgets import QMessageBox
from qt_material import apply_stylesheet



def show_msg_box(_msg :str) -> None:
    info_box = QMessageBox()
    info_box.setWindowTitle("Toggle")
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
