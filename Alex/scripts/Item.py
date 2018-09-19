from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import socket
import requests
import json
import ChatPage
import sys

class Item1(QWidget):
    def __init__(self, mc,item,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(Item1, self).__init__(parent)
        loadUi('UI/item1.ui', self)
        self.mc = mc
        self.itemInfo = item
        self.lbl_itemName.setText(self.itemInfo['goods_name'])
        self.lbl_seller.setText(self.itemInfo['seller_name'])
        self.lbl_startPrice.setText(str(self.itemInfo['minimum_price']))
        self.btn_itemDetail.clicked.connect(self.itemDetail)
        self.btn_chatSeller.clicked.connect(self.chatSeller)
        self.btn_agree.clicked.connect(self.agree)
        self.btn_disagree.clicked.connect(self.disagree)

    def itemDetail(self):
        ItemDetail(self.mc,[]).run()

    def chatSeller(self):
        url = self.mc.url + '/chat/'
        # 获取本机电脑名
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)

        info = {'fromname': self.mc.username,
                'toname': self.itemInfo['seller_name'],
                'fromip': ip}

        # try:
        res = requests.post(url, data=info)
        # print(res.text)
        result = json.loads(res.text)
        if result['status']:
            print(1)
            self.mc.chatOther = self.itemInfo['seller_name']
            self.mc.chatState = 'r'
            self.mc.otherIP = ip
            ChatPage.ChatPage(self.mc).run()
        else:
            QMessageBox.information(self, "错误", "无法与该卖家通信!", QMessageBox.Yes)
        # except:
        #     QMessageBox.information(self, "错误", "与服务器通讯失败!", QMessageBox.Yes)

    def agree(self):
        pass

    def disagree(self):
        pass

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
        self.btn_itemDetail.clicked.connect(self.itemDetail)

    def itemDetail(self):
        ItemDetail(self.mc,[]).run()


    def joinAuction(self):
        self.mc.acutionItem = self.itemInfo['itemName']
        self.mc.nextPage = 'auctionPage'
        self.mc.mainPage.close()

class Item3(QWidget):
    def __init__(self, mc,i,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(Item3, self).__init__(parent)
        loadUi('UI/item3.ui',self)
        self.mc = mc
        self.itemInfo = mc.items[i]
        self.lbl_itemName.setText(self.itemInfo['itemName'])
        self.lbl_lastBidder.setText(self.itemInfo['lastBidder'])
        self.lbl_startTime.setText(self.itemInfo['endTime'])
        self.lbl_curPrice.setText(self.itemInfo['curPrice'])
        self.btn_itemDetail.clicked.connect(self.itemDetail)

    def itemDetail(self):
        ItemDetail(self.mc,[]).run()

class ItemDetail(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,itemInfo,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(ItemDetail, self).__init__(parent)
        loadUi('UI/itemDetail.ui',self)
        # self.btn_toRegister.clicked.connect(self.toRegister)
        self.mc = mc
        self.btn_ok.clicked.connect(self.ok)

    def ok(self):
        self.close()

    def run(self):
        self.exec_()
