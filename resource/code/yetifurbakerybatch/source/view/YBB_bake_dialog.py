from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog,
                                QVBoxLayout, QHBoxLayout, QWidget, QProgressBar, QLabel, QLineEdit,
                                QListWidget, QListWidgetItem, QSizePolicy, QSpacerItem, QWidget,
                                QComboBox, QAbstractItemView, QMenuBar, QMenu, QAction, QDialog,
                                QTextBrowser, QDesktopWidget, QGridLayout, QSpinBox, QCheckBox)
from PyQt5.QtCore import (QProcess, Qt, QMetaObject, QSize, QRect, pyqtSignal, qDebug)
from PyQt5.QtGui import (QDragEnterEvent, QDragMoveEvent, QDropEvent, QPaintEvent, QIcon, QCursor,
                            QPainter, QColor, QBrush, QPen, QImage, QFont, QPixmap, QWindow, QMovie, qRgb)
import sys
import re
import os
import datetime, time
from pprint import pprint
from functools import partial
from qt_material import apply_stylesheet
from json import dumps, loads

check_path = os.path.dirname(os.path.dirname(os.path.abspath( __file__ )))
if check_path not in sys.path:
    sys.path.append(check_path)


from YBB_path_module import (FOLDER_IMG, DROP_FOLDER_IMG, MAYA_IMG, YETI_IMG,
                             LOADING_GIF, CLEAR_GIF, ERROR_GIF, WARNNING_GIF)


from toolkit.YBB_py_toolkit import ProcessPool



class ProcessMSG(QDialog):
    def __init__(self, _parent=None) -> None:
        super(ProcessMSG, self).__init__(_parent)
        self.setupUi()

    def setupUi(self) -> None:
        
        self.main_msg_view = QTextBrowser()
        self.main_msg_view.setText("")

        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.main_msg_view)


        self.setLayout(self.main_vl)
        self.setWindowTitle("Process message")
        self.resize(320, 270)

    def set_msg(self, input_msg :str) -> None:
        self.main_msg_view.setText(input_msg)

    def clear_view(self) -> None:
        self.main_msg_view.clear()

def get_zfillnum(num: int, padding: int):
    return str(num).zfill(padding)

class customQspinBox(QSpinBox):
    def __init__(self, parent=None) -> None:
        super(customQspinBox, self).__init__(parent)


        self.setAlignment(Qt.AlignCenter)
        self.setMinimum(1)
        self.setMaximum(1000)
        self.setFocusPolicy(Qt.NoFocus)

    def value(self) -> str:
        return "v"+get_zfillnum(super().value(), 3)

    def setValue(self, val: str) -> None:
        val = val.replace('v', '')
        return super().setValue(int(val))

    def textFromValue(self, v: int) -> str:
        return "v"+get_zfillnum(v, 3)

