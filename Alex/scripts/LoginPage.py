from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import json
import requests
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
        self.mc = mc

    def login(self):
        ##########################
        #访问主服务器
        ##########################
        url = self.mc.url + '/login?'
        url += 'login_name_email=' + self.lie_username.text()
        url += '&login_password=' + self.lie_password.text()

        try:
            res = requests.get(url)
            result = json.loads(res.text)
            if result['status']:
                self.mc.username = self.lie_username.text()
                self.mc.nextPage = 'mainPage'
                self.close()
            else:
                QMessageBox.information(self, "错误", "用户名或密码错误!", QMessageBox.Yes)
        except:
            QMessageBox.information(self, "错误", "与服务器通讯失败!", QMessageBox.Yes)

        self.lie_username.setText('')
        self.lie_password.setText('')

    def toRegister(self):
        self.mc.nextPage = 'registerPage'
        self.close()

    def closeEvent(self, event):
        if not self.mc.nextPage:
            sys.exit()

    def run(self):
        self.mc.nextPage = None
        self.exec_()