from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import requests
import json
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
        if not self.lie_username.text() or not self.lie_password.text() or not self.lie_password2.text():
            QMessageBox.information(self, "错误", "信息不能为空!", QMessageBox.Yes)
            return
        if not self.cbx_gm.isChecked() and not self.cbx_nu.isChecked():
            QMessageBox.information(self, "错误", "至少选择一个角色!", QMessageBox.Yes)
            return
        if self.lie_password.text() != self.lie_password2.text():
            QMessageBox.information(self, "错误", "两次密码不一致!", QMessageBox.Yes)
            return

        #print(self.cbx_gm.isChecked())
        ##########################
        # 主服务器
        ##########################
        url =self.mc.url + '/register?'
        url += 'username=' + self.lie_username.text()
        url += '&password=' + self.lie_password.text()
        url += '&gm=' + str(self.cbx_gm.isChecked()+0)
        url += '&u=' + str(self.cbx_nu.isChecked()+0)

        try:
            res = requests.get(url)
            result = json.loads(res.text)
            if result['status']:
                self.mc.nextPage = 'loginPage'
                self.close()
                QMessageBox.information(self, "成功", "用户 " + self.lie_username.text() + " 注册成功!", QMessageBox.Yes)
            else:
                QMessageBox.information(self, "错误", "无法注册!", QMessageBox.Yes)
        except:
            QMessageBox.information(self, "错误", "与服务器通讯失败!", QMessageBox.Yes)

        self.lie_username.setText('')
        self.lie_password.setText('')
        self.lie_password2.setText('')
        self.cbx_gm.setChecked(False)
        self.cbx_nu.setChecked(False)


    def toLogin(self):
        self.mc.nextPage = 'loginPage'
        self.close()

    def closeEvent(self, event):
        if not self.mc.nextPage:
            sys.exit()

    def run(self):
        self.mc.nextPage = None
        self.exec_()