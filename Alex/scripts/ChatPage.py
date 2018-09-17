from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
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
        self.msgs = ''
        self.btn_endChat.clicked.connect(self.endChat)
        # self.btn_send.clicked.connect(self.send)
        self.lie.returnPressed.connect(self.send)

    def endChat(self):
        self.close()

    def send(self):
        self.txb.append(self.mc.username + ' :\n' + self.lie.text() + '\n')
        self.txb.moveCursor(QTextCursor.End)
        self.lie.setText('')

    def run(self):
        self.lbl_other.setText(self.mc.chatOther)
        self.exec_()