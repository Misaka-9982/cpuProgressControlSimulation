import random
import Global_var


class PCB:
    def __init__(self, processname, runningtime, memory, priority, status='Waiting'):
        self.processname = processname
        self.runningtime = runningtime
        self.memory = memory                       # self为对象成员，不加self为类成员，对应java中不加和加static
        self.priority = priority
        self.status = status
        self.waittime = 0
        self.pid = random.randint(0, 65536)
        while not self.ispidlegal(self.pid):
            self.pid = random.randint(0, 65536)

    @staticmethod
    def ispidlegal(pid):
        for i in Global_var.Runningprocess:
            if pid == i.pid:
                return False
        for i in Global_var.WaitingQueue:
            if pid == i.pid:
                return False
        for i in Global_var.ReadyQueue:
            if pid == i.pid:
                return False
        for i in Global_var.HangingQueue:
            if pid == i.pid:
                return False
        return True


class MemoryPartition:
    def __init__(self, start=0, size=1024, usingprocesspid=None):  # size单位为MB
        self.start = start
        self.size = size
        self.usingprocesspid = usingprocesspid  # 记录占用当前分区的进程名字，不是完整PCB


class UiUpdateFlag:
    waitingqueue = False
    readyqueue = False
    runningprocess = False
    runningprocesstime = False
    hangingqueue = False
    memorybar = False
    usedpartition = False
'''
class LinkList:
    def __init__(self, data, nextnode):
        self.data = data
        self.nextnode = nextnode
'''