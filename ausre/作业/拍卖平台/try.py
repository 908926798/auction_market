from multiprocessing import Process
import os

def run_proc(name,i):
    for j in range(0,5):
        print str(i)
        print "\n"
    print 'Run child process %s (%s)...' % (name, os.getpid())

if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Process(target=run_proc, args=('test',0))
    q = Process(target=run_proc, args=('test',1))
    print 'Process will start.'
    p.start()
    q.start()
    print 'Process end.'