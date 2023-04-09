
from maya.cmds import ls, workspace
from os import environ, path
import sys




__PUB_PATH_TEMPLATE__       = "{input_dirpath}/{pub_ext}/{assetname}_cfx.{pub_ext}"
__CUR_THEME__               = "dark_blue.xml"
__HGWEAVER_YETI_ROOT__      = (path.realpath(environ["HGWEAVER_YETI_ROOT"])).replace("\\", "/")
__HGWEAVER_RESOURCE_PATH__  = __HGWEAVER_YETI_ROOT__ + "/" + "resource"



# image path
cam_img = __HGWEAVER_RESOURCE_PATH__ + "/" + "icons" + "/" + "camera.png"



def is_windows(platform=None):
    """
    Determine if the current platform is Windows.

    :param platform: sys.platform style string, e.g 'linux2', 'win32' or
                     'darwin'.  If not provided, sys.platform will be used.

    :returns: True if the current platform is Windows, otherwise False.
    :rtype: bool
    """
    if platform:
        return platform == "win32"
    return sys.platform == "win32"

def is_linux(platform=None):
    """
    Determine if the current platform is Linux.

    :param platform: sys.platform style string, e.g 'linux2', 'win32' or
                     'darwin'.  If not provided, sys.platform will be used.

    :returns: True if the current platform is Linux, otherwise False.
    :rtype: bool
    """
    if platform:
        return platform.startswith("linux")
    return sys.platform.startswith("linux")

def is_macos(platform=None):
    """
    Determine if the current platform is MacOS.

    :param platform: sys.platform style string, e.g 'linux2', 'win32' or
                     'darwin'.  If not provided, sys.platform will be used.

    :returns: True if the current platform is MacOS, otherwise False.
    :rtype: bool
    """
    if platform:
        return platform == "darwin"
    return sys.platform == "darwin"


def get_open_dir_cmd() -> str:
    if is_linux() == True:
        return "nautilus"
    elif is_windows() == True:
        return "explorer.exe"

def set_path_env() -> None:
    global __HGWEAVER_YETI_ROOT__
    sys_path_list = [__HGWEAVER_YETI_ROOT__+"/"+"source"+"/"+"YCPackages"]
    for _path in sys_path_list:
        sys.path.append(_path)



def get_workspace_dir() -> str:
    return workspace(q=True, fullName=True)

def get_assetname(input_name :str="") -> str:
    _assetname = ""
    if input_name == "":
        selected_tars = ls(sl=True)
        if not selected_tars:
            return ""
        _assetname = selected_tars[0].split("_")[0]
    else:
        _assetname = input_name.split("_")[0]
    return _assetname






def get_pub_paths(input_dir :str, assetname :str, pub_ext :str) -> str:
    global __PUB_PATH_TEMPLATE__
    if "." in pub_ext:
        pub_ext = pub_ext.replace(".", "")
    
    pub_fullpath = __PUB_PATH_TEMPLATE__.format(
                                                    input_dirpath   = input_dir,
                                                    pub_ext         = pub_ext,
                                                    assetname       = assetname
                                                )
    return pub_fullpath


set_path_env()