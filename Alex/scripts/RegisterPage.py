from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys

class RegisterPage(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,parent=None):
        super(RegisterPage, self).__init__(parent)
        loadUi('UI/registerPage.ui',self)
        self.mc = mc
        self.btn_register.clicked.connect(self.register)
        self.btn_toLogin.clicked.connect(self.toLogin)

    def register(self):
        ok = True
        username = 'cxl'
        print(self.cbx_gm.isChecked())
        ##########################
        # 主服务器
        ##########################
        url =self.mc.url + '/register?'
        if ok:
            QMessageBox.information(self,'成功',username + ' 账号注册成功！')
            self.mc.nextPage = 'loginPage'
            self.close()

    def toLogin(self):
        self.mc.nextPage = 'loginPage'
        self.close()

    def closeEvent(self, event):
        if not self.mc.nextPage:
            sys.exit()

    def run(self):
        self.mc.nextPage = None
        self.exec_()