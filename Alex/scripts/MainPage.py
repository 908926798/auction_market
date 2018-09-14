from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

class MainPage(QWidget):
    close_signal = pyqtSignal()
    def __init__(self, parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(MainPage, self).__init__(parent)
        loadUi('test1.ui',self)

    def closeEvent(self, event):
        self.close_signal.emit()
        self.close()
