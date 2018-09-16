import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import LoginPage
import RegisterPage
import MainPage

class MainController():
    def __init__(self):
        self.username = None
        self.mainServerIP = None
        self.pages = {}
        self.nextPage = None
        self.exit = False

if __name__ == "__main__":
    App = QApplication(sys.argv)

    mc = MainController()
    #登录和注册
    mc.pages['registerPage'] = RegisterPage.RegisterPage(mc)
    mc.pages['loginPage'] = LoginPage.LoginPage(mc)
    mc.pages['mainPage'] = MainPage.MainPage(mc)

    mc.nextPage = 'mainPage'

    while(mc.nextPage):
        mc.pages[mc.nextPage].run()

    sys.exit(App.exec_())