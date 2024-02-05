import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui


class CustomListWidget(QtGui.QListWidget):
    def __init__(self, parent):
        super(CustomListWidget, self).__init__(parent)
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet(
                                        "QListWidget{"+\
                                        "border-style: solid;"+\
                                        "border-width : 0.5px;"+\
                                        "border-color: "+ self.style_component['border_color'] +";"+\
                                        "border-radius: 1px;"+\
                                        "color : "+ self.style_component['font_color'] +";"+\
                                        "background:"+self.style_component['background_color']+";"+\
                                        "font: 12px;"+\
                                        "}"+\
                                        "QListWidget::branch:hover{"+\
                                        "background: #363636;"+\
                                        "}"+\
                                        "QListWidget::branch:selected{"+\
                                        "background: #363636;"+\
                                        "}"+\
                                        "QListWidget::item:hover {"+\
                                        "color: "+ self.style_component['font_color'] +";"+\
                                        "background: #363636;"+\
                                        "}"+\
                                        "QListWidget::item:selected{"+\
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
                                      "}"
                                      )
