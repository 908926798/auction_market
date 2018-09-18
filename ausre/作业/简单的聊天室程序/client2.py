import socket
import time
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 5550))
sock.send(b'1')
print(sock.recv(1024).decode())
nickName = raw_input('input your nickname: ')
sock.send(nickName.encode())


def sendThreadFunc():
    while True:
        try:
            myword = raw_input()
            sock.send(myword.encode())
            # print(sock.recv(1024).decode())
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