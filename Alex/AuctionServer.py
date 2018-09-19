# coding=utf-8
from time import sleep, ctime
import threading
import socket
import json

flag = 0
class Auction(object):
    def __init__(self,port):
        self.mydict = dict()
        self.mylist = list()
        self.update_price = ['', 0]  # initial the name and price
        self.remainTime = 100  # record the number of the guests.when num=1,start the countdown
        self.port=port
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
                return

    def send(self,whatToSay):#can be used several times
        for c in self.mylist:
            try:
                c.send(whatToSay.encode())
            except:
                pass


    def startAuction(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', self.port))
        self.sock.listen(10)

        codethread = threading.Thread(target=self.codedown, args=())
        codethread.setDaemon(True)
        codethread.start()
        codethread.join()
        print('的拍卖结束啦')

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
                print(self.mydict[connNumber], ':', recvedMsg)
                self.remainTime=3 #update the codedown

    def finish(self):
        self.send('e')
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        for c in self.mylist:
            try:
                c.shutdown(socket.SHUT_RDWR)
            except:
                pass
        self.flag = 1

def auctionControl():
    a = Auction(5550)

if __name__ == '__main__':
    # 主线程
    t = threading.Thread(target=auctionControl, args=())
    t.start()
    t.join()
