from multiprocessing import Process
import os

count = []

def run_proc(name):
    print count
    print "\n"
    count.append((0,1))
    print count
    print 'Run child process %s (%s)...' % (name, os.getpid())

if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Process(target=run_proc, args=('test',))
    q = Process(target=run_proc, args=('test',))
    print 'Process will start.'
    p.start()
    p.join()
    q.start()
    q.join()
    print count
    print 'Process end.'