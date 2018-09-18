import socket
import time
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 8080))
sock.send(b'1')
print(sock.recv(1024).decode())
nickName = raw_input('input your nickname: ')
sock.send(nickName.encode())

def sendThreadFunc():
    while True:
        try:
            #myword = raw_input()
            #sock.send(myword.encode())
            while True:
                myword = None
                try:
                    myword = int(input("your bid:"))
                except:
                    print "invalid input:please input a num"
                    pass
                if type(myword) == int:
                    sock.send(str(myword).encode())
                    break
        except:
            print('Server failed!')
            break



def recvThreadFunc():
    while True:
        try:
            otherword = sock.recv(1024)
            if otherword:
                print(otherword.decode())
            else:
                pass
        #except ConnectionAbortedError:
        #    print('Server closed this connection!')

        #except ConnectionResetError:
        #    print('Server is closed!')
        except:
            print('Server failed!')
            break



th1 = threading.Thread(target=sendThreadFunc)
th2 = threading.Thread(target=recvThreadFunc)
threads = [th1, th2]

for t in threads:
    t.setDaemon(True)
    t.start()
t.join()