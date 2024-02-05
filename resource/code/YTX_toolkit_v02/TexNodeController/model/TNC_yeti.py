# -*- coding:utf-8 -*-

import os
import sys
if sys.version_info.major == 3:
    from importlib import reload
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
from toolkit import TNC_toolkit
reload(TNC_toolkit)


class TNCyeti():
    def __init__(self, _yeti=''):
        self.DATA_HUB = {}
        self._YETI = _yeti
        self.texnode_list = TNC_toolkit.get_texnode_list_from_yeti(self._YETI)

        for _texnode in self.texnode_list:
            _filename = TNC_toolkit.get_tex_file_name_from_texnode(self._YETI, _texnode)
            _filename_count = len(_filename)
            self.DATA_HUB[_texnode] = {'file_name':_filename, 'flength':_filename_count}





    def get_yetiname(self):
        return self._YETI


    def get_texnode_list(self):
        return self.texnode_list


    def get_filename_from_texnode(self, _texnode):
        cur_texnode = self.DATA_HUB.get(_texnode)
        if cur_texnode is None:
            print('Error : Is not right texnode name from {0} Yeti node'.format(self._YETI))
            return ''
        return cur_texnode.get('file_name')


    def get_fcount_from_texnode(self, _texnode):
        cur_texnode = self.DATA_HUB.get(_texnode)
        if cur_texnode is None:
            print('Error : Is not right texnode name from {0} Yeti node'.format(self._YETI))
            return ''
        return cur_texnode.get('flength')


    def get_shortest_dirpath(self):
        _check_int = 0
        _cur_texnode = ''
        _do_start = False
        if self.get_texnode_list() == []:
            return None, None
        for _texnode in self.get_texnode_list():
            if _check_int == 0 and _do_start == False:
                _do_start = True
                _check_int = self.get_fcount_from_texnode(_texnode)
                _cur_texnode = _texnode
                continue
            else:
                if _check_int > self.get_fcount_from_texnode(_texnode):
                    _check_int = self.get_fcount_from_texnode(_texnode)
                    _cur_texnode = _texnode
                    continue
                else:
                    continue
        if _check_int == 0:
            return None, None
        else:
            _ISPath = self.get_filename_from_texnode(_cur_texnode)
            

            if TNC_toolkit.does_exist(_ISPath) == True:
                return _cur_texnode, os.path.dirname(_ISPath)
            else:
                # already the texnode has relatives path
                return None, None
