import Class

ReadyQueue = []     # 就绪队列
HangingQueue = []   # 挂起队列
WaitingQueue = []   # 后备队列


def addprogress(progressname, runningtime, priority, status):
    WaitingQueue.append(Class.PCB(progressname, runningtime, priority, status))


