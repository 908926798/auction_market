import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import LoginPage
import RegisterPage
import MainPage
import ChatPage
import AuctionPage

class MainController():
    def __init__(self):
        self.url = 'http://192.168.43.17:8000'
        self.username = '我'
        self.roles = ['商品管理员1','普通用户']
        self.money = 40
        self.mainServerIP = None
        self.pages = {}
        self.nextPage = None
        self.searchState = 1
        self.items = []
        self.chatOther = '1'
        self.mainPage = None
        self.auctionItem = 'df'

if __name__ == "__main__":
    App = QApplication(sys.argv)

    mc = MainController()
    #登录和注册
    mc.pages['registerPage'] = RegisterPage.RegisterPage(mc)
    mc.pages['loginPage'] = LoginPage.LoginPage(mc)
    mc.pages['mainPage'] = MainPage.MainPage(mc)
    mc.pages['chatPage'] = ChatPage.ChatPage(mc)
    mc.pages['auctionPage'] = AuctionPage.AuctionPage(mc)

    mc.nextPage = 'registerPage'

    while(mc.nextPage):
        mc.pages[mc.nextPage].run()

    sys.exit(App.exec_())