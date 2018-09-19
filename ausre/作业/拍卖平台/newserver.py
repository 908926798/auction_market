#coding:utf-8
import socket
import threading
import sys
import time
import mysql.connector
import os
import signal

reload(sys)
sys.setdefaultencoding('utf8')
#message=raw_input("please input the commodity you what to trade:")#to get the commodity's information

#config = {
#    'host': '192.168.1.26',
#    'user': 'root',
#    'password': 'yueyue',
#    'port': 3306,
#    'database': 'auc',
#    'charset': 'utf8'
#}
#cnn = mysql.connector.connect(**config)
#cursor = cnn.cursor(buffered=True)

class sell(object):
    def __init__(self,message,port):
        self.mydict = dict()
        self.mylist = list()
        self.update_price = ['', 0]  # initial the name and price
        self.ncount = ["surplus_transaction_time:", 9999]  # record the number of the guests.when num=1,start the countdown
        self.message=message
        self.port=port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', port))
        self.sock.listen(5)
        print('Server', socket.gethostbyname('localhost'), 'listening ...')

    def tellOthers(self,exceptNum, whatToSay):  # can be used several times
        for c in self.mylist:
            if c.fileno() != exceptNum:
                try:
                    c.send(whatToSay.encode())
                except:
                    pass

    def tellOne(self,exceptNum,whatToSay):#can be used several times
        for c in self.mylist:
            if c.fileno()== exceptNum:
                try:
                    c.send(whatToSay.encode())
                    break
                except:
                    pass

    def telltoALL(self,whatToSay):#can be used several times
        for c in self.mylist:
            try:
                c.send(whatToSay.encode())
            except:
                pass

    def subThreadIn(self,myconnection, connNumber): #mulitiple threads
        nickname = myconnection.recv(1024).decode()
        self.mydict[myconnection.fileno()] = nickname
        self.mylist.append(myconnection)
        print('connection', connNumber, ' has nickname :', nickname)
        self.tellOthers(connNumber, '\n'+"[[system hints：" + self.mydict[connNumber] + " enters chatroom]]")
        if self.ncount[1]==-1:
            self.tellOne(connNumber,'\n'+"[[system hints:the trade is closed]]")
            return
        else:
            self.tellOne(connNumber,'\n'+"[[system hints:Commodities being traded: "+self.message+"]]") #tell the freshman the information of commodity
        while True:
            try:
                if self.ncount[1]==-1:
                    break
                else:
                    recvedMsg = myconnection.recv(1024).decode()
                    if recvedMsg:
                        print(self.mydict[connNumber], ':', recvedMsg)#print the connector's name and bid price
                #then we update the updated_price and the duration
                    if int(recvedMsg)>self.update_price[1]:
                        self.update_price[0]=self.mydict[connNumber]
                        self.update_price[1]=int(recvedMsg)
                        self.ncount[1]=5 #update the codedown
                        print("the updated price is:",self.update_price[0],":",self.update_price[1])
                        try:
                            self.tellOthers(connNumber,'\n'+ self.mydict[connNumber] + ' :' + recvedMsg)
                        except:
                            pass
        #except (OSError, ConnectionResetError):
            except:
                try:
                    self.mylist.remove(myconnection)
                except:
                    pass
                print(self.mydict[connNumber], 'exit, ', len(self.mylist), ' person left')
                self.tellOthers(connNumber, '\n'+'[[system hints：' + self.mydict[connNumber] + ' leaves]]')
                myconnection.close()
                return

    def codedown(self,count):
        while True:
            if self.ncount[1]==-1:
                break
            if self.ncount[1]!=-1 and self.ncount[1]!=9999:
                while (count <= self.ncount[1]):
                    time.sleep(1)
                    self.ncount[1]-=1
                return

    def tellAll(self,whatToSay): #announce the codedown
        numb=0
        while True:
            if self.ncount[1]==-1:
                break
            else:
                if whatToSay[1]%10==0 and numb==0:
                    numb=1
                    for c in self.mylist:
                        try:
                            c.send(('\n'+'[[system hints:'+whatToSay[0]+str(whatToSay[1])+']]').encode())
                        except:
                            return
                else:
                    if whatToSay[1]%10!=0:
                        numb=0

    def record(self):
        while True:
            if self.ncount[1]==-1:
                self.telltoALL('\n' + "[[system hints: " + self.update_price[0] + " finnaly get the commodity " + "by " + str(self.update_price[1]) + " yuan" + "]]")
                self.telltoALL("[[system hints:the trade is closed]]")
                #cursor.execute('UPDATE database_goods SET lastbid_username = %s WHERE goods_name = %s',(self.update_price[0],self.message))
                #cursor.execute('UPDATE database_goods SET lastprice = %s WHERE goods_name = %s',(self.update_price[1],self.message))
                #cursor.execute('UPDATE database_goods SET lastbid_time = now() where goods_name = %s',(self.message,))
                #cursor.execute('UPDATE database_goods SET status = "end" where goods_name = %s', (self.message,))
                #cnn.commit()
                break

    def fun(self):
        num = 0
        codethread = threading.Thread(target=self.codedown, args=(num,))
        codethread.setDaemon(True)
        codethread.start()
        announcethread = threading.Thread(target=self.tellAll, args=(self.ncount,))
        announcethread.setDaemon(True)
        announcethread.start()
        recordthread = threading.Thread(target=self.record, args=())
        recordthread.setDaemon(True)
        recordthread.start()
        while True:
            if self.ncount[1] == -1:
                break
            connection, addr = self.sock.accept()
            try:
                buf = connection.recv(1024).decode()
                if buf == '1':
                    connection.send(b'welcome to server!')
                    mythread = threading.Thread(target=self.subThreadIn, args=(connection, connection.fileno()))
                    mythread.setDaemon(True)
                    mythread.start()
                else:
                    connection.send(b'please go out!')
                    connection.close()
            except:
                pass

if __name__=='__main__':
    me=[]
    message = ["pig", "dog"]
    while True:
        try:
            for i in range(len(message)):
                me.append(sell(message[i],5550+10*i))
                me[i].fun()
                #还是阻塞。无法返回a。怀疑是因为socke没法关闭
                print "ok"
        except:
            pass

#python newserver.py