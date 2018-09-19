from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import sys
import Item
import ChatPage
import SellPage
import requests
import json

class MainPage(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(MainPage, self).__init__(parent)
        loadUi('UI/mainPage.ui',self)
        self.mc = mc
        self.mc.mainPage = self
        self.itemWidget = QWidget()
        self.sca.setWidget(self.itemWidget)
        self.vLayout = QVBoxLayout(self.itemWidget)
        self.btn_state1.clicked.connect(self.toState1)
        self.btn_state2.clicked.connect(self.toState2)
        self.btn_state3.clicked.connect(self.toState3)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_addMoney.clicked.connect(self.addMoney)
        self.btn_startChat.clicked.connect(self.startChat)
        self.btn_sell.clicked.connect(self.sell)
        self.btn_fresh.clicked.connect(self.getChat)

    def toState1(self):
        self.mc.searchState = 1
        self.getState()

    def toState2(self):
        self.mc.searchState = 2
        self.getState()

    def toState3(self):
        self.mc.searchState = 3
        self.getState()

    def getItemInfo(self):
        self.mc.items = []
        ##########################
        # 访问主服务器 获取商品信息
        ##########################
        url = self.mc.url + '/goods?'
        url += 'status=' + str(self.mc.searchState)
        try:
            res = requests.get(url)
            result = json.loads(res.text)

            for x in result:
                self.mc.items.append(x)
            print(self.mc.items)
        except:
            pass

    def getState(self):
        self.setLine()
        self.getItemInfo()
        self.itemWidget.destroy()
        self.itemWidget = QWidget()
        self.sca.setWidget(self.itemWidget)
        self.vLayout = QVBoxLayout(self.itemWidget)
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.setSpacing(0)
        ##########################
        for i in range(len(self.mc.items)):
            if self.mc.searchState == 1:
                item = Item.Item1(self.mc,self.mc.items[i])
            if self.mc.searchState == 2:
                item = Item.Item2(self.mc,self.mc.items[i])
            if self.mc.searchState == 3:
                item = Item.Item3(self.mc,self.mc.items[i])
            # item.setStyleSheet("background-color:rgb(230,255,255)")
            item.setMinimumSize(521, 100)
            self.vLayout.addWidget(item, alignment=Qt.AlignTop)
        self.vLayout.addStretch(1)

    def setLine(self):
        self.lin.setGeometry(290 + (self.mc.searchState-1)*140,170,20,31)

    def logout(self):
        self.mc.username = None
        self.mc.nextPage = 'loginPage'
        self.close()

    def addMoney(self):
        if self.lie_addMoney.text().isdigit():
            self.mc.money += int(self.lie_addMoney.text())
        else:
            QMessageBox.information(self, "错误", "请输入正确金额！\n（目前只支持整数金额）",QMessageBox.Yes)

        url = self.mc.url + '/money/'
        info = {'username':self.mc.username,
                'money': int(self.lie_addMoney.text())}
        try:
            res = requests.post(url,data=info)
            # print(res.text)
            result = json.loads(res.text)
            if result['status']:
                QMessageBox.information(self, "成功", "充值成功!", QMessageBox.Yes)

                self.mc.money = result['money']
                self.lie_addMoney.setText('')
                self.lbl_money.setText(str(self.mc.money) + ' 元')
        except:
            self.lie_addMoney.setText('')
            QMessageBox.information(self, "错误", "冲的钱太多啦!", QMessageBox.Yes)

    def startChat(self):
        if not self.lwg_other.selectedItems():
            QMessageBox.information(self, "错误", "请选择一个用户!",QMessageBox.Yes)
            return
        other = self.lwg_other.selectedItems()[0].text()
        #########################################
        #开始p2p
        #########################################
        self.mc.chatOther = other
        self.mc.chatState = 's'

        self.mc.otherIP = self.mc.chats[self.lwg_other.selectedItems()[0].text()]
        ChatPage.ChatPage(self.mc).run()
        QMessageBox.information(self, "结束", "聊天已结束!", QMessageBox.Yes)

        # self.mc.nextPage = 'chatPage'
        # self.close()

    def closeEvent(self, event):
        if not self.mc.nextPage:
            sys.exit()

    def sell(self):
        SellPage.SellPage(self.mc).run()

    def getChat(self):
        for i in range(self.lwg_other.count()):
            self.lwg_other.takeItem(0)

        url = self.mc.url + '/chat?'
        url += 'username=' + self.mc.username
        try:
            res = requests.get(url)
            result = json.loads(res.text)
            for x in result:
                print(x)
                print(x['sourceName'])
                self.mc.chats[x['sourceName']] = x['sourceIP']
                self.lwg_other.addItem(x['sourceName'])
        except:
            print('error')


    def run(self):
        self.mc.nextPage = None
        self.lbl_username.setText(self.mc.username)
        #填写角色
        r = ''
        for x in self.mc.roles:
            r += x + '\n'
        self.lbl_roles.setText(r)
        #判断是否管理员
        if not '商品管理员' in self.mc.roles:
            self.btn_state1.setEnabled(False)

        self.lbl_money.setText(str(self.mc.money) + ' 元')
        self.exec_()
