# -*- coding: utf-8 -*-

import os
import sys
if sys.version_info.major == 3:
    from importlib import reload
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')
import time
import maya.cmds as cmds
import maya.mel as mel
import traceback

import TNC_path_module
reload(TNC_path_module)
from model import TNC_yeti
reload(TNC_yeti)
from toolkit import TNC_toolkit
reload(TNC_toolkit)



class TNC():

    def __init__(self, _script_path=''):

        mel.eval('source "{0}"'.format(TNC_path_module._mel_path))

        self.yeti_hub = []
        self.error_list = []

    def init_data(self):
        _yeti_node_list = TNC_toolkit.get_selected_yeti_node()

        for _yeti_node in _yeti_node_list:
            tnc_yeti = TNC_yeti.TNCyeti(_yeti_node)
            self.yeti_hub.append(tnc_yeti)


    def run(self):
        _msg = u'경로 설정 방식 선택'
        _sel_res = cmds.confirmDialog( title='Confirm', message=_msg, button=[u'To 절대 경로',u'To 상대 경로'])


        self.init_data()

        try:
            if _sel_res == u'To 절대 경로':
                self.run_for_absolute()
            elif _sel_res == u'To 상대 경로':
                self.run_for_relatives()
        except Exception as e:
            print(str(e))
            traceback.print_exc()



    def check_print(self):
        for _tnc_yeti in self.yeti_hub:
            print('============================================')
            print(_tnc_yeti.get_yetiname())
            print(_tnc_yeti.get_texnode_list())
            print('=================================')
            for _texnode in _tnc_yeti.get_texnode_list():
                print(_tnc_yeti.get_filename_from_texnode(_texnode))
                print(_tnc_yeti.get_fcount_from_texnode(_texnode))
            print('============================================')
            print('============================================')
            _tnc_yeti.get_shortest_dirpath()



    def print_error(self):
        _error_msg = u''
        for _error in self.error_list:
            _error_msg += u'{0} 예티 노드의 {1} 텍스노드\n'.format(_error[0], _error[1])

        cmds.confirmDialog( title='Error', message=_error_msg)


    def print_complete(self):
        _msg = u'성공!'


        cmds.confirmDialog( title='Complete!!', message=_msg)


    def run_for_absolute(self):
        for _tnc_yeti in self.yeti_hub:
            cur_yeti = _tnc_yeti.get_yetiname()
            _isppath = TNC_toolkit.get_ISPpath(cur_yeti)
            if _isppath is None:
                continue
            _is_clear = True
            for _texnode in _tnc_yeti.get_texnode_list():
                cur_filename_value = _tnc_yeti.get_filename_from_texnode(_texnode)
                if TNC_toolkit.does_exist(cur_filename_value):
                    print('\# TNC Warnning : Exists : {0}'.format(cur_filename_value))
                    continue
                else:
                    _isppath = os.path.realpath(_isppath)
                    cur_fullpath = '{0}/{1}'.format(_isppath, cur_filename_value)
                    if TNC_toolkit.does_exist(cur_fullpath) == False:
                        self.error_list.append((_tnc_yeti.get_yetiname(), _texnode))
                        _is_clear = False
                    # print cur_fullpath
                    cur_fullpath = os.path.realpath(cur_fullpath)
                    if cur_fullpath.count("\\"):
                        cur_fullpath = cur_fullpath.replace('\\', '/')
                    TNC_toolkit.set_tex_filename_in_texnode(cur_yeti, _texnode, cur_fullpath)
                time.sleep(0.8)
            if _is_clear == True:
                TNC_toolkit.set_ISPpath(cur_yeti, '')
        if self.error_list == []:
            self.print_complete()
        else:
            self.print_error()


    def run_for_relatives(self):
        for _tnc_yeti in self.yeti_hub:
            _texnode, _tar_isppath=_tnc_yeti.get_shortest_dirpath()
            if _texnode is None:
                continue
            cur_yeti = _tnc_yeti.get_yetiname()
            _tar_isppath = TNC_toolkit.make_script_path(_tar_isppath)
            for _texnode in _tnc_yeti.get_texnode_list():
                from_filename_value = _tnc_yeti.get_filename_from_texnode(_texnode)

                from_filename_value = TNC_toolkit.make_script_path(from_filename_value)


                if _tar_isppath in from_filename_value:
                    to_filename_value = from_filename_value.replace(_tar_isppath, '')
                else:
                    self.error_list.append((_tnc_yeti.get_yetiname(), _texnode))
                    to_filename_value = from_filename_value

                TNC_toolkit.set_tex_filename_in_texnode(cur_yeti, _texnode, to_filename_value)

                time.sleep(0.8)

            TNC_toolkit.set_ISPpath(cur_yeti, _tar_isppath)


        if self.error_list == []:
            self.print_complete()
        else:
            self.print_error()
