from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys

class Item1(QWidget):
    def __init__(self, mc,i,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(Item1, self).__init__(parent)
        loadUi('UI/item1.ui',self)
        self.mc = mc
        self.itemInfo = mc.items[i]
        self.lbl_itemName.setText(self.itemInfo['itemName'])
        self.lbl_seller.setText(self.itemInfo['seller'])
        self.lbl_startTime.setText(self.itemInfo['startTime'])
        self.lbl_startPrice.setText(self.itemInfo['startPrice'])
        self.btn_chatSeller.clicked.connect(self.chatSeller)

    def chatSeller(self):
        self.mc.chatOther = self.itemInfo['seller']
        self.mc.nextPage = 'chatPage'
        self.mc.mainPage.close()


class Item2(QWidget):
    def __init__(self, mc,i,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(Item2, self).__init__(parent)
        loadUi('UI/item2.ui',self)
        self.mc = mc
        self.itemInfo = mc.items[i]
        self.lbl_itemName.setText(self.itemInfo['itemName'])
        self.lbl_lastBidder.setText(self.itemInfo['lastBidder'])
        self.lbl_startTime.setText(self.itemInfo['startTime'])
        self.lbl_curPrice.setText(self.itemInfo['curPrice'])
        self.btn_joinAuction.clicked.connect(self.joinAuction)

    def joinAuction(self):
        self.mc.acutionItem = self.itemInfo['itemName']
        self.mc.nextPage = 'auctionPage'
        self.mc.mainPage.close()
