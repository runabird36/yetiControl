import sys
import os
from tempfile import gettempdir
from random import randint
script_path = os.path.dirname(os.path.abspath( __file__ ))
# _main_path = "Z:/backstage/multi/GiantSubmitter"
print("\n\n\n===========================\n\nCurrent script path : {0}\n\n===========================\n\n\n".format(script_path))
script_path = script_path.replace('\\', '/')
_main_path = script_path


_quesion_icon = _main_path + '/icon/question_mark_v03.png'
_no_image_icon = _main_path + '/icon/no_image_icon.png'


_atx_tool_path = os.path.dirname(_main_path) + "/ATXarnoldattr2"

# sys.path.append(_main_path+'/MTX_dialog')

def get_thumb_path(_prj_name, _pub_id):
    # return '/usersetup/linux/scripts/general_sc/loader/prj_json/{0}/publishFiles/{1}.png'.format(_prj_name, _pub_id)
    return '/usersetup/linux/shotgrid_DB/sg_thumbnails/projects/{0}/publishFiles/{1}.png'.format(_prj_name, _pub_id)


# HAIR_STEP_PROJECTS_LIST = ['2022_09_pipelineEDU2', '2023_01_mov2']



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

theme_idx = randint(0, int(len(theme_list)/2))
dark_theme_idx = randint(0, len(dark_theme_list)-1)

cur_theme = dark_theme_list[dark_theme_idx]
# theme_idx = 1
