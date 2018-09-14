from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

class RegisterPage(QWidget):
    def __init__(self, parent=None):
        super(RegisterPage, self).__init__(parent)
        loadUi('UI/test2.ui',self)

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()