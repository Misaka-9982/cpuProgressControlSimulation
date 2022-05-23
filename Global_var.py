import Memory
import Main

ReadyQueue = []     # 就绪队列
HangingQueue = []   # 挂起队列
WaitingQueue = []   # 后备队列
Runningprocess = []  # 正在运行的进程
UsedPartition = []
FreeMemory = 1024
OperationSystem = Memory.PCB('operationsystem', 'infinite', 175, 5, 'running')
FreePartition = [Memory.MemoryPartition()]
SumSpace = 1024


# MinimumPartition = 5  # MB