class SequenceInfoWidget(QWidget):
    MIN_NUM = 1
    MAX_NUM = 99999
    def __init__(self, _parent=None) -> None:
        super(SequenceInfoWidget, self).__init__(_parent)



        self.setupUi()

    def setupUi(self) -> None:

        self.s_frame_title_lb = QLabel("Start Frame")
        self.s_frame_contents_sb = QSpinBox()
        self.s_frame_contents_sb.setRange(self.MIN_NUM, self.MAX_NUM)
        self.s_frame_contents_sb.setValue(1001)

        self.e_frame_title_lb = QLabel("End Frame")
        self.e_frame_contents_sb = QSpinBox()
        self.e_frame_contents_sb.setRange(self.MIN_NUM, self.MAX_NUM)
        self.e_frame_contents_sb.setValue(1100)

        self.sample_title_lb = QLabel("Sample Value")
        self.sample_contents_sb = QSpinBox()
        self.sample_contents_sb.setRange(self.MIN_NUM, self.MAX_NUM)
        self.sample_contents_sb.setValue(3)

        self.main_gl = QGridLayout()
        self.main_gl.addWidget(self.s_frame_title_lb, 0,0)
        self.main_gl.addWidget(self.s_frame_contents_sb, 0,1)
        self.main_gl.addWidget(self.e_frame_title_lb, 1,0)
        self.main_gl.addWidget(self.e_frame_contents_sb, 1,1)
        self.main_gl.addWidget(self.sample_title_lb, 2,0)
        self.main_gl.addWidget(self.sample_contents_sb, 2,1)
        self.main_gl.setAlignment(Qt.AlignLeft)
        seq_margin = 50
        self.main_gl.setContentsMargins(seq_margin, 0, seq_margin, seq_margin)

        self.setLayout(self.main_gl)
        


    def get_info(self) -> dict:
        s_frame = self.s_frame_contents_sb.value()
        e_frame = self.e_frame_contents_sb.value()
        sample  = self.sample_contents_sb.value()

        return {"Start_Frame":s_frame, "End_Frame":e_frame, "Sample":sample}
    
    def set_info(self, *args, **kwargs) -> None:
        
        s_frame         = kwargs["Start_Frame"]
        e_frame         = kwargs["End_Frame"]
        sample          = kwargs["Sample"]
        
        self.s_frame_contents_sb.setValue(s_frame)
        self.e_frame_contents_sb.setValue(e_frame)
        self.sample_contents_sb.setValue(sample)
   
class OutDirLineedit(QLineEdit):
    def __init__(self, _parent=None) -> None:
        super(OutDirLineedit, self).__init__(_parent)

        self.setReadOnly(True)
        self.setStyleSheet(f'''
                            QLineEdit{{color : #A9A9A9;}}
                            QLineEdit:hover{{color : #D9D9D9;}}
                            ''')
    def mousePressEvent(self, e) -> None:
        input_dir = self.text()
        if os.path.exists(input_dir) == True:
            os.system(f"nautilus {input_dir}")

