import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
import maya.cmds as cmds
import sys


class ResultTable(QtGui.QTableView):

    def __init__(self):
      QtGui.QTableView.__init__(self)
      self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
      sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
      sizePolicy.setHorizontalStretch(0)
      sizePolicy.setVerticalStretch(0)
      sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
      self.setSizePolicy(sizePolicy)
      self.setMinimumSize(QtCore.QSize(0, 0))
      self.setMaximumSize(QtCore.QSize(16777215, 16777215))
      # self.setHeaderLabels(['Name', 'Message', 'status'])
      # self.setRootIsDecorated(False)
      # self.setColumnWidth(0,350)
      # self.setColumnWidth(1,350)
      # self.setColumnWidth(2,15)
      # self.setIconSize(QtCore.QSize(12, 12))

      # self.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
      # self.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
      # self.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
      # self.setSortingEnabled(True)
      # self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
      self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
      self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
      self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
      self.verticalHeader().hide()
      self.clicked.connect(self.print_item)

      self.setStyleSheet(
                                      "QTableView{"+\
                                            "border-style: solid;"+\
                                            "border-width : 0.5px;"+\
                                            "border-color: "+ self.style_component['border_color'] +";"+\
                                            "border-radius: 1px;"+\
                                            "color : "+ self.style_component['font_color'] +";"+\
                                            "background:"+self.style_component['background_color']+";"+\
                                            "font: 12px;"+\
                                      "}"+\
                                      "QTreeWidget::item{"+\
                                            "border-bottom: 1px solid #303030;"+\
                                            "color:"+ self.style_component['font_color'] +";"+\
                                            "height : 16.5px;"+\
                                      "}"+\
                                      "QTreeWidget::branch:hover{"+\
                                            "background: #363636;"+\
                                      "}"+\
                                      "QTreeWidget::branch:selected{"+\
                                            "background: #363636;"+\
                                      "}"+\
                                      "QTreeWidget::item:hover {"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "background: #363636;"+\
                                      "}"+\
                                      "QTreeWidget::item:selected{"+\
                                            "background: #595959;"+\
                                            "color:"+ self.style_component['font_color'] +";"+\
                                      "}"+\
                                      "QScrollBar:vertical {"+\
                                            "width: 10px;"+\
                                            "margin: 20px 0 3px 0;"+\
                                            "border-radius: 5px;"+\
                                    "}"+\
                                    "QScrollBar::handle:vertical {"+\
                                            "background:" + self.style_component['font_color'] +";"+\
                                            "min-height: 5px;"+\
                                            "width : 10px;"
                                            "border-radius: 5px;"+\
                                    "}"+\
                                    "QScrollBar::add-line:vertical {"+\
                                      "background: none;"+\
                                      "height: 45px;"+\
                                      "subcontrol-position: bottom;"+\
                                      "subcontrol-origin: margin;"+\
                                    "}"+\
                                    "QScrollBar::sub-line:vertical {"+\
                                      "background: none;"+\
                                      "height: 45px;"+\
                                      "subcontrol-position: top;"+\
                                      "subcontrol-origin: margin;"+\
                                    "}"+\
                                    "QScrollBar:horizontal {"+\
                                      "height: 10px;"+\
                                      "margin: 20px 0 3px 0;"+\
                                      "border-radius: 5px;"+\
                                    "}"+\
                                    "QScrollBar::handle:horizontal {"+\
                                      "background:" + self.style_component['font_color'] +";"+\
                                      "min-height: 5px;"+\
                                    "}"+\
                                    "QScrollBar::add-line:horizontal {"+\
                                      "background: none;"+\
                                      "width: 45px;"+\
                                      "subcontrol-position: right;"+\
                                      "subcontrol-origin: margin;"+\
                                    "}"+\
                                    "QScrollBar::sub-line:horizontal {"+\
                                      "background: none;"+\
                                      "width: 45px;"+\
                                      "subcontrol-position: left;"+\
                                      "subcontrol-origin: margin;"+\
                                    "}"
                                    )

    def add_item(self, target, message, status):
        warn_item = QtGui.QTreeWidgetItem(self)
        warn_item.setTextAlignment(0, QtCore.Qt.AlignCenter)
        warn_item.setTextAlignment(1, QtCore.Qt.AlignCenter)
        warn_item.setTextAlignment(2, QtCore.Qt.AlignCenter)

        warn_item.setText(0, target)
        warn_item.setText(1, message)
        icon_label = QtGui.QLabel(self)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        if sys.platform.count("win"):
            img_path = "Z:/pipeline/playground/tools/milki/branches/taiyeong/code_data/milky_branch/icons/{0}_circle.png"
        else:
            img_path = "/usersetup/linux/module/ui_icons_md/milki/{0}_circle.png"
        if status == 'error':
          img_path = img_path.format("red")
        elif status == 'clear':
          img_path = img_path.format("green")
        pix_map = QtGuiOrig.QPixmap(img_path).scaled(12, 12, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        icon_label.setPixmap(pix_map)
        self.setItemWidget(warn_item, 2, icon_label)
        return warn_item

    def add_items(self, error_list):
        self._row_num = len(error_list)
        check_table_model = QtGuiOrig.QStandardItemModel(self._row_num, 3)
        check_table_model.setHorizontalHeaderLabels(['Name', u'Message', u'Status'])
        for row, info_dict in enumerate(error_list):
            _target_name = info_dict[0]
            _msg = info_dict[1]
            _status = "error"
            if _status.lower() == 'clear':
                continue
            _sel_tar = info_dict[0]
            task_name_item = QtGuiOrig.QStandardItem(str(_target_name))
            task_name_item.setData(_sel_tar, QtCore.Qt.UserRole)
            task_name_item.setTextAlignment(QtCore.Qt.AlignCenter)
            check_table_model.setItem(row, 0, task_name_item)

            link_name_item = QtGuiOrig.QStandardItem(str(_msg))
            link_name_item.setData(_sel_tar, QtCore.Qt.UserRole)
            link_name_item.setTextAlignment(QtCore.Qt.AlignCenter)
            check_table_model.setItem(row, 1, link_name_item)

            step_item = QtGuiOrig.QStandardItem(str(_status))
            step_item.setData(_sel_tar, QtCore.Qt.UserRole)
            step_item.setTextAlignment(QtCore.Qt.AlignCenter)
            step_item.setForeground(QtGuiOrig.QBrush(QtGuiOrig.QColor('#f05353')))
            check_table_model.setItem(row, 2, step_item)

        self.setModel(check_table_model)
        self.horizontalHeader().setFixedHeight(30)
        _column_width = 250
        self.setColumnWidth(0, _column_width)
        self.setColumnWidth(1, _column_width)
        self.setColumnWidth(2, 100)
        for row in range(self._row_num):
            self.setRowHeight(row, 30)
            self.showRow(row)


    def print_item(self, _idx):
        selected_tar_list = self.selectedIndexes()
        if selected_tar_list is None or selected_tar_list == []:
            return
        target = self.model().data(selected_tar_list[0])
        if target == '':
            print('none what this')
            return
        try:
            targets = cmds.ls(target, l=True)
            print('select ', targets)
            cmds.select(targets)
        except:
            return

    def clear_all_items(self):
        cur_data_model = self.model()
        if cur_data_model is None:
            return
        cur_data_model.clear()
        self.reset()
