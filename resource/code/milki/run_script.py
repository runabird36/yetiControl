

import sys

for _path in sys.path:
    if "/milki/" in sys.path:
        sys.path.remove(_path)

import site

cur_path = "/home/taiyeong.song/Desktop/pipeTemp/milki"
site.addsitedir(cur_path)
import sys
if sys.version_info.major == 3:
    from importlib import reload
import milki
reload(milki)
milki.main('MAYA')