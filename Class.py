class PCB:
    def __init__(self, progressname, runningtime, priority, status='Waiting'):
        self.progressname = progressname
        self.runningtime = runningtime
        self.priority = priority
        self.status = status
        # 是否加入独立进程/同步进程
