import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import LoginPage
import RegisterPage

if __name__ == "__main__":
    App = QApplication(sys.argv)

    #登录和注册
    registerPage = RegisterPage.RegisterPage()

    loginPage = LoginPage.LoginPage(registerPage)

    loginPage.pushButton.clicked.connect(loginPage.hide)
    loginPage.close_signal.connect(loginPage.close)

    loginPage.show()
    sys.exit(App.exec_())