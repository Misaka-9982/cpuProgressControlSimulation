import random
import Global_var


def ispidlegal(pid):
    if Global_var.Runningprocess is not None:
        if pid == Global_var.Runningprocess.pid:
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


class PCB:
    def __init__(self, processname, runningtime, memory, priority, status='Waiting'):
        self.processname = processname
        self.runningtime = runningtime
        self.memory = memory                       # self为对象成员，不加self为类成员，对应java中不加和加static
        self.priority = priority
        self.status = status
        self.pid = random.randint(0, 65536)
        while not ispidlegal(self.pid):
            self.pid = random.randint(0, 65536)


class MemoryPartition:
    def __init__(self, start=0, size=1024, usingprocesspid=None):  # size单位为MB
        self.start = start
        self.size = size
        self.usingprocesspid = usingprocesspid  # 记录占用当前分区的进程名字，不是完整PCB

'''
class LinkList:
    def __init__(self, data, nextnode):
        self.data = data
        self.nextnode = nextnode
'''