import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
import shutil, time, os, pprint, subprocess
import maya.cmds as cmds

import tex_copy_dialog
#reload (tex_copy_dialog)


class TexCopier (QtCore.QObject):
    all_complete = QtCore.Signal()
    job_infos = []
    copiers = []
    copy_dialog = None
    total_num = 0

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.copy_dialog = tex_copy_dialog.TexCopyDialog()

    def clear_jobs(self):
        self.job_infos = []

    def add_job(self, src, dst, tex, is_udim):
        job = {'src' : src, 'dst' : dst, 'tex' : tex, 'is_udim': is_udim}
        self.job_infos.append(job)

    def start_copy(self):
        # self.copy_dialog.clear_items()
        # pprint.pprint(self.job_infos)
        if self.job_infos == []:
            print('There are no jobs. Just to go post_execute')
            self.copy_dialog.hide()
            self.all_complete.emit()
        else:
            print('There are jobs. execute copying')
            for idx, info in enumerate(self.job_infos):
                copier = Copier(info['src'], info['dst'], idx)
                copier.complete.connect(self.copy_complete)
                self.copiers.append(copier)
                self.copy_dialog.add_item(info['src'], info['dst'])
                copier.start()
                self.total_num += 1
            self.copy_dialog.show()

    def copy_complete(self, idx, res, copier):
        print("======================================================")
        print("copy target : {0} ".format(self.job_infos[idx]['dst']))
        print("copy result : {0} ".format(res))

        if copier in self.copiers:
            copier.terminate()
            self.copiers.remove(copier)
        if res == True:
            info = self.job_infos[idx]
            self.change_tex_path(info['tex'], info['dst'], info['is_udim'])

        self.total_num -= 1
        self.copy_dialog.change_item(idx, res)
        if self.total_num <= 0:
            self.copy_dialog.hide()
            self.all_complete.emit()




    def change_tex_path(self, tex_node, path, is_udim = False):
        attr_list = cmds.listAttr(tex_node)
        tex_attr= ''
        if 'fileTextureName' in attr_list:
            tex_attr = tex_node + '.' + 'fileTextureName'
        elif 'filename' in attr_list:
            tex_attr = tex_node + '.' + 'filename'

        if is_udim == True:
            path_splits = path.split('.')
            path_splits[-2] = '<UDIM>'
            path = '.'.join(path_splits)

        cmds.setAttr(tex_attr, path, type = "string")

class Copier(QtCore.QThread):

    idx = None
    src = None
    dst = None
    complete = QtCore.Signal(int, bool, object)
    # robocopy_cmd_template = 'robocopy {0} {1} /MIR /E /W:2 /R:3 /REG /MT:8'
    def __init__(self, src, dst, idx):
        QtCore.QThread.__init__(self)
        self.src = src
        self.dst = dst
        self.idx = idx

    def run(self):
        try:
            shutil.copy2(self.src, self.dst)
            self.complete.emit(self.idx, True, self)
        except Exception as e:
            print(str(e))
            self.complete.emit(self.idx, False, self)
