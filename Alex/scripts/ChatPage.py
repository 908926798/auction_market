# coding:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import socket
import threading
import sys


class ChatPage(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(ChatPage, self).__init__(parent)
        loadUi('UI/chatPage.ui',self)
        # self.btn_toRegister.clicked.connect(self.toRegister)
        self.mc = mc
        self.msg = ''
        self.btn_endChat.clicked.connect(self.endChat)
        # self.btn_send.clicked.connect(self.send)
        self.lie.returnPressed.connect(self.send)
        self.connection = None
        self.socket = None
        self.state = 0


    def listen(self):
        self.bwThread = ListenThread(self.mc,self)
        self.bwThread.start()

    def require(self):
        self.bwThread = RequireThread(self.mc, self)
        self.bwThread.start()

    def endChat(self):
        if self.state == 0:
            self.lbl_other.setText('等待 ' + self.mc.chatOther + " 响应聊天请求")
            self.btn_endChat.setText('结束聊天')
            self.listen()
            self.state = 1
        else:
            self.close()

    def send(self):
        msg = self.mc.username + ' :\n' + self.lie.text() + '\n'
        self.txb.append(msg)
        self.txb.moveCursor(QTextCursor.End)
        self.lie.setText('')
        self.bwThread.send(msg)

    def run(self):
        # self.lbl_other.setText(self.mc.chatOther)
        self.lbl_other.setText('未连接')

        if self.mc.chatState == 's':
            self.lbl_other.setText('正在与   ' + self.mc.chatOther + "   聊天")
            self.require()

        self.exec_()

#继承 QThread 类
class ListenThread(QThread):
    """docstring for BigWorkThread"""
    def __init__(self, mc,cp,parent=None):
        super(ListenThread, self).__init__(parent)
        self.mc = mc
        self.cp = cp

    #重写 run() 函数，在里面干大事。
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.mc.otherIP, 5550))
        sock.listen(5)

        # shou
        connection, addr = sock.accept()
        self.cp.lbl_other.setText('正在与   ' + self.mc.chatOther + "   聊天")
        self.connection = connection
        print("ccc")
        print(connection)
        # try:
        buf = connection.recv(1024).decode()
        # if buf == '1':
        connection.send(b'welcome to server!')

        # new thread
        mythread = threading.Thread(target=self.subThreadIn, args=())
        mythread.setDaemon(True)
        mythread.start()

        mythread.join()

    def subThreadIn(self):
        while True:
            try:
                recvedMsg = self.connection.recv(1024).decode()
                if recvedMsg:
                    self.cp.txb.append(recvedMsg)
                    self.cp.txb.moveCursor(QTextCursor.End)
            except:
                self.connection.close()
                return

    def send(self,msg):
        if self.connection:
            self.connection.send(msg.encode())


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

        print(self.mc.otherIP)
        sock.connect((self.mc.otherIP, 5550))
        sock.send(b'1')
        print(sock.recv(1024).decode())

        self.connection = sock
        print("ccc")
        print(sock)

        mythread = threading.Thread(target=self.subThreadIn, args=())
        mythread.setDaemon(True)
        mythread.start()

        mythread.join()

    def subThreadIn(self):
        while True:
            try:
                recvedMsg = self.connection.recv(1024).decode()
                if recvedMsg:
                    self.cp.txb.append(recvedMsg)
                    self.cp.txb.moveCursor(QTextCursor.End)

            except:
                self.connection.close()
                return

    def send(self,msg):
        if self.connection:
            self.connection.send(msg.encode())
