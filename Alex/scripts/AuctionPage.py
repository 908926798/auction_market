from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys
import Item
import ChatPage

class AuctionPage(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(AuctionPage, self).__init__(parent)
        loadUi('UI/auctionPage.ui',self)
        self.mc = mc
        self.mc.mainPage = self

    def leaveAuction(self):
        self.mc.nextPage = 'mainPage'
        self.close()

    def closeEvent(self, event):
        if not self.mc.nextPage:
            sys.exit()

    def run(self):
        self.mc.nextPage = None
        self.lbl_username.setText(self.mc.username)
        self.lbl_money.setText(str(self.mc.money) +' 元')
        for i in range(100):
            self.lwg_other.addItem(str(i))

        self.exec_()