class JobSpecInputWidget(QWidget):
    
    def __init__(self, _parent=None) -> None:
        super(JobSpecInputWidget, self).__init__(_parent)
        self.contents_widgets = []
        self.input_path       = ""
        self.setupUi()
        

    def setupUi(self) -> None:
        


        self.with_scene_info_cb = QCheckBox("Do bake with Maya Scene value?")
        self.with_scene_info_cb.setChecked(True)
        

        self.seq_info_wg = SequenceInfoWidget()
        self.seq_info_wg.setEnabled(False)


        self.vernum_title_lb = QLabel("Version")
        self.vernum_title_lb.setStyleSheet(f'''
                                            QLabel{{font : 14px;}}
                                            ''')
        self.vernum_contents_sb = customQspinBox()
        self.vernum_contents_sb.setContentsMargins(8, 3, 13, 3)
        vernum_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.vernum_hl = QHBoxLayout()
        self.vernum_hl.addWidget(self.vernum_title_lb)
        self.vernum_hl.addWidget(self.vernum_contents_sb)
        self.vernum_hl.addItem(vernum_spacer)
        self.vernum_hl.setStretch(0, 1)
        self.vernum_hl.setStretch(1, 6)
        self.vernum_hl.setStretch(2, 2)

        self.outdir_title_lb = QLabel("Output")
        self.outdir_title_lb.setStyleSheet(f'''
                                            QLabel{{font : 14px;}}
                                            ''')
        self.outdir_contents_le = OutDirLineedit()
        self.outdir_contents_le.setContentsMargins(8, 1, 8, 2)
        self.outdir_contents_btn = QPushButton("...")
        self.outdir_contents_btn.clicked.connect(self.select_dir)

        self.out_dir_hl = QHBoxLayout()
        self.out_dir_hl.addWidget(self.outdir_title_lb, Qt.AlignLeft)
        self.out_dir_hl.addWidget(self.outdir_contents_le)
        self.out_dir_hl.addWidget(self.outdir_contents_btn)
        self.out_dir_hl.setStretch(0, 1)
        self.out_dir_hl.setStretch(1, 6)
        self.out_dir_hl.setStretch(2, 1)


        input_info_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.save_btn = QPushButton("Save Job Info")

        self.main_vl = QVBoxLayout()
        self.main_vl.addWidget(self.with_scene_info_cb)
        self.main_vl.addWidget(self.seq_info_wg)
        self.main_vl.addLayout(self.vernum_hl)
        self.main_vl.addLayout(self.out_dir_hl)
        self.main_vl.addItem(input_info_spacer)
        self.main_vl.addWidget(self.save_btn)
        
        self.setLayout(self.main_vl)


        # Set Signal and Slot
        self.with_scene_info_cb.stateChanged.connect(self.seq_info_wg.setDisabled)

        

    def select_dir(self) -> str:
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        selected_path = folder_dialog.getExistingDirectory(self, "Select Directory",  os.path.expanduser("~"),options=QFileDialog.DontUseNativeDialog)

        if selected_path:
            self.outdir_contents_le.setText(selected_path)


    def set_contents_style(self) -> None:
        background_color    = "#232629"
        border_color        = "#232629"
        border_radius       = "12px"
        contents_font_color = "rgba(255,255,255,200)"
        for item in self.contents_widgets:
            if isinstance(item, QLineEdit):
                item.setStyleSheet(f'''QLineEdit{{
                                               background-color: {background_color};
                                               color:{contents_font_color};
                                               border : {border_color};
                                               border-radius : 12px;
                                            }}''')
            elif isinstance(item, QComboBox):
                item.setStyleSheet(f'''QComboBox{{
                                               background-color: {background_color};
                                               color:{contents_font_color};
                                               border : {border_color};
                                               border-radius : 12px;
                                            }}''')
            elif isinstance(item, QTextEdit):
                item.setStyleSheet(f'''QTextEdit{{
                                               background-color: {background_color}; 
                                               color:{contents_font_color};
                                            }}''')
            elif isinstance(item, QListWidget):
                item.setStyleSheet(f'''QListWidget{{
                                               background-color: {background_color}; 
                                               color:{contents_font_color};
                                            }}''')

    def set_info(self, info_dict :dict) -> None:
        def get_default_path(input_path :str) -> str:
            input_file_dir = os.path.dirname(input_path)
            root_path = ""
            if "/dev/" in input_file_dir:
                root_path = input_file_dir.split("/dev/")[0]
            else:
                root_path = input_file_dir
            
            default_path = f"{root_path}/dev/cache/fur"
            if os.path.exists(default_path) == False:
                os.makedirs(default_path)
            return default_path
        
        def get_last_vernum(input_path :str) -> str:
            exists_ver_list = []
            for tar in os.listdir(input_path):
                if os.path.isfile(tar) == False:
                    if re.search(r"v\d{3}", tar):
                        exists_ver_list.append(tar)
            
            if exists_ver_list == []:
                return "v001"
            exists_ver_list.sort()
            last_vernum = exists_ver_list[-1]
            temp = int(last_vernum.replace("v", ""))
            temp += 1
            latest_vernum = f"v" + str(temp).zfill(3)
            return latest_vernum

        if info_dict == {}:
            return
        
        input_file_path     = info_dict.get("Input_File_Path")
        with_scene_info     = info_dict.get("With_Scene_Info")
        s_frame             = info_dict.get("Start_Frame")
        e_frame             = info_dict.get("End_Frame")
        sample              = info_dict.get("Sample")
        out_dir             = info_dict.get("Out_Dir")
        vernum              = info_dict.get("Vernum")

        self.input_path = input_file_path

        if with_scene_info == False:
            self.with_scene_info_cb.setChecked(with_scene_info)
        else:
            self.with_scene_info_cb.setChecked(True)



        seq_info_dict = {}
        if s_frame:
            seq_info_dict["Start_Frame"] = s_frame
        else:
            seq_info_dict["Start_Frame"] = 1001

        if e_frame:
            seq_info_dict["End_Frame"] = e_frame
        else:
            seq_info_dict["End_Frame"] = 1100

        if sample:
            seq_info_dict["Sample"] = sample
        else:
            seq_info_dict["Sample"] = 3


        default_path = get_default_path(input_file_path)
        latest_vernum = get_last_vernum(default_path)
        if vernum:
            self.vernum_contents_sb.setValue(vernum)
        else:
            self.vernum_contents_sb.setValue(latest_vernum)


        if out_dir:
            self.outdir_contents_le.setText(out_dir)
        else:
            
            self.outdir_contents_le.setText(default_path)

        self.seq_info_wg.set_info(**seq_info_dict)
    
    def get_saved_info(self) -> dict:
        
        saved_info = {}
        saved_info["Input_File_Path"] = self.input_path
        saved_info["With_Scene_Info"] = self.with_scene_info_cb.isChecked()
        seq_info_dict = self.seq_info_wg.get_info()
        saved_info["Start_Frame"]   = seq_info_dict.get("Start_Frame")
        saved_info["End_Frame"]     = seq_info_dict.get("End_Frame")
        saved_info["Sample"]        = seq_info_dict.get("Sample")
        saved_info["Out_Dir"]       = self.outdir_contents_le.text()
        saved_info["Vernum"]        = self.vernum_contents_sb.value()
    
        return saved_info
        
