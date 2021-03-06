from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import socket
import requests
import json
import ChatPage
import AuctionPage
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
        ItemDetail(self.mc,self.itemInfo).run()

    def chatSeller(self):
        url = self.mc.url + '/chat/'
        # 获取本机电脑名
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)

        info = {'fromname': self.mc.username,
                'toname': self.itemInfo['seller_name'],
                'fromip': ip+':'+str(self.mc.port)}

        # try:
        res = requests.post(url, data=info)
        # print(res.text)
        result = json.loads(res.text)
        if result['status']:

            self.mc.chatOther = self.itemInfo['seller_name']
            self.mc.chatState = 'r'
            self.mc.otherIP = ip
            try:
                ChatPage.ChatPage(self.mc).run()
                QMessageBox.information(self, "结束", "聊天已结束!", QMessageBox.Yes)
                self.mc.port += 1
            except:
                return

        else:
            QMessageBox.information(self, "错误", "无法与该卖家通信!", QMessageBox.Yes)

    def agree(self):
        self.judgeItem(1)

    def disagree(self):
        self.judgeItem(0)

    def judgeItem(self,r):
        url = self.mc.url + '/judgement/'
        info = {'G_number': self.itemInfo['G_number'],
                'result': r}
        try:
            res = requests.post(url, data=info)
            # print(res.text)
            result = json.loads(res.text)
            if result['status']:
                self.mc.mainPage.getState()
        except:
            QMessageBox.information(self, "错误", "通讯失败!", QMessageBox.Yes)


class Item2(QWidget):
    def __init__(self, mc,item,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(Item2, self).__init__(parent)
        loadUi('UI/item2.ui',self)
        self.mc = mc
        self.itemInfo = item
        self.lbl_itemName.setText(self.itemInfo['goods_name'])
        self.lbl_lastBidder.setText(self.itemInfo['lastbid_username'])
        if self.itemInfo['lastbid_username']:
            self.lbl_lastBidder.setText(self.itemInfo['lastbid_username'])
        else:
            self.lbl_lastBidder.setText('暂无')
        self.lbl_seller.setText(self.itemInfo['seller_name'])

        self.lbl_curPrice.setText(str(self.itemInfo['lastprice']))
        self.btn_joinAction.clicked.connect(self.joinAuction)
        self.btn_itemDetail.clicked.connect(self.itemDetail)

    def itemDetail(self):
        ItemDetail(self.mc,self.itemInfo).run()

    def joinAuction(self):
        if not '拍卖者' in self.mc.roles:
            QMessageBox.information(self, "错误", "您不是拍卖者，不能参与竞拍！", QMessageBox.Yes)
            return
        self.mc.curMoney = self.itemInfo['lastprice']
        self.mc.auctionItem = self.itemInfo
        AuctionPage.AuctionPage(self.mc).run()
        self.mc.mainPage.getState()
        self.mc.mainPage.getMoney()

class Item3(QWidget):
    def __init__(self, mc,item,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(Item3, self).__init__(parent)
        loadUi('UI/item3.ui',self)
        self.mc = mc
        self.itemInfo = item
        self.lbl_itemName.setText(self.itemInfo['goods_name'])
        self.lbl_lastBidder.setText(self.itemInfo['lastbid_username'])
        t = self.itemInfo['lastbid_time']
        if t:
            self.lbl_endTime.setText(t[0:10] + ' '+ t[11:19])
        else:
            self.lbl_endTime.setText('无')
        self.lbl_curPrice.setText(str(self.itemInfo['lastprice']))
        self.btn_itemDetail.clicked.connect(self.itemDetail)

    def itemDetail(self):
        ItemDetail(self.mc,self.itemInfo).run()

class ItemDetail(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,itemInfo,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(ItemDetail, self).__init__(parent)
        loadUi('UI/itemDetail.ui',self)
        # self.btn_toRegister.clicked.connect(self.toRegister)
        self.mc = mc
        self.itemInfo = itemInfo
        self.btn_ok.clicked.connect(self.ok)

    def ok(self):
        self.close()

    def run(self):

        url = self.mc.url + '/detail?'
        url += 'G_number=' + str(self.itemInfo['G_number'])
        try:
            res = requests.get(url)
            result = json.loads(res.text)[0]
            print(result)
        except:
            pass

        self.ID.setText(str(result['G_number']))
        self.itemName.setText(str(result['goods_name']))
        self.seller.setText(str(result['seller_name']))
        self.lastBidder.setText(str(result['lastbid_username']))
        self.lastTime.setText(str(result['lastbid_time']))
        self.lastPrice.setText(str(result['lastprice']))
        self.minPrice.setText(str(result['minimum_price']))
        self.state.setText(str(result['status']))
        self.detail.setText(str(result['detail']))

        self.exec_()
