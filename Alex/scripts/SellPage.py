from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import requests
import json
import sys

class SellPage(QDialog):
    close_signal = pyqtSignal()
    def __init__(self, mc,parent=None):
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(SellPage, self).__init__(parent)
        loadUi('UI/sellPage.ui',self)
        # self.btn_toRegister.clicked.connect(self.toRegister)
        self.mc = mc
        self.btn_upLoad.clicked.connect(self.upLoad)
        # self.btn_send.clicked.connect(self.send)

    def upLoad(self):
        if not self.lie_itemname.text() or not self.lie_price.text() or not self.txe_detail.toPlainText():
            QMessageBox.information(self, "错误", "信息不能为空!", QMessageBox.Yes)
            return

        if not self.lie_price.text().isdigit():
            QMessageBox.information(self, "错误", "价格必须为数字!", QMessageBox.Yes)
            return
        url = self.mc.url + '/goods/'
        info = {'username':self.mc.username,
                'itemname': self.lie_itemname.text(),
                'price' : self.lie_price.text(),
                'detail' : self.txe_detail.toPlainText()}

        try:
            res = requests.post(url,data=info)
            # print(res.text)
            result = json.loads(res.text)
            if result['status']:
                QMessageBox.information(self, "成功", "成功！商品 " + self.lie_itemname.text() + " 正在等待审核!", QMessageBox.Yes)
                self.close()
            else:
                QMessageBox.information(self, "错误", "无法上架!", QMessageBox.Yes)
        except:
            QMessageBox.information(self, "错误", "与服务器通讯失败!", QMessageBox.Yes)

        self.lie_itemname.setText('')
        self.lie_price.setText('')
        self.txe_detail.setText('')

    def run(self):
        self.exec_()