class JobProcess_item(QWidget):
    ITEM_PROCESS = None
    def __init__(self):
        super().__init__()

        self.PROCESS_STATUS = ""        # FINISHED / ERROR / NOT_ENOUGH / READY / RUNNING
        self.process_log    = ""
        self.p              = None
        self.JOB_NUM        = ""
        self.JOB_INFO    = ""
        self.FROM_PATH      = ""
        self.ITEM_PROCESS   = QProcess()

        self.status_movie   = QMovie()

        self.folder_thumb_lb = QLabel()
        

        self.title_lb = QLabel("...")
        self.title_lb.setStyleSheet('''QLabel{{padding-top:5px;}}''')
        self.title_lb.setFixedHeight(17)

        txt_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.status_lb = QLabel("ready")

        self.text_hl = QHBoxLayout()
        self.text_hl.addWidget(self.title_lb)
        self.text_hl.addItem(txt_spacer)
        self.text_hl.addWidget(self.status_lb)


        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setFixedHeight(6)
        self.progress.setStyleSheet(f'''
                                        QProgressBar{{
                                            border : 1px solid #4f5b62;
                                            border-radius : 7px;
                                        }}
                                        QProgressBar::chunk{{
                                            border : 1px solid #4f5b62;
                                            border-radius : 7px;
                                        }}
                                    ''')

        self.h = QVBoxLayout()
        self.h.addLayout(self.text_hl)
        self.h.addWidget(self.progress)
        self.h.setContentsMargins(7,2,7,2)
        
        btn_size = 30
        self.del_item_btn = QPushButton("X")
        self.del_item_btn.setFixedSize(btn_size, btn_size)
        self.del_item_btn.setStyleSheet(f'''QPushButton{{border-radius : 15px;}}''')

        l = QHBoxLayout()
        l.addWidget(self.folder_thumb_lb)
        l.addLayout(self.h)
        l.addWidget(self.del_item_btn)
        
        self.setLayout(l)
        self.setAcceptDrops(True)

        
    
    def get_del_btn(self) -> QPushButton:
        return self.del_item_btn

    def set_info(self, input_path :str) -> None:
        '''
        get assetname, type, project name from path
        and then
        auto set tags

        and then 
        user name, update date
        '''
        self.FROM_PATH = input_path

        size = 50
        folder_pixmap = QPixmap(YETI_IMG)
        pr = QWindow().devicePixelRatio()
        folder_pixmap.setDevicePixelRatio(pr)
        size *= pr
        folder_pixmap = folder_pixmap.scaled(int(size), int(size), Qt.KeepAspectRatio,
                                                                   Qt.SmoothTransformation)
        self.folder_thumb_lb.setPixmap(folder_pixmap)
        self.title_lb.setText(os.path.basename(input_path))


    def set_job_num(self, job_num :str) -> None:
        self.JOB_NUM = job_num
        # self.check_process_ready()

    def store_upload_info(self, editted_job_spec :dict) -> None:
        '''
        Data contents example : 
                {'Created_Date': '2023-04-26 11:31:53',
                'Description': 'eeee',
                'Name': 'ryan',
                'Tags': ['aaa'],
                'Thumb_Path': '/tmp/publishThumbs/thumb_20230426113206.png',
                'Type': 'Character',
                'User': '송태영 PIPE'}
        '''
        self.progress.setValue(0)
        self.JOB_INFO = dumps(editted_job_spec)
        # self.check_process_ready()


    def update_progress(self, to_value :int) -> None:
        from_value = self.progress.value()

        for cur_value in range(from_value, to_value+1):
            self.progress.setValue(cur_value)
            QApplication.processEvents()
            time.sleep(0.005)

    def check_process_ready(self) -> bool:
        
        if len(loads(self.JOB_INFO)) < 4 or self.JOB_NUM == "" or self.FROM_PATH == "":
            self.PROCESS_STATUS = "NOT_ENOUGH"
            self.set_log(f"업로드하려는 어셋의 정보가 다 입력되지 않았습니다.\n\n{self.JOB_INFO}")
            return False
        else:
            self.PROCESS_STATUS = "READY"
            return True

    def change_status_gif(self, status_msg :str) -> None:
        
            
        self.status_movie.stop()
        
        cur_gif = ""
        if status_msg == "START":
            cur_gif = LOADING_GIF
            scaled_size = QSize(27, 27)
        elif status_msg == "CLEAR":
            cur_gif = CLEAR_GIF
            scaled_size = QSize(27, 27)
        elif status_msg == "ERROR":
            cur_gif = ERROR_GIF
            scaled_size = QSize(41, 32)
        elif status_msg == "WARNNING":
            cur_gif = WARNNING_GIF
            scaled_size = QSize(27, 27)
            
        
        self.status_movie.setFileName(cur_gif)
        self.status_movie.setScaledSize(scaled_size)
        self.status_movie.start()

        if self.status_lb.movie():
            return
        self.status_lb.setMovie(self.status_movie)

    def set_log(self, input_msg :str) -> None:
        self.process_log = input_msg

    def get_log(self) -> str:
        return self.process_log

    # # =======================================================================
    # #                           Process part
    # # =======================================================================
    def get_process(self) -> QProcess:
        return self.ITEM_PROCESS

