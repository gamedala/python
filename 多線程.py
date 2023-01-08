
import threading,queue,os
import time
#导入方法模块

def main(inargs):
    work_queue = queue.Queue()     #queue类中实现了锁
    for i in range(3):#设置了3个子进程
        worker = Worker(work_queue,i)     #工作线程、工作队列、线程编号
        worker.daemon = True                  #守护进程
        worker.start()                        #启动线程开始
    for elemt in inargs:
        work_queue.put(elemt)              #加入到队列中开始各个线程
    work_queue.join()                       #队列同步


class Worker(threading.Thread):
    #继承线程类，类也是不太好学习的部分

    def __init__(self, work_queue,number):
        super(Worker,self).__init__()
        self.work_queue = work_queue
        self.number = number

    def process(self,elemt):
        #自定义的线程处理函数，用于run()中.
        #这里仅仅打印线程号和传入参数
        time.sleep(5)
        print("\n{0}  task:----{1}".format(self.number,elemt))

    def run(self):
        #重载threading类中的run()
        while True:
            try:
                elemt = self.work_queue.get() #从队列取出任务
                self.process(elemt)
            finally:
                self.work_queue.task_done() #通知queue前一个task已经完成

if __name__=="__main__":
    main(os.listdir("."))
    #这一步是用当前目录下得文件名作测
    
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.delay, 5)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")