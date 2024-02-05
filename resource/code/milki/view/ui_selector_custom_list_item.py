# -*- coding: utf-8 -*-


import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class QCustomQWidget(QtGui.QWidget):
    rm_click = QtCore.Signal()
    def __init__ (self, item_info, parent =None):
        super(QCustomQWidget, self).__init__(parent)
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}

        
        self.setupUi(self)
        self.set_data(item_info)

        
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(424, 35)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.file_name_label = QtGui.QLabel(Form)
        self.file_name_label.setText(_fromUtf8(""))
        self.file_name_label.setObjectName(_fromUtf8("file_name_label"))
        self.file_name_label.setStyleSheet(
                                        "QLabel{"+\
                                            "background: "+self.style_component['background_color']+";"+\
                                            "border: none;"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "padding-left: 2px;"+\
                                        "}"+\
                                        "QLabel:hover{"+\
                                            "color: "+ self.style_component['font_color'] +";"+\
                                            "background: #363636;"+\
                                        "}"+\
                                        "QLabel:selected{"+\
                                            "background: #595959;"+\
                                            "color:"+ self.style_component['font_color'] +";"+\
                                        "}")
        self.horizontalLayout.addWidget(self.file_name_label)
        self.checkBox = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setText(_fromUtf8("X"))
        self.checkBox.clicked.connect(self.emit_rm_click)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox.setStyleSheet(
                                                "QPushButton{"+\
                                                "font: bold 11px ;"+\
                                                "border: none;"+\
                                                "border-color:"+ self.style_component['border_color']+";"+\
                                                "background-color:"+self.style_component['background_color']+";"+\
                                                "color:"+ self.style_component['font_color'] +";"+\
                                                "qproperty-alignment: AlignVCenter;"+\
                                                "border-radius : 5px;"
                                                "height : 21px;"+\
                                                "width : 21px;"+\
                                                "}"+\
                                                "QPushButton:pressed{"+\
                                                "color:"+ self.style_component['font_color_pressed'] +";"+\
                                                "border-color:" +self.style_component['background_color']+";"+\
                                                "background-color:" +self.style_component['font_color']+";"+\
                                                "qproperty-alignment: AlignVCenter;"+\
                                                "}")

        self.horizontalLayout.addWidget(self.checkBox)
        self.horizontalLayout.setStretch(0, 15)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
    def set_data(self, item_info):
        self.file_name_label.setText(item_info)
    
    def emit_rm_click(self):
        self.rm_click.emit()
        
