#coding:utf-8
import socket
import threading
import sys
import time
from multiprocessing import Process
from multiprocessing import Pool
import os

reload(sys)
sys.setdefaultencoding('utf8')
#message=raw_input("please input the commodity you what to trade:")#to get the commodity's information
message=["vases","book","pig"]

def run_proc(message,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(5)
    print('Server', socket.gethostbyname('localhost'), 'listening ...')
    mydict = dict()
    mylist = list()
    update_price=['',0]#initial the name and price
    ncount=["surplus_transaction_time:",9999] #record the number of the guests.when num=1,start the countdown

    def tellOthers(exceptNum, whatToSay):#can be used several times
        for c in mylist:
            if c.fileno() != exceptNum:
                try:
                    c.send(whatToSay.encode())
                except:
                    pass

    def tellOne(exceptNum,whatToSay):#can be used several times
        for c in mylist:
            if c.fileno()== exceptNum:
                try:
                    c.send(whatToSay.encode())
                    break
                except:
                    pass

    def telltoALL(whatToSay):#can be used several times
        for c in mylist:
            try:
                c.send(whatToSay.encode())
            except:
                pass


    def subThreadIn(myconnection, connNumber): #mulitiple threads
        nickname = myconnection.recv(1024).decode()
        mydict[myconnection.fileno()] = nickname
        mylist.append(myconnection)
        print('connection', connNumber, ' has nickname :', nickname)
        tellOthers(connNumber, '\n'+"[[system hints：" + mydict[connNumber] + " enters chatroom]]")
        tellOne(connNumber,'\n'+"[[system hints:Commodities being traded: "+message+"]]") #tell the freshman the information of commodity
        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()
                if recvedMsg:
                    print(mydict[connNumber], ':', recvedMsg)#print the connector's name and bid price
                #then we update the updated_price and the duration
                    if ncount[1]==-1:
                        try:
                            tellOne(connNumber, "sorry the trade is closed")
                        except:
                            pass
                    if int(recvedMsg)>update_price[1]:
                        if ncount[1]!=-1:
                            update_price[0]=mydict[connNumber]
                            update_price[1]=int(recvedMsg)
                            ncount[1]=60 #update the codedown
                            print("the updated price is:",update_price[0],":",update_price[1])
                            try:
                                tellOthers(connNumber,'\n'+ mydict[connNumber] + ' :' + recvedMsg)
                            except:
                                pass


        #except (OSError, ConnectionResetError):
            except:
                try:
                    mylist.remove(myconnection)
                except:
                    pass
                print(mydict[connNumber], 'exit, ', len(mylist), ' person left')
                tellOthers(connNumber, '\n'+'[[system hints：' + mydict[connNumber] + ' leaves]]')
                myconnection.close()
                return

    def codedown(count):
        while True:
            if ncount[1]!=-1 and ncount[1]!=9999:
                while (count <= ncount[1]):
                    time.sleep(1)
                    ncount[1]-=1
                print 'done'
                print ncount[1]
                telltoALL('\n'+"[[system hints: "+update_price[0]+" finnaly get the commodity "+"by "+str(update_price[1])+" yuan"+"]]")
                break
    num=0
    codethread = threading.Thread(target=codedown, args=(num,))
    codethread.setDaemon(True)
    codethread.start()

    def tellAll(whatToSay): #announce the codedown
        numb=0
        while True:
            if whatToSay[1]%10==0 and numb==0:
                numb=1
                for c in mylist:
                    try:
                        c.send(('\n'+'[[system hints:'+whatToSay[0]+str(whatToSay[1])+']]').encode())
                    except:
                        pass
            else:
                if whatToSay[1]%10!=0:
                    numb=0

    announcethread = threading.Thread(target=tellAll, args=(ncount,))
    announcethread.setDaemon(True)
    announcethread.start()

    while True:
        if ncount[1]==-1:
            sock.shutdown(2)
            sock.close()
            break
        else:
            connection, addr = sock.accept()
            try:
                buf = connection.recv(1024).decode()
                if buf == '1':
                    connection.send(b'welcome to server!')
                    mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
                    mythread.setDaemon(True)
                    mythread.start()
                else:
                    connection.send(b'please go out!')
                    connection.close()
            except:
                pass

if __name__=='__main__':
    po=Pool(3)
    po.apply_async(run_proc,(message[0],5550))
    po.apply_async(run_proc,(message[1],6000))
    po.apply_async(run_proc,(message[2],8080))
    po.close()
    po.join()