class custom_listwidget(QListWidget):
    def __init__(self, _parent=None, DEFAULT_INFO :dict={}) -> None:
        super(custom_listwidget, self).__init__(_parent)
        self.setAcceptDrops(True)
        self.default_info = DEFAULT_INFO
        # self.setGridSize(QSize(300, 220))

    def add_item(self, input_path :str) -> None:
        
        self.default_info.update({"Input_File_Path":input_path})

        _custom_item = JobProcess_item()
        _custom_item.set_info(input_path)
        _custom_item.get_del_btn().clicked.connect(self.delete_custom_item)
    
        _listwidet_item = QListWidgetItem(self)
        _listwidet_item.setSizeHint(_custom_item.sizeHint())
        _listwidet_item.setFlags(_listwidet_item.flags() & ~Qt.ItemIsDragEnabled)
        _listwidet_item.setData(Qt.UserRole, self.default_info)
        self.addItem(_listwidet_item)
        self.setItemWidget(_listwidet_item, _custom_item)


    def delete_custom_item(self):
        _click_pos = self.mapFromGlobal(QCursor.pos())
        item = self.itemAt(_click_pos)
        pop_widget = self.itemWidget(item)
        idx  = self.indexFromItem(item).row()
        pop_item = self.takeItem(idx)
        

