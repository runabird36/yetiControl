import maya.mel as mel
import maya.cmds as cmds
from os import path, environ
from shutil import copy2


__TOOL_NAME__ = "Library Updater"

def run_update() -> None:
    global __TOOL_NAME__
    if environ.get("HGWEAVER_YETI_SHELVES") == None:
        cmds.confirmDialog(title=__TOOL_NAME__, message="The \"HGWEAVER_YETI_SHELVES\" enviroment variable not exists")
        return


    shelf_dir = mel.eval("getShelfDir;")
    shelf_dir = shelf_dir.replace("\\", "/")



    from_yeti_fullpath  = shelf_dir + "/" + "shelf_HG_yeti.mel"
    to_yeti_dirpath     = path.abspath(environ["HGWEAVER_YETI_SHELVES"])

    copy2(from_yeti_fullpath, to_yeti_dirpath)


    cmds.confirmDialog(title=__TOOL_NAME__, message="Update Plugin Complete !")

