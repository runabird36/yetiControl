



from importlib import reload
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui
import maya.cmds as cmds
from functools import partial
import yaml
from source.YCPackages.hgweaverQT import core
from source.YCPackages.qt_material import apply_stylesheet
from source.milki.view import YC_milki_main_view
from source.milki.toolkit import (YC_checker, YC_exporter)
from source.YC_core_module import (__CUR_THEME__, __HGWEAVER_YETI_ROOT__, get_workspace_dir)
reload(YC_milki_main_view)
reload(YC_checker)
reload(YC_exporter)

def load_yaml_file(yaml_path):
        try:
            with open(yaml_path) as f:
                load_yml = yaml.safe_load(f)
            return load_yml
        except Exception as e:
            print(str(e))
            return

def dump_to_yaml(info, yaml_path):
    try:
        with open(yaml_path, "w") as f:
            yaml.dump(info, f)
    except Exception as e:
        print(str(e))
    return

def _maya_main_window():
   '''
   Get the maya main window as a QMainWindow instance
   '''
   import maya.cmds as cmds
   import maya.OpenMayaUI as mui
   from shiboken2 import wrapInstance
   ptr = mui.MQtUtil.mainWindow()
   if ptr is not None:
        return wrapInstance(int(ptr),QtGui.QWidget)
   

class YCMilkiController(QtGui.QMainWindow):
    def __init__(self):
        window_parent = _maya_main_window()
        QtGui.QMainWindow.__init__(self, window_parent)
        
        self._ui = YC_milki_main_view.Ui_YC_main_view()
        
        
        
        


    def set_ui(self):
        self._ui.setupUi(self)
        self._ui.init_anim()
        pass


    def set_link(self) -> None:
        self._ui.YC_pub_cancel_btn.clicked.connect(self.close)
        self._ui.YC_pub_check_contents_lw.itemDoubleClicked.connect(self.set_error_view)
        self._ui.YC_pub_check_contents_lw._CHECK_CONVETION_SIGNAL_.connect(self.check_convention)
        self._ui.YC_check_log_contents_lw.itemClicked.connect(self.select_node)
        self._ui.YC_pub_path_info_set_btn.clicked.connect(self.set_pub_path)
        self._ui.YC_pub_update_btn.clicked.connect(self.update_pub_info)
        self._ui.YC_publish_btn.clicked.connect(self.publish_data)
    
    def init_data(self) -> None:
        sel_res = cmds.ls(sl=True)
        if sel_res:
            self.cur_target = sel_res[0]
            self.cur_assetname = self.cur_target.split("_")[0]
        else:
            cmds.confirmDialog(title="Milki", message="There is no Asset Selection!")
            return None
        self._ui.set_assetname(self.cur_assetname)
        self._ui.set_variantname()
        self._ui.set_vernum()

        name_check_log = YC_checker.check_yeti_components_name_convention()
        self._ui.set_log_item_info("Name", name_check_log)

        tex_check_log = YC_checker.check_texture_path_convention()
        self._ui.set_log_item_info("Texture", tex_check_log)

        # set init pub dir
        start_dir = get_workspace_dir()
        self._ui.set_pub_path(start_dir)

        # set Exporter pre-execute
        self.cfx_export_engine = YC_exporter.CFXExporter()
        
        self.update_pub_info()
        

        return True
    
    def show_ui(self):
        try:
            apply_stylesheet(self, theme=__CUR_THEME__)
        except:
            import traceback
            traceback.print_exc()
        self.show()
        pass

    def run(self):
        self.set_ui()
        self.set_link()
        init_res = self.init_data()
        if init_res == None:
            return
        self.show_ui()

    def check_convention(self, _item :QtGui.QListWidgetItem):
        cmds.select(cl=True)
        cmds.select(self.cur_target)
        check_item_contents = _item.data(QtCore.Qt.UserRole)
        check_title = check_item_contents[0]
        self._ui.YC_pub_check_contents_lw.clear()
        if check_title == "Name":
            name_check_log = YC_checker.check_yeti_components_name_convention()
            # self._ui.set_log_item_info(check_title, name_check_log)
            self._ui.update_check_item_view(check_title, name_check_log)
            self._ui.set_error_view(check_title, name_check_log)
        if check_title == "Texture":
            tex_check_log = YC_checker.check_texture_path_convention()
            # self._ui.set_log_item_info(check_title, tex_check_log)
            self._ui.update_check_item_view(check_title, tex_check_log)
            self._ui.set_error_view(check_title, name_check_log)
        

    def set_error_view(self, _item :QtGui.QListWidgetItem) -> None:
        cur_item_contents = _item.data(QtCore.Qt.UserRole)
        check_title = cur_item_contents[0]
        check_logs  = cur_item_contents[2]
        print(check_logs)
        self._ui.set_error_view(check_title, check_logs)
        self._ui.start_anim(check_title)
        return
    
    def select_node(self, _selected_log_item :QtGui.QListWidgetItem) -> None:
        cmds.select(_selected_log_item.whatsThis())

    def set_pub_path(self, _status) -> None:
        start_dir = get_workspace_dir()
        if get_workspace_dir:
            dir_path = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", start_dir)
        else:
            dir_path = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")

        if dir_path:
            self._ui.set_pub_path(dir_path)
        return
    
    def update_pub_info(self) -> None:
        pub_items = self.cfx_export_engine.pre_execute(self.cur_target,
                                                        self._ui.get_variantname(),
                                                        self._ui.get_vernum(),
                                                        self._ui.get_pub_dirname())
        self._ui.set_pub_item_view(pub_items)

    def publish_data(self) -> None:
        thumb_path      = self._ui.get_thumbpath()
        desc            = self._ui.get_desc()
        
        export_info = self.cfx_export_engine.execute(thumb_path, desc)
        
        yaml_hub_path   = export_info.get("SEARCH_PATH") + "/" + "{0}_cfx_hub.yaml".format(self.cur_assetname)
        dump_to_yaml(export_info, yaml_hub_path)

        self.complete_dialog = core.get_confirm_dialog_with_exec(title="Milki", msg="Publish Complete!", btn_list=["Ok"])
        self.complete_dialog.exec_()
        
    def mousePressEvent(self, event) -> None:
        self.origin_pos = event.pos()

        focused_widget = QtGui.QApplication.focusWidget()
        if focused_widget == None:
            return super().mousePressEvent(event)
        if isinstance(focused_widget, QtGui.QListWidget):
            # focused_widget.clear()
            focused_widget.clearSelection()
        # elif isinstance(focused_widget, QtGui.QMainWindow):
        #     self._ui.clear_info_view()
        # elif isinstance(focused_widget, QtGui.QLineEdit):
        #     focused_widget.setText("")
        else:
            focused_widget.clearFocus()
            
        return 
    
    def mouseMoveEvent(self, event) -> None:
        m_x = event.pos().x()
        m_y = event.pos().y()

        x_bias = (m_x-self.origin_pos.x())
        y_bias = (m_y-self.origin_pos.y())

        self.move(self.pos().x() + x_bias, self.pos().y() + y_bias)
        return