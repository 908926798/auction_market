from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

class LoginPage(QWidget):
    close_signal = pyqtSignal()
    def __init__(self, rP,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(LoginPage, self).__init__(parent)
        loadUi('UI/test1.ui',self)
        self.registerPage = rP
        self.pushButton.clicked.connect(self.login)

    def closeEvent(self, event):
        self.close_signal.emit()
        self.close()

    def login(self):
        ok = True
        ##########################
        #调用数据库
        ##########################
        if ok:
            self.registerPage.handle_click()