class JobListWidget(QWidget):
    def __init__(self, _parent=None, DEFAULT_INFO :dict={}) -> None:
        super(JobListWidget, self).__init__(_parent)
        self.setAcceptDrops(True)

        # self.target_list = []
        
        self.edge_color     = [66, 135, 245, 100]
        self.brush_color    = [245, 132, 66, 100]
        
        self.font_size      :int = 30
        self.rect_rounded   :int = 5
        self.device_width   :int = 0
        self.device_height  :int = 0
        self.init_data()

        self.VIEW_TYPE = "DRAG_N_DROP"

        self.job_items_view = custom_listwidget(DEFAULT_INFO=DEFAULT_INFO)
        self.LALU_upload_btn = QPushButton("Execute")
        
        
        

    @property
    def edge_color(self) -> QPen:
        return self.__pen

    @edge_color.setter
    def edge_color(self, pen_color: list) -> None:
        self.__pen = QPen()
        self.__pen.setColor(QColor(pen_color[0], pen_color[1], pen_color[2], pen_color[3]))

    @property
    def brush_color(self) -> QBrush:
        return self.__brush

    @brush_color.setter
    def brush_color(self, brush_color: list) -> None:
        self.__brush = QBrush()
        self.__brush.setColor(QColor(brush_color[0], brush_color[1], brush_color[2], brush_color[3]))
        self.__brush.setStyle(Qt.SolidPattern)

    def init_data(self) -> None:
        img_data = open(MAYA_IMG, "rb").read()
        _path, img_type = os.path.splitext(MAYA_IMG)
        if "." in img_type:
            img_type = img_type.replace(".", "")

        # Load image
        image = QImage.fromData(img_data, img_type)

        self.dragdrop_img_w = image.width()
        self.dragdrop_img_h = image.height()


    def draw_file_inputinform_rect(self, e: QPaintEvent, painter: QPainter) -> None:
        painter.eraseRect(e.rect())
        painter.setPen(QPen(QColor(0, 0, 0), 10, Qt.DotLine))
        painter.setBrush(QBrush(QColor(255,255,255,0)))
        cur_font = QFont()
        cur_font.setPixelSize(self.font_size)
        painter.setFont(cur_font)
        painter.drawRoundedRect(QRect(0, 0, self.device_width, self.device_height), self.rect_rounded, self.rect_rounded)
        painter.drawText(int(self.device_width/2)-90, int(self.device_height/2)+int(self.dragdrop_img_h/2)+30, "Drag and Drop")
        file_img = QPixmap(MAYA_IMG)
        painter.drawPixmap(int(self.device_width/2)-int(self.dragdrop_img_w/2), int(self.device_height/2)-int(self.dragdrop_img_h/2), file_img)
         



    
    def paintEvent(self, e: QPaintEvent) -> None:
        def init_painter(edge_color, brush_color,_painter):
            _painter.setRenderHint(QPainter.Antialiasing)
            _painter.setPen(edge_color)
            _painter.setBrush(brush_color)

            self.device_width   = _painter.device().width()
            self.device_height  = _painter.device().height()
        
        if self.VIEW_TYPE == "DRAG_N_DROP":
            _p = QPainter(self)
            init_painter(self.edge_color, self.brush_color, _p)
            self.draw_file_inputinform_rect(e, _p)
            _p.end()
        else:
            self.update()



    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        cur_mimeData = e.mimeData()
        if cur_mimeData.hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        pass

    def dropEvent(self, e: QDropEvent) -> None:
        def check_path(input_path :str) -> bool:
            if os.path.exists(input_path) == False:
                return False
            if os.path.isdir(input_path) == True:
                return False
            elif os.path.isfile(input_path) == True and ".mb" in os.path.splitext(input_path):
                return True
            elif os.path.isfile(input_path) == True and ".ma" in os.path.splitext(input_path):
                return True
            # elif os.path.isfile(input_path) == True:
            #     return True
            else:
                return False
        
        target_list = []
        check_paths = e.mimeData().urls()
        for _check_tar in check_paths:
            _check_tar_str = _check_tar.toString()
            _check_tar_str = _check_tar_str.replace("file:///", "/")
            if check_path(_check_tar_str) == False:
                continue
            target_list.append(_check_tar_str)

        self.VIEW_TYPE = "LISTWIDGET"
        self.setup_listwidget_view()
        for target in target_list:
            self.job_items_view.add_item(target)


    def drop_from_outPack(self, pack_root_path :str) -> None:
        self.VIEW_TYPE = "LISTWIDGET"
        self.setup_listwidget_view()
        self.job_items_view.add_item(pack_root_path)


    def set_preference(self) -> None:
        print("Set path preference")


    def setup_listwidget_view(self) -> None:
            
        main_vl = QVBoxLayout(self)
        main_vl.addWidget(self.job_items_view)
        main_vl.addWidget(self.LALU_upload_btn)

        self.setLayout(main_vl)

    def get_current_item(self) -> QListWidgetItem:
        selected_items = self.job_items_view.selectedItems()
        if selected_items:
            return selected_items[0]
        
