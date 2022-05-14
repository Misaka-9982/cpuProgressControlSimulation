class PCB:
    def __init__(self, progressname, runningtime, memory, priority, status='Waiting'):
        self.progressname = progressname
        self.runningtime = runningtime
        self.memory = memory
        self.priority = priority
        self.status = status
        # 是否加入独立进程/同步进程
