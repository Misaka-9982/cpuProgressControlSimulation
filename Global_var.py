import Memory

ReadyQueue = []     # 就绪队列
HangingQueue = []   # 挂起队列
WaitingQueue = []   # 后备队列
RunningProgress = None  # 正在运行的进程
UsedPartition = []
FreePartition = [Memory.MemoryPartition()]
SumSpace = 1024
MinimumPartition = 5  # MB
