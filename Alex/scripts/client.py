import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import LoginPage
import RegisterPage
import MainPage
import AuctionPage

class MainController():
    def __init__(self):
        self.url = 'http://192.168.1.4:8000'
        self.username = None
        self.roles = []
        self.money = None
        self.mainServerIP = None
        self.pages = {}
        self.nextPage = None
        self.searchState = 1
        self.items = []
        self.mainPage = None
        self.auctionItem = 'df'
        self.chatOther = '1'
        self.chatState = 's'
        self.otherIP = None
        self.chats = {}

if __name__ == "__main__":
    App = QApplication(sys.argv)

    mc = MainController()
    #登录和注册
    mc.pages['registerPage'] = RegisterPage.RegisterPage(mc)
    mc.pages['loginPage'] = LoginPage.LoginPage(mc)
    mc.pages['mainPage'] = MainPage.MainPage(mc)
    mc.pages['auctionPage'] = AuctionPage.AuctionPage(mc)

    mc.nextPage = 'loginPage'

    while(mc.nextPage):
        mc.pages[mc.nextPage].run()

    sys.exit(App.exec_())