class JobSpecWidget(QWidget):
    def __init__(self, _parent=None) -> None:
        super(JobSpecWidget, self).__init__(_parent)
        self.setAcceptDrops(True)

        self.edge_color = [0, 0, 0, 200]
        self.brush_color = [255, 255, 255, 0]
        
        self.font_size      :int = 30
        self.rect_rounded   :int = 5
        self.device_width   :int = 0
        self.device_height  :int = 0

        self.VIEW_TYPE = "DRAG_N_DROP"
        self.input_job_info_view = JobSpecInputWidget()

    @property
    def edge_color(self) -> QPen:
        return self.__pen

    @edge_color.setter
    def edge_color(self, pen_color: list) -> None:
        self.__pen = QPen()
        self.__pen.setColor(QColor(pen_color[0], pen_color[1], pen_color[2], pen_color[3]))

    @property
    def brush_color(self) -> QBrush:
        return self.__brush

    @brush_color.setter
    def brush_color(self, brush_color: list) -> None:
        self.__brush = QBrush()
        self.__brush.setColor(QColor(brush_color[0], brush_color[1], brush_color[2], brush_color[3]))
        self.__brush.setStyle(Qt.SolidPattern)

    def paintEvent(self, e: QPaintEvent) -> None:
        def init_painter(edge_color, brush_color,_painter):
            _painter.setRenderHint(QPainter.Antialiasing)
            _painter.setPen(edge_color)
            _painter.setBrush(brush_color)

            self.device_width   = _painter.device().width()
            self.device_height  = _painter.device().height()
        
        if self.VIEW_TYPE == "DRAG_N_DROP":
            _p = QPainter(self)
            init_painter(self.edge_color, self.brush_color, _p)
            
            cur_font = QFont()
            cur_font.setPixelSize(self.font_size)
            font_size = cur_font.pixelSize()
            _p.setFont(cur_font)
            _p.drawRoundedRect(QRect(0, 0, self.device_width, self.device_height), self.rect_rounded, self.rect_rounded)
            _p.drawText(15, int(self.device_height/2) + font_size, "선택된 Job 이 없습니다.")

            _p.end()
        else:
            self.update()

    def setup_listwidget_view(self) -> None:
        self.VIEW_TYPE = "JOB_SPEC"
        
        
        main_vl = QVBoxLayout()
        main_vl.addWidget(self.input_job_info_view)
        
        self.setLayout(main_vl)


    def set_spec_view(self, spec_info :dict) -> None:
        if self.VIEW_TYPE != "JOB_SPEC":
            self.setup_listwidget_view()

        self.input_job_info_view.set_info(spec_info)

    def set_save_siganl(self, save_signal :pyqtSignal) -> None:
        self.save_signal = save_signal
        self.input_job_info_view.save_btn.clicked.connect(self.save_info)

    def save_info(self) -> None:
        saved_info = self.input_job_info_view.get_saved_info()
        self.save_signal.emit(saved_info)
    
