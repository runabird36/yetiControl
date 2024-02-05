import os, sys

root_path = os.path.dirname(os.path.abspath( __file__ ))
if root_path not in sys.path:
    sys.path.append(root_path)
root_path = root_path.replace('\\', '/')

path_list = [
                root_path,
                root_path + "/" + "view",
                root_path + "/" + "toolkit",
                root_path + "/" + "model"
            ]
for _path in path_list:
    print(_path)
    if _path in sys.path:
        continue
    sys.path.append(_path)


yeti_icon_path          = root_path + "/" + "icons" + "/" + "yeti_icon.png"
logo_path               = root_path + "/" + "icons" + "/" + "giantLogo.png"

_rigth_arrow            = root_path + "/" + "icons" + '/' + 'right_arrow_resized_33.png'
_rigth_arrow_pressed    = root_path + "/" + "icons" + '/' + 'right_arrow_resized_33_pressed.png'
_left_arrow             = root_path + "/" + "icons" + '/' + 'left_arrow_resized_33.png'
_left_arrow_pressed     = root_path + "/" + "icons" + '/' + 'left_arrow_resized_33_pressed.png'


_down_arrow             = root_path + "/" + "icons" + '/' + 'donw_arrow_resized_29.png'
_down_arrow_pressed     = root_path + "/" + "icons" + '/' + 'donw_arrow_resized_29_pressed.png'
_up_arrow               = root_path + "/" + "icons" + '/' + 'up_arrow_resized_29.png'
_up_arrow_pressed       = root_path + "/" + "icons" + '/' + 'up_arrow_resized_29_pressed.png'



default_samples = "3"




import sys

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