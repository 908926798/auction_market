from multiprocessing import Process
import os


def run_proc(name,count):
    count.append(0)
    print count
    print 'Run child process %s (%s)...' % (name, os.getpid())

if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    count=[]
    p = Process(target=run_proc, args=('test',count,))
    q = Process(target=run_proc, args=('test', count,))
    print 'Process will start.'
    p.start()
    p.join()
    q.start()
    q.join()
    print 'Process end.'