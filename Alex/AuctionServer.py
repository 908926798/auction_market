# coding=utf-8
from time import sleep, ctime
import threading
import socket
import requests
import json

import mysql.connector

config = {
   'host': '192.168.43.23',
   'user': 'root',
   'password': 'yueyue',
   'port': 3306,
   'database': 'auc',
   'charset': 'utf8'
}
cnn = mysql.connector.connect(**config)
cursor = cnn.cursor(buffered=True)

flag = 0
class Auction(object):
    def __init__(self,port,id):
        self.mydict = dict()
        self.mylist = list()
        self.update_price = ['', 0]  # initial the name and price
        self.remainTime = 100  # record the number of the guests.when num=1,start the countdown
        self.port=port

        self.message = id
        self.startAuction()
        self.flag = 0

    def codedown(self):
        listen = threading.Thread(target=self.listen, args=())
        listen.setDaemon(True)
        listen.start()
        while True:
            # if self.remainTime != -1 and self.remainTime != 999:
            if self.remainTime != -1:
                sleep(1)
                self.remainTime -= 1
                print(self.remainTime)
                self.send('t'+str(self.remainTime))
            else:

                cursor.execute('select seller_name_id,lastbid_username,lastprice from database_goods WHERE G_number=%s',(self.message,))
                message = cursor.fetchall()

                cursor.execute('UPDATE database_user SET assets = assets + %s  where username = %s', (message[0][2],message[0][0],))
                cursor.execute('UPDATE database_user SET assets = assets - %s  where username = %s',
                               (message[0][2], message[0][1],))

                cursor.execute('UPDATE database_goods SET status = "end" where G_number = %s', (self.message,))
                cnn.commit()
                self.send('e')
                return

    def send(self,whatToSay):#can be used several times
        for c in self.mylist:
            try:
                c.send(whatToSay.encode())
            except:
                pass


    def startAuction(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 获取本机电脑名
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        self.sock.bind((ip, self.port))
        self.sock.listen(20)

        codethread = threading.Thread(target=self.codedown, args=())
        codethread.setDaemon(True)
        codethread.start()
        codethread.join()
        print(str(self.message) + '号商品 拍卖结束啦')

    def listen(self):
        while True:
            connection, addr = self.sock.accept()

            username = connection.recv(1024).decode()
            print(username)
            self.mydict[connection.fileno()] = username
            self.mylist.append(connection)

            print(self.mydict.values())
            # self.send('u'+)

            mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()


    def subThreadIn(self,myconnection, connNumber): #mulitiple threads
        while True:
            recvedMsg = myconnection.recv(1024).decode()
            if recvedMsg:
                self.send('p'+self.mydict[connNumber]+':'+recvedMsg)
                cursor.execute('UPDATE database_goods SET lastbid_username = %s WHERE G_number = %s',(self.mydict[connNumber], self.message))
                cursor.execute('UPDATE database_goods SET lastprice = %s WHERE G_number = %s',(recvedMsg, self.message))
                cursor.execute('UPDATE database_goods SET lastbid_time = now() where G_number = %s', (self.message,))
                cnn.commit()
                print(self.mydict[connNumber], ':', recvedMsg)
                self.remainTime=20 #update the codedown


def newAuction(id):
    Auction(5000 + int(id) % 60000, id)

def auctionControl():
    cnn = mysql.connector.connect(**config)
    cursor = cnn.cursor(buffered=True)
    while True:
        # try:
        cursor.execute('select G_number from database_goods WHERE status="ready"')
        message = cursor.fetchall()
        print(message)
        if message != []:
            for i in range(len(message)):
                print(message[i][0])
                cursor.execute('UPDATE database_goods SET status = "in" where G_number = %s', (message[i][0],))
                cnn.commit()

                mythread = threading.Thread(target=newAuction, args=(message[i][0],))
                mythread.setDaemon(True)
                mythread.start()

        cnn.close()
        cnn = mysql.connector.connect(**config)
        cursor = cnn.cursor(buffered=True)
        # except:
        #     print('错误')
        sleep(1)


if __name__ == '__main__':
    # 主线程
    t = threading.Thread(target=auctionControl, args=())
    t.start()
    t.join()
