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
        try:
            self.bwThread = ListenThread(self.mc,self)
            self.bwThread.start()
        except:
            pass

    def require(self):
        self.bwThread = RequireThread(self.mc, self)
        self.bwThread.start()

    def endChat(self):
        try:
            self.bwThread.send('TypeError: information')
        except:
            pass
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
        if self.mc.chatState == 'r':
            self.lbl_other.setText('等待   ' + self.mc.chatOther + " 同意聊天请求")
            self.listen()

        if self.mc.chatState == 's':
            self.lbl_other.setText('正在与   ' + self.mc.chatOther + "   聊天")
            self.require()

        self.exec_()

    def end(self):
        print('end')
        #QMessageBox.information(self, "错误", "连接已断开!", QMessageBox.Yes)
        self.close()

    def closeEvent(self, event):
        try:
            self.bwThread.send('TypeError: information')
        except:
            pass


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
        self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((self.mc.otherIP, self.mc.port))
        sock.listen(5)

        # shou
        connection, addr = sock.accept()
        self.cp.lbl_other.setText('正在与   ' + self.mc.chatOther + "   聊天")
        self.connection = connection
        # try:
        # buf = connection.recv(1024).decode()
        # if buf == '1':
        # connection.send(b'welcome to server!')

        # new thread
        mythread = threading.Thread(target=self.subThreadIn, args=())
        mythread.setDaemon(True)
        mythread.start()

        mythread.join()

    def subThreadIn(self):
        while True:
            try:
                recvedMsg = self.connection.recv(1024).decode()
                print(recvedMsg)
                if recvedMsg != 'TypeError: information':
                    self.cp.txb.append(recvedMsg)
                    self.cp.txb.moveCursor(QTextCursor.End)
                else:
                    self.connection.close()
                    self.socket.close()
                    self.cp.end()

            except:
                self.socket.close()
                self.connection.close()

    def send(self,msg):

        try:
            if self.connection:
                self.connection.send(msg.encode())
        except:
            self.connection.close()
            self.socket.close()
            self.cp.end()

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
        self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        ip,port = self.mc.otherIP.split(':')
        sock.connect((ip, int(port)))

        self.connection = sock

        mythread = threading.Thread(target=self.subThreadIn, args=())
        mythread.setDaemon(True)
        mythread.start()

        mythread.join()

    def subThreadIn(self):
        while True:
            try:
                recvedMsg = self.connection.recv(1024).decode()
                print(recvedMsg)
                if recvedMsg != 'TypeError: information':
                    self.cp.txb.append(recvedMsg)
                    self.cp.txb.moveCursor(QTextCursor.End)
                else:
                    self.connection.close()
                    self.cp.end()
            except:
                self.connection.close()

    def send(self,msg):
        try:
            if self.connection:
                self.connection.send(msg.encode())
        except:
            self.connection.close()
            self.cp.end()