class MainWindow(QMainWindow):
    _SAVE_SPEC_INFO_CLICKED_ = pyqtSignal(dict)
    def __init__(self, _parent=None):
        def move_2_center(main_view):
            qr = main_view.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            main_view.move(qr.topLeft())

        super(MainWindow, self).__init__(_parent)

        self.msg_dialog     = ProcessMSG(self)
        self.process_pool   = ProcessPool()
        self.p              = None
        self.CUR_DATE       = ""


        
        current_time    = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.CUR_DATE   = current_time


        self.job_list_view_lw = JobListWidget(DEFAULT_INFO={})

        # self.input_jobspec_wg = JobSpecInputWidget()
        self.input_jobspec_wg = JobSpecWidget()
        self.input_jobspec_wg.set_save_siganl(self._SAVE_SPEC_INFO_CLICKED_)
        

        main_hl = QHBoxLayout()
        main_hl.addWidget(self.job_list_view_lw)
        main_hl.addWidget(self.input_jobspec_wg)
        main_hl.setStretch(0,3)
        main_hl.setStretch(1,2)



        w = QWidget()
        w.setLayout(main_hl)
        self.setCentralWidget(w)


        self.menu_bar       = QMenuBar(self)
        self.menu_bar.setGeometry(0, 0, 800, 25)
        self.menu_element   = QMenu(self.menu_bar)
        self.menu_element.setTitle("Edit")
        self.action_import  = QAction(self)
        self.action_import.setText("Set Preference")                # Set path info // mayapy...
        self.menu_element.addAction(self.action_import)
        self.action_import.triggered.connect(self.job_list_view_lw.set_preference)
        self.menu_bar.addAction(self.menu_element.menuAction())


        self.setMenuBar(self.menu_bar)


        self.resize(850,600)
        self.setWindowTitle("YetiFurBakery - Batch mode")
        self.setWindowIcon(QIcon(YETI_IMG))
        move_2_center(self)

        apply_stylesheet(self, "dark_blue.xml")

        self.set_link()

    def set_link(self) -> None:
        
        self.job_list_view_lw.job_items_view.itemClicked.connect(self.show_and_edit_spec)
        self.job_list_view_lw.job_items_view.itemDoubleClicked.connect(self.show_process_msg)
        self._SAVE_SPEC_INFO_CLICKED_.connect(self.update_upload_item)
        self.job_list_view_lw.LALU_upload_btn.clicked.connect(self.do_upload)
        
    def show_and_edit_spec(self, item :QListWidgetItem) -> None:
        job_spec_info = item.data(Qt.UserRole)
        if job_spec_info == None:
            job_spec_info = {}
        self.input_jobspec_wg.set_spec_view(job_spec_info)

    def show_process_msg(self, item :QListWidgetItem) -> None:
        process_item = self.job_list_view_lw.job_items_view.itemWidget(item)
        process_msg = process_item.get_log()

        if process_msg == "":
            process_msg = "Clear !"

        self.msg_dialog.clear_view()
        self.msg_dialog.set_msg(process_msg)
        self.msg_dialog.exec_()


    def update_upload_item(self, updated_info :dict) -> None:
        
        
        cur_selected_item = self.job_list_view_lw.get_current_item()
        cur_selected_item.setData(Qt.UserRole, updated_info)

        self.show_and_edit_spec(cur_selected_item)


    def do_upload(self) -> None:
        print("Upload!!")
        READY_TO_START = True

        self.process_pool.clear_all()
        self.job_list_view_lw.job_items_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.input_jobspec_wg.setEnabled(False)
        for _idx in range(self.job_list_view_lw.job_items_view.count()):
            cur_job_item = self.job_list_view_lw.job_items_view.item(_idx)
            job_item_wg = self.job_list_view_lw.job_items_view.itemWidget(cur_job_item)
            
            editted_job_spec = cur_job_item.data(Qt.UserRole)
            job_item_wg.set_job_num("Job{0}".format(str(_idx).zfill(2)))
            job_item_wg.store_upload_info(editted_job_spec)
            
            if job_item_wg.check_process_ready() == False:
                READY_TO_START = False
                job_item_wg.change_status_gif("WARNNING")
            
            self.process_pool.add_process(job_item_wg)

        if READY_TO_START == True:
            self.process_pool.run()

        self.job_list_view_lw.job_items_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.input_jobspec_wg.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()


    app.exec_()