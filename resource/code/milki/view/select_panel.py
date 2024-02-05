import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui
from importlib import reload
from functools import partial
from maya_md import neon
from general_md_3x import LUCY

import custom_list
#reload (custom_list)

import custom_list_item
#reload (custom_list_item)

import custom_lineedit
reload(custom_lineedit)

import maya_toolkit
reload(maya_toolkit)



import functools, os

class SelectPanel(QtGui.QWidget):

    back_layout = None
    main_layout = None

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.widgets = []
        self.spacers = []
        self.editors = {}

        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}

        self.verticalLayout_2 = QtGui.QVBoxLayout(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.back_layout = QtGui.QVBoxLayout()

        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.setStyleSheet("background : "+self.style_component['background_color']+";}")

        self.verticalLayout_2.addLayout(self.back_layout)

    def refresh(self):
        self.widgets = []
        self.spacers = []
        self.editors = {}

    def add_custom_item(self):
        list_items = []
        selected_roots= []
        try:
            selected_list = cmds.ls(selection=True, long = True)
        except Exception as e:
            # print(str(e))
            import maya.cmds as cmds
            selected_list = cmds.ls(selection=True, long = True)

        for sel in selected_list:
            if '|' in sel:
                selected_roots.append(sel.split('|')[-1])
            else:
                selected_roots.append(sel)

        list_items.extend(selected_roots)

        for widget in self.widgets:
            widget_name = widget.objectName().lower()
            if widget_name == "list":
                item_type = 'selector'
                list_widget = widget
                for idx, item in enumerate(list_items):
                    list_item=custom_list_item.CustomListItem(list_widget, item_type, item, idx)
                    list_item.selector_item_ui.rm_click.connect(functools.partial(self.remove_item, list_widget))


    def set_path_lb(self, dir_path):
        try:
            _file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", dir_path))
        except:
            _file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))

        self._file = str(_file)
        self.saturn_path_lb.setText(self._file)

        if not os.path.exists(self._file):
            self.saturn_path_lb.setText(dir_path)


    def add_select_widget(self, widget_type, title, items):
        
        if self.main_layout is None:
            self.main_layout = self.create_main_layout()
            self.back_layout.addLayout(self.main_layout)

        self._add_title(title)
        if widget_type.lower() == "checkbox":
            self._add_check_items(items)
        elif widget_type.lower() == "list":
            self._add_list_items(items)
        elif widget_type.lower() == 'edit':
            self._add_edit_items(title, items)
        elif widget_type.lower() == 'milki_edit':
            self._add_edit_items(title, items, _is_custom=True)
        # this part for saturn tool
        elif widget_type.lower() == 'browser':
            self._add_path_browser_items(title, items)
        # this part for saturn tool
        # this port must be with list
        elif widget_type.lower() == 'button':
            self._add_target_adder_items(title, items)
        elif widget_type.lower() == 'spinbox':
            self._add_spinbox_items(title, items)

        

        spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.spacers.append(spacer)
        self.back_layout.addItem(spacer)
        self.back_layout.invalidate()
        self.repaint()

    def create_main_layout(self):
        m_layout = QtGui.QVBoxLayout(self)
        m_layout.setSpacing(0)
        m_layout.setMargin(0)
        return m_layout

    def clear_all_of_list(self):
        for widget in self.widgets:
            widget_name = widget.objectName().lower()
            if widget_name == "list":
                item_type = 'selector'
                list_widget = widget
                list_widget.clear()
                


    def _add_target_adder_items(self, title, items):
        


        try:
            import maya.cmds as cmds
        except Exception as e:
            print(str(e))

        path_layout = QtGui.QHBoxLayout(self)
        self.main_layout.addLayout(path_layout)

        spacer = QtGui.QSpacerItem(680, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.spacers.append(spacer)


        btn_list = []
        if LUCY.get_category() == 'sequence' and LUCY.get_pipe_step() in ["animation", "layout", "previz"]:
            btn_width = 70
            btn_height = 40
            self.select_loc_btn = QtGui.QPushButton(self)
            self.select_loc_btn.setText("Sel Loc")
            self.select_loc_btn.setFixedSize(btn_width, btn_height)
            self.select_loc_btn.clicked.connect(maya_toolkit.sel_all_loc)
            path_layout.addWidget(self.select_loc_btn)
            btn_list.append(self.select_loc_btn)


            self.select_geo_btn = QtGui.QPushButton(self)
            self.select_geo_btn.setText("Sel Geo")
            self.select_geo_btn.setFixedSize(btn_width, btn_height)
            self.select_geo_btn.clicked.connect(maya_toolkit.sel_all_geo)
            path_layout.addWidget(self.select_geo_btn)
            btn_list.append(self.select_geo_btn)


            self.select_clear_btn = QtGui.QPushButton(self)
            self.select_clear_btn.setText("Clear")
            self.select_clear_btn.setFixedSize(btn_width, btn_height)
            self.select_clear_btn.clicked.connect(self.clear_all_of_list)
            path_layout.addWidget(self.select_clear_btn)
            btn_list.append(self.select_clear_btn)





        path_layout.addItem(spacer)

        self.saturn_plus_btn = QtGui.QPushButton(self)
        self.saturn_plus_btn.setObjectName("plus target button")
        self.saturn_plus_btn.setFixedSize(40,40)
        btn_list.append(self.saturn_plus_btn)
        self.saturn_plus_btn.setText('+')
        path_layout.addWidget(self.saturn_plus_btn)
        self.saturn_plus_btn.clicked.connect(self.add_custom_item)


        for btn in btn_list:
            btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px ;"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 3px;"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "border-radius: 3px;"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")

    def _add_path_browser_items(self, title, items):
        try:
            import maya.cmds as cmds
        except Exception as e:
            print(str(e))

        _idx_path = 0
        cur_file_dir_path = items[_idx_path]

        path_layout = QtGui.QHBoxLayout(self)
        self.main_layout.addLayout(path_layout)

        self.saturn_find_btn = QtGui.QPushButton(self)
        self.saturn_find_btn.setObjectName("saturn_find_btn")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saturn_find_btn.sizePolicy().hasHeightForWidth())
        self.saturn_find_btn.setSizePolicy(sizePolicy)
        self.saturn_find_btn.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: 13px ;"+\
                                                "border: 1px solid;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "border-radius: 3px;"+\
                                                "background-color:"+self.style_component['button_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "border-radius: 3px;"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "}")
        self.saturn_find_btn.setText('Select Path')
        path_layout.addWidget(self.saturn_find_btn)
        self.saturn_find_btn.clicked.connect(functools.partial(self.set_path_lb, cur_file_dir_path))


        self.saturn_path_lb = QtGui.QLabel(self)
        self.saturn_path_lb.setObjectName("browserlabel")
        self.saturn_path_lb.setStyleSheet("QLabel{"+\
                                    "border-style: solid;"+\
                                    "border-width : 0.5px;"+\
                                    "border-color: "+ self.style_component['border_color'] +";"+\
                                    "border-radius: 5px;"+\
                                    "color :"+ self.style_component['font_color'] +";"+\
                                    "background:#272727;"+\
                                    "font: 11px;"+\
                                    "padding-left: 3px;"+\
                                    "}")

        self.saturn_path_lb.setText(cur_file_dir_path)
        self.saturn_path_lb.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        path_layout.addWidget(self.saturn_path_lb)

        path_layout.setStretch(0, 1)
        path_layout.setStretch(1, 7)

        self.widgets.append(self.saturn_path_lb)

    def _add_title(self, title):
        if title == 'plus button':
            pass
        else:
            title_label = QtGui.QLabel(self)
            title_label.setText(title)
            title_label.setObjectName("title")
            title_label.setMinimumHeight(30)
            title_label.setMaximumHeight(30)
            title_label.setStyleSheet(
                                    "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "color: "+ self.style_component['font_color'] +";"+\
                                        "font: bold 13px;"+\
                                        "padding-left: 2px;"+\
                                    "}")
            self.widgets.append(title_label)
            self.main_layout.addWidget(title_label)

    def _add_check_items(self, check_items):
        check_layout = None
        
        for idx, check_item in enumerate(check_items):
            if idx % 3 == 0:
                check_layout = QtGui.QHBoxLayout(self)
                self.main_layout.addLayout(check_layout)

            if check_layout is None:
                continue

            check_box = QtGui.QCheckBox(self)
            check_box.setMinimumHeight(30)
            check_box.setMaximumHeight(30)
            check_box.setText(str(check_item))
            print(11111111111111111111, check_item)
            if check_item == "abc sequence":
                check_box.setObjectName("abcsequencecheckbox")
            else:
                check_box.setObjectName("CheckBox")
            check_box.setStyleSheet(
                                "QCheckBox{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: none;"+\
                                    "color: "+ self.style_component['font_color'] +";"+\
                                    "font: 11px;"+\
                                "}")
            if not str(check_item) in ["submit"]:
                check_box.setChecked(1)

            if str(check_item).lower() == "abc sequence":
                check_box.setChecked(1)

            if str(check_item).lower() in 'sequence':
                check_box.setChecked(0)

            if str(check_item).lower() =="publish with alembic":
                check_box.setChecked(0)

            if str(check_item).lower() =="lookdev is assigned":
                check_box.setChecked(0)

            if str(check_item).lower() == "is anim shader":
                check_box.setChecked(0)

            if str(check_item).lower() == "export texture":
                check_box.setChecked(0)
                
            if str(check_item).lower() == "export tx":
                check_box.setChecked(0)

            # if str(check_item) == 'Strip Namespaces':
            #     checked_prj = []
            #     with open("Z:/backstage/maya/milki/docs/checked_projects.txt", 'r') as test_txt:
            #         checked_prj.extend(test_txt.read().split())
            #     if scn.get_project() in checked_prj:
            #         check_box.setChecked(0)

            self.widgets.append(check_box)

            check_layout.addWidget(check_box)

    def _add_list_items(self, list_items):
        list_widget = custom_list.CustomListWidget(self)
        list_widget.setObjectName("List")
        self.widgets.append(list_widget)
        self.main_layout.addWidget(list_widget)
        spacer = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.spacers.append(spacer)
        self.main_layout.addItem(spacer)
        item_type = 'selector'
        for idx, item in enumerate(list_items):
            list_item=custom_list_item.CustomListItem(list_widget, item_type, item, idx)
            list_item.selector_item_ui.rm_click.connect(functools.partial(self.remove_item, list_widget))
            


    def remove_item(self, list_widget):
        # list_widget = self.listWidget()
        if list_widget.count() < 2:
            return
        cursor = QtGuiOrig.QCursor()
        point = list_widget.mapFromGlobal(cursor.pos())
        item = list_widget.itemAt(point)
        idx  = list_widget.indexFromItem(item).row()
        print(item, idx)
        list_widget.takeItem(idx)


    def _add_edit_items(self, title, edit_items, _is_custom=False):
        if not title in self.editors:
            self.editors[title] = []
        edit_layout = None

        for idx, edit_item in enumerate(edit_items):
            if idx % 3 == 0:
                edit_layout = QtGui.QHBoxLayout(self)
                self.main_layout.addLayout(edit_layout)

            if edit_layout is None:
                continue


            line_edit = QtGui.QLineEdit(self)
            if _is_custom == True:
                line_edit = custom_lineedit.MilkiLineEdit(self, self.widgets)
            elif title == "Create Variation":
                line_edit = QtGui.QLineEdit(self)
                line_edit.setFixedWidth(120)
                line_edit.setFixedHeight(30)
                line_edit.setStyleSheet(
                            "QLineEdit{"+\
                                "background: #424242;"+\
                                "border: 1px solid #5e5e5e;"+\
                                "color: "+ self.style_component['font_color'] +";"+\
                                "font: 11px;"+\
                            "}")
            

            else:
                line_edit = QtGui.QLineEdit(self)
                line_edit.setMinimumHeight(20)
                line_edit.setMaximumHeight(20)
                line_edit.setMaximumWidth(50)
                line_edit.setMinimumWidth(50)
                line_edit.setStyleSheet(
                                    "QLineEdit{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: 1px solid #5e5e5e;"+\
                                        "color: "+ self.style_component['font_color'] +";"+\
                                        "font: 11px;"+\
                                    "}")


            line_edit.setText(str(edit_item))

            if title == "End Frame":
                line_edit.setObjectName("EndFrameLineEdit")
            else:
                line_edit.setObjectName("LineEdit")
            self.widgets.append(line_edit)
            self.editors[title].append(line_edit)
            edit_layout.addWidget(line_edit)

        spacer = QtGui.QSpacerItem(50, 30, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.spacers.append(spacer)
        edit_layout.addItem(spacer)


    def _add_spinbox_items(self, title, edit_items) -> None:
        if not title in self.editors:
            self.editors[title] = []
        spinbox_layout = None

        for idx, edit_item in enumerate(edit_items):
            if idx % 3 == 0:
                spinbox_layout = QtGui.QHBoxLayout(self)
                self.main_layout.addLayout(spinbox_layout)

            if spinbox_layout is None:
                continue


            spinbox = QtGui.QSpinBox(self)
            
            
            spinbox.setMinimumHeight(20)
            spinbox.setMaximumHeight(20)
            spinbox.setMaximumWidth(150)
            spinbox.setMinimumWidth(150)
            spinbox.setStyleSheet(
                        "QSpinBox{"+\
                            "background: "+self.style_component['background_color']+";"+\
                            "border: 1px solid #5e5e5e;"+\
                            "color: "+ self.style_component['font_color'] +";"+\
                            "font: 11px;"+\
                        "}")
            

            

            spinbox.setValue(edit_item[0])
            spinbox.setMaximum(edit_item[1])
            spinbox.setMinimum(edit_item[2])
            if title == "Description 에 입력할 nuke version":
                spinbox.setPrefix("Version : ")
            
            spinbox.setObjectName("LineEdit")
            self.widgets.append(spinbox)
            self.editors[title].append(spinbox)
            spinbox_layout.addWidget(spinbox)

        spacer = QtGui.QSpacerItem(50, 30, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.spacers.append(spacer)
        spinbox_layout.addItem(spacer)

    def get_select_infos(self):
        infos = {}
        title = ""
        elem_name = ""

        for widget in self.widgets:
            widget_name = widget.objectName().lower()

            if widget_name == 'title':
                title = str(widget.text())
                infos[title] = []
                continue
            elif widget_name in ["checkbox", "abcsequencecheckbox"]:
                if widget.isChecked() == True:
                    elem_name = widget.text()
                    infos[title].append(elem_name)
            elif widget_name == "list":
                all_items = self._get_all_list_items(widget)
                infos[title].extend(all_items)
            elif widget_name in ["lineedit", "endframelineedit"]:
                if not title in self.editors:
                    continue
                all_edits = self.editors[title]
                for edit in all_edits:
                    infos[title].append(str(edit.text()))
            elif widget_name == "browserlabel":
                infos[title].append(str(widget.text()))
            else:
                continue

        
        return infos
    
    def set_signal(self, from_widget_objname :str, to_widget_objname :str) -> list:

        def find_widget_by_objectname(obj_name :str):
            for widget in self.widgets:
                widget_name = widget.objectName().lower()
                if widget_name == obj_name:
                    return widget
                
        def edit_lineedit_txt(_status):
            if _status:
                to_widget.setText(str(neon.get_end_time()))
            else:
                to_widget.setText(str(neon.get_start_time()))
        if from_widget_objname == "abcsequencecheckbox" and to_widget_objname == "endframelineedit":
            from_widget = find_widget_by_objectname(from_widget_objname)
            to_widget = find_widget_by_objectname(to_widget_objname)
            from_widget.stateChanged.connect(edit_lineedit_txt)
            


    def _get_all_list_items(self, list_widget):
        list_items = []
        item_type = 'selector'
        for row in range(list_widget.count()):
            item = list_widget.item(row)
            list_items.append(item.get_label_text(item_type))

        return list_items

    def clear_all_items(self):
        if self.main_layout is None:
            return

        for widget in self.findChildren(QtGui.QWidget):
            self.main_layout.removeWidget(widget)
            widget.hide()

        for layout in self.findChildren(QtGui.QHBoxLayout):
            self.main_layout.removeItem(layout)
        for spacer in self.spacers:
            try:
                self.main_layout.removeItem(spacer)
            except:
                continue

        self.findChildren(QtGui.QHBoxLayout)
        for idx in range(self.main_layout.count()):
            widget_item = self.main_layout.takeAt(idx)
