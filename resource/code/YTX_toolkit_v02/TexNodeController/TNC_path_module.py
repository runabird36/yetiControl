# -*- coding:utf-8 -*-

import sys
import os
script_path = os.path.dirname(os.path.abspath( __file__ ))
print("\n\n\n===========================\n\nCurrent script path : {0}\n\n===========================\n\n\n".format(script_path))
if script_path.count("\\"):
    script_path = script_path.replace('\\', '/')
_main_path = script_path
sys.path.append(_main_path+'/model')
sys.path.append(_main_path+'/toolkit')
_mel_path = _main_path+'/toolkit/TNC_yeti_toolkit.mel'
