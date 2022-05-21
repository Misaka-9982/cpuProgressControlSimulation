import Global_var
from time import *
from Memory import *


# 该模块为与ui无关的逻辑函数


def detectwaitingprocessqueue():  # 检测后备队列有无可调入就绪队列的进程
    while True:
            for i in Global_var.WaitingQueue:
                #print(ismemoryenough(process=i))
                if ismemoryenough(process=i) is True:
                    Global_var.ReadyQueue.append(i)
                    Global_var.isReadyQueueEmpty = False
                    Global_var.ReadyQueue[len(Global_var.ReadyQueue)-1].status = 'Ready'
                    memoryallocation(process=i)  # 分配内存
                    Global_var.WaitingQueue.remove(i)  # remove是移除指定元素，pop是指定下标的元素
                    try:
                        Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)  # key传进函数的是列表中的每一个元素
                    except ValueError:
                        print('valueerror_w')
                    # 入就绪队列后，对就绪队列优先级排序
                    try:
                        Global_var.ReadyQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
                    except ValueError:
                        print('valueerror_r')
        #print(Global_var.ReadyQueue)


def cputiming():  # cpu计时，要在检测就绪队列之后启动
    while True:
        if Global_var.Runningprocess is not None:
            while Global_var.Runningprocess.runningtime > 0:
                sleep(1)
                Global_var.Runningprocess.runningtime -= 1
                # print('-1s')

            memoryrelease(Global_var.Runningprocess)
            Global_var.Runningprocess = None


def detectreadyprocessqueue():  # 检测就绪队列有无需要抢占当前运行进程
    while True:
        # 反复排序会导致ui闪烁，将对ReadyQueue的排序移动到每次对其操作后
        if len(Global_var.ReadyQueue):
            try:
                if Global_var.Runningprocess is None:  # 当前无正在运行进程
                    Global_var.Runningprocess = Global_var.ReadyQueue[0]
                    Global_var.Runningprocess.status = 'Running'
                    Global_var.ReadyQueue.pop(0)
                elif Global_var.ReadyQueue[0].priority > Global_var.Runningprocess.priority:  # 有正在运行的进程
                    Global_var.Runningprocess.status = 'Ready'
                    Global_var.ReadyQueue.append(Global_var.Runningprocess)
                    Global_var.Runningprocess = Global_var.ReadyQueue[0]
                    Global_var.Runningprocess.status = 'Running'
                    Global_var.ReadyQueue.pop(0)
                    try:
                        Global_var.ReadyQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
                    except ValueError:
                        print('valueerror_r')
            except AttributeError:
                print('Runningprocess has been removed')


def hangingprocess():
    Global_var.Runningprocess.status = 'Hanging'
    Global_var.HangingQueue.append(Global_var.Runningprocess)
    memoryrelease(Global_var.Runningprocess)
    Global_var.Runningprocess = None


def unhangingprocess(process):
    process.status = 'Ready'
    Global_var.ReadyQueue.append(process)
    Global_var.HangingQueue.remove(process)
