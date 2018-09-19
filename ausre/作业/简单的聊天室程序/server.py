#coding:utf-8
import socket
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 5550))

sock.listen(5)
print('Server', socket.gethostbyname('localhost'), 'listening ...')

mydict = dict()
mylist = list()



def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum:
            try:
                c.send(whatToSay.encode())
            except:
                pass


def subThreadIn(myconnection, connNumber):
    nickname = myconnection.recv(1024).decode()
    mydict[myconnection.fileno()] = nickname
    mylist.append(myconnection)
    print('connection', connNumber, ' has nickname :', nickname)
    tellOthers(connNumber, "[[system hints：" + mydict[connNumber] + " enters chatroom]]")
    while True:
        try:
            recvedMsg = myconnection.recv(1024).decode()
            if recvedMsg:
                print(mydict[connNumber], ':', recvedMsg)
                tellOthers(connNumber, mydict[connNumber] + ' :' + recvedMsg)

        #except (OSError, ConnectionResetError):
        except:
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'exit, ', len(mylist), ' person left')
            tellOthers(connNumber, '[[system hints：' + mydict[connNumber] + ' leaves]]')
            myconnection.close()
            return


while True:
    connection, addr = sock.accept()
    print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        # connection.settimeout(5)
        buf = connection.recv(1024).decode()
        if buf == '1':
            connection.send(b'welcome to server!')

        #new thread
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()

        else:
            connection.send(b'please go out!')
            connection.close()
    except:
        pass