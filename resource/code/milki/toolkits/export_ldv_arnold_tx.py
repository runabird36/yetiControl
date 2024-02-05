
import subprocess, os, pprint, time, shutil
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
import maya.cmds as cmds

import ui_progressbar
# reload(ui_progressbar)
import tempfile
temp_dir = tempfile.gettempdir()

def get_cmd_template():
    _maya_ver = cmds.about(v=True)
    if _maya_ver == '2018':
        sRGB_cmd_template = '/usr/autodesk/arnold/maya' + str(os.environ["MAYA_VERSION"]) + '/bin/maketx -v -u --unpremult --oiio --colorconvert sRGB linear {0} -o {1}'
        cmd_template = '/usr/autodesk/arnold/maya' + str(os.environ["MAYA_VERSION"]) + '/bin/maketx -v -u --unpremult --oiio {0} -o {1}'
    else:
        sRGB_cmd_template = '/usr/autodesk/arnold/maya' + str(os.environ["MAYA_VERSION"]) + '/bin/maketx -v -u --unpremult --oiio --colorconvert sRGB linear {0} -o {1}'
        cmd_template = '/usr/autodesk/arnold/maya' + str(os.environ["MAYA_VERSION"]) + '/bin/maketx -v -u --unpremult --oiio {0} -o {1}'
    return sRGB_cmd_template, cmd_template

def maketx_with_cmd(pub_target_tex_full_path_list):
    global temp_dir

    # setting progressbar
    backup_progressbar_window = ui_progressbar.Ui_ProgressbarUI()
    progress_title = 'Baking Tx......'
    backup_progressbar_window.progress_window.setWindowTitle(progress_title)
    backup_progressbar_window.blackhole_pb.setValue(0)


    item_list = []

    item_list = pub_target_tex_full_path_list
    item_total_count = len(item_list)

    _count = 1
    before_percentage = 1
    for item in item_list:
        tex_full_path = item[0]
        file_node = item[1]
        tar_colorspace = cmds.getAttr('{0}.colorSpace'.format(file_node))
        # update progressbar
        percentage = float(_count)/float(item_total_count)*100
        for i in range(int(before_percentage), int(percentage)+1):

            backup_progressbar_window.blackhole_pb.setValue(int(i))
            QtGui.QApplication.processEvents()
            time.sleep(0.03)
        before_percentage = percentage
        _count += 1

        # item is each tex pub full path
        # change file format to .tx
        # and make maktetx cmd
        if os.path.isfile(tex_full_path):
            from_tex_full_path = tex_full_path
            fname, ext = os.path.splitext(tex_full_path)
            to_tex_full_path = tex_full_path.replace(ext, '.tx')
            to_tex_fname = os.path.basename(to_tex_full_path)
            temp_to_path = "{0}/{1}".format(temp_dir, to_tex_fname)

            sRGB_cmd_template, cmd_template = get_cmd_template()
            print(cmd_template)
            if tar_colorspace == 'sRGB':
                maketx_cmd = sRGB_cmd_template.format(from_tex_full_path, temp_to_path)
            else:
                maketx_cmd = cmd_template.format(from_tex_full_path, temp_to_path)
            subprocess.Popen(maketx_cmd, shell=True, stdout=subprocess.PIPE).stdout.read()


            shutil.move(temp_to_path, to_tex_full_path)
