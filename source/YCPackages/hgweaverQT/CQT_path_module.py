

import os, sys
from random import randint
script_path = os.path.dirname(os.path.abspath( __file__ ))
if "\\" in script_path:
    script_path = script_path.replace('\\', '/')

if script_path not in sys.path:
    sys.path.append(script_path)

check_img       = script_path + "/icons/check_img.png"
warnning_img    = script_path + "/icons/warning.png"
error_img       = script_path + "/icons/error_img_resize.png"


dragdrop_img    = script_path + "/icons/dragdrop_img04.png"
dragdrop_img_w  = 128
dragdrop_img_h  = 128



dark_theme_list = ['dark_amber.xml',
                    'dark_blue.xml',
                    'dark_cyan.xml',
                    'dark_lightgreen.xml',
                    'dark_pink.xml',
                    'dark_purple.xml',
                    'dark_red.xml',
                    'dark_teal.xml',
                    'dark_yellow.xml']
light_theme_list = [
                    'light_amber.xml',
                    'light_blue.xml',
                    'light_cyan.xml',
                    'light_cyan_500.xml',
                    'light_lightgreen.xml',
                    'light_pink.xml',
                    'light_purple.xml',
                    'light_red.xml',
                    'light_teal.xml',
                    'light_yellow.xml'
                    ]
theme_list = dark_theme_list + light_theme_list






def get_theme() -> str:
    global theme_list
    global dark_theme_list

    theme_idx = randint(0, int(len(theme_list)/2))
    dark_theme_idx = randint(0, len(dark_theme_list)-1)

    return "dark_blue.xml"