import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui



class MilkiLineEdit(QtGui.QLineEdit):
    def __init__(self, _parent=None, _other_widgets=[]):
        super(MilkiLineEdit, self).__init__(_parent)
        self.style_component = {'background_color': '#333333',
                                'border_color': '#595959',
                                'font_color':'#D9D9D9',
                                'font_color_pressed': '#595959',
                                'button_color': 'rgba(70,70,70,0.5)'}

        self.setFixedWidth(120)
        self.setFixedHeight(30)
        self.setEnabled(False)
        self.textChanged.connect(self.check_input)
        self.setStyleSheet(
                            "QLineEdit{"+\
                                "background: "+self.style_component['background_color']+";"+\
                                "border: 1px solid #454545;"+\
                                "color: "+ self.style_component['font_color'] +";"+\
                                "font: 11px;"+\
                            "}")


        self.other_widget = _other_widgets
        self._anim_lb = self.other_widget[0]
        self._anim_cb = self.other_widget[1]
        self.create_version_lb = self.other_widget[-1]
        self.create_version_lb.setStyleSheet(
                                "QLabel{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: none;"+\
                                    "color: "+ self.style_component['font_color_pressed'] +";"+\
                                    "font: bold 13px;"+\
                                    "padding-left: 2px;"+\
                                "}")

    def enterEvent(self, event):
        self.setEnabled(True)
        self.setStyleSheet(
                            "QLineEdit{"+\
                                "background: #424242;"+\
                                "border: 1px solid #5e5e5e;"+\
                                "color: "+ self.style_component['font_color'] +";"+\
                                "font: 11px;"+\
                            "}")


        self._anim_lb.setStyleSheet(
                                "QLabel{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: none;"+\
                                    "color: "+ self.style_component['font_color_pressed'] +";"+\
                                    "font: bold 13px;"+\
                                    "padding-left: 2px;"+\
                                "}")
        self._anim_cb.setChecked(False)
        self._anim_cb.setStyleSheet(
                            "QCheckBox{"+\
                                "background: "+self.style_component['background_color']+";"+\
                                "border: none;"+\
                                "color: "+ self.style_component['font_color_pressed'] +";"+\
                                "font: 11px;"+\
                            "}")

        self.create_version_lb.setStyleSheet(
                                "QLabel{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: none;"+\
                                    "color: "+ self.style_component['font_color'] +";"+\
                                    "font: bold 13px;"+\
                                    "padding-left: 2px;"+\
                                "}")


    def leaveEvent(self, event):
        if str(self.text()) == "":
            self.setEnabled(False)
            self.setStyleSheet(
                                "QLineEdit{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: 1px solid #454545;"+\
                                    "color: "+ self.style_component['font_color'] +";"+\
                                    "font: 11px;"+\
                                "}")
            self._anim_lb.setStyleSheet(
                                    "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "color: "+ self.style_component['font_color'] +";"+\
                                        "font: bold 13px;"+\
                                        "padding-left: 2px;"+\
                                    "}")
            self._anim_cb.setStyleSheet(
                                "QCheckBox{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: none;"+\
                                    "color: "+ self.style_component['font_color'] +";"+\
                                    "font: 11px;"+\
                                "}")
            self.create_version_lb.setStyleSheet(
                                    "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "color: "+ self.style_component['font_color_pressed'] +";"+\
                                        "font: bold 13px;"+\
                                        "padding-left: 2px;"+\
                                    "}")



    def check_input(self, _text):
        if str(_text) == "":
            self.setStyleSheet(
                                "QLineEdit{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: 1px solid #454545;"+\
                                    "color: "+ self.style_component['font_color'] +";"+\
                                    "font: 11px;"+\
                                "}")
            self._anim_lb.setStyleSheet(
                                    "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "color: "+ self.style_component['font_color'] +";"+\
                                        "font: bold 13px;"+\
                                        "padding-left: 2px;"+\
                                    "}")
            self._anim_cb.setStyleSheet(
                                "QCheckBox{"+\
                                    "background: "+self.style_component['background_color']+";"+\
                                    "border: none;"+\
                                    "color: "+ self.style_component['font_color'] +";"+\
                                    "font: 11px;"+\
                                "}")
            self.create_version_lb.setStyleSheet(
                                    "QLabel{"+\
                                        "background: "+self.style_component['background_color']+";"+\
                                        "border: none;"+\
                                        "color: "+ self.style_component['font_color_pressed'] +";"+\
                                        "font: bold 13px;"+\
                                        "padding-left: 2px;"+\
                                    "}")
