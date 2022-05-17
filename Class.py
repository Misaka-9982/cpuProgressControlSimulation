class PCB:
    def __init__(self, progressname, runningtime, memory, priority, status='Waiting'):
        self.progressname = progressname
        self.runningtime = runningtime
        self.memory = memory                       # self为对象成员，不加self为类成员，对应java中不加和加static
        self.priority = priority
        self.status = status
        # 是否加入独立进程/同步进程


class MemoryPartition:
    def __init__(self, start=0, size=1024, usingprogress=None):  # size单位为MB
        self.start = start
        self.size = size
        self.usingprogress = usingprogress  # 记录占用当前分区的进程名字，不是完整PCB

'''
class LinkList:
    def __init__(self, data, nextnode):
        self.data = data
        self.nextnode = nextnode
'''