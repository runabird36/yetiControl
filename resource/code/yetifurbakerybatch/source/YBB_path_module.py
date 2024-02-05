
import sys, os

SOURCE_PATH     = os.path.dirname(os.path.abspath( __file__ ))
RESOURCE_PATH   = ""


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


def set_resource_path(root_path :str) -> None:
    global RESOURCE_PATH
    os.chdir(root_path)
    os.chdir('..')
    os.chdir('./resource')
    RESOURCE_PATH = os.getcwd()
    os.chdir(root_path)


set_resource_path(SOURCE_PATH)



FOLDER_IMG                     = os.path.join(RESOURCE_PATH, "icons") + '/' + 'folder_img.png'
YETI_IMG                       = os.path.join(RESOURCE_PATH, "icons") + '/' + 'pgYeti_icon.png'
DROP_FOLDER_IMG                = os.path.join(RESOURCE_PATH, "icons") + '/' + 'drop_folder_img.png'
MAYA_IMG                       = os.path.join(RESOURCE_PATH, "icons") + '/' + 'mayaico.png'

LOADING_GIF                    = os.path.join(RESOURCE_PATH, "icons") + '/' + 'status_loading.gif'
CLEAR_GIF                      = os.path.join(RESOURCE_PATH, "icons") + '/' + 'status_clear.gif'
ERROR_GIF                      = os.path.join(RESOURCE_PATH, "icons") + '/' + 'status_error_alpha.gif'
WARNNING_GIF                   = os.path.join(RESOURCE_PATH, "icons") + '/' + 'status_warnning02.gif'



BAKE_FUR_PROCESS_SCRIPT        = os.path.join(SOURCE_PATH, "toolkit") + '/' + 'YBB_bakefur_process.py' 
PYTHON_COMPILER_PATH           = "/usersetup/linux/python/py39/bin/python3.9"

if is_linux() == True:
    MAYA_EXE_PATH              = "/usr/autodesk/maya/bin/maya"
else:
    MAYA_EXE_PATH              = ""

