from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import sys
import Item
import ChatPage
import socket
import threading

class AuctionPage(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(AuctionPage, self).__init__(parent)
        loadUi('UI/auctionPage.ui',self)
        self.mc = mc
        self.btn_bid.clicked.connect(self.bid)

    def bid(self):
        if not self.lie.text().isdigit():
            QMessageBox.information(self, "错误", "金额必须为数字", QMessageBox.Yes)
            return
        if int(self.lie.text()) < self.mc.curMoney:
            QMessageBox.information(self, "错误", "出价必须大于现价", QMessageBox.Yes)
            return
        if int(self.lie.text()) > self.mc.money:
            QMessageBox.information(self, "错误", "你没有这么多钱", QMessageBox.Yes)
            return

        self.bwThread.send(self.lie.text())
        self.lie.setText('')

    def leaveAuction(self):
        self.mc.nextPage = 'mainPage'
        self.close()

    def closeEvent(self, event):
        self.mc.nextPage = 'mainPage'
        self.close()

    def run(self):
        self.mc.nextPage = None
        self.lbl_username.setText(self.mc.username)
        self.lbl_money.setText(str(self.mc.money) +' 元')
        self.lbl_itemName.setText(str(self.mc.auctionItem['goods_name']))

        self.bwThread = RequireThread(self.mc, self)
        self.bwThread.start()

        #读取当前人数
        for i in range(100):
            self.lwg_other.addItem(str(i))

        self.exec_()


#继承 QThread 类
class RequireThread(QThread):
    """docstring for BigWorkThread"""
    def __init__(self, mc,cp,parent=None):
        super(RequireThread, self).__init__(parent)
        self.mc = mc
        self.cp = cp

    #重写 run() 函数，在里面干大事。
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = sock
        print(self.mc.auctionIP)
        print(5000 + self.mc.auctionItem['G_number'] % 60000)

        sock.connect((self.mc.auctionIP, 5000 + self.mc.auctionItem['G_number'] %60000))
        self.send(self.mc.username)

        mythread = threading.Thread(target=self.subThreadIn, args=())
        mythread.setDaemon(True)
        mythread.start()
        mythread.join()

    def subThreadIn(self):
        while True:
            try:
                recvedMsg = self.connection.recv(1024).decode()
                print(recvedMsg)
                self.handleMsg(recvedMsg)
            except:
                self.connection.close()

    def send(self,msg):
        try:
            if self.connection:
                self.connection.send(msg.encode())
        except:
            self.connection.close()
            self.cp.end()

    def handleMsg(self,msg):
        m = msg[1:]
        if msg[0] == 't':
            self.cp.lbl_remainTime.setText(m + ' S')
        if msg[0] == 'p':
            u,p = m.split(':')
            self.cp.txb.append('新出价人: ' + u + '  价格: ' + p +'元' )
            self.mc.curMoney = int(p)
            self.cp.txb.moveCursor(QTextCursor.End)
            self.cp.lbl_curPrice.setText(p+' 元')
        if msg[0] == 'e':
            self.cp.txb.append('当前竞拍已结束' )
            self.cp.txb.moveCursor(QTextCursor.End)
