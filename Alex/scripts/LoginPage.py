from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys

class LoginPage(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(LoginPage, self).__init__(parent)
        loadUi('UI/loginPage.ui',self)
        self.btn_login.clicked.connect(self.login)
        self.btn_toRegister.clicked.connect(self.toRegister)
        self.mainController = mc
        self.opened = False

    def login(self):
        ok = True
        ##########################
        #调用数据库
        ##########################
        if ok:
            self.mainController.username = 'cxl'
            self.mainController.nextPage = 'mainPage'
            self.close()

    def toRegister(self):
        self.mainController.nextPage = 'registerPage'
        self.close()

    def closeEvent(self, event):
        if not self.mainController.nextPage:
            sys.exit()

    def run(self):
        self.mainController.nextPage = None
        self.exec_()