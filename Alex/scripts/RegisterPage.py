from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys

class RegisterPage(QDialog):
    def __init__(self, mc,parent=None):
        super(RegisterPage, self).__init__(parent)
        loadUi('UI/registerPage.ui',self)
        self.mainController = mc
        self.btn_register.clicked.connect(self.register)
        self.btn_toLogin.clicked.connect(self.toLogin)

    def register(self):
        ok = True
        username = 'cxl'
        ##########################
        # 调用数据库
        ##########################
        if ok:
            QMessageBox.information(self,'成功',username + ' 账号注册成功！')
            self.mainController.nextPage = 'loginPage'
            self.close()

    def toLogin(self):
        self.mainController.nextPage = 'loginPage'
        self.close()

    def closeEvent(self, event):
        if not self.mainController.nextPage:
            sys.exit()

    def run(self):
        self.mainController.nextPage = None
        self.exec_()