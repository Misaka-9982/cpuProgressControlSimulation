import Global_var
from time import *
from Memory import *


# 该模块为与ui无关的逻辑函数


def detectwaitingprocessqueue():  # 检测后备队列有无可调入就绪队列的进程
    while True:
        for i in Global_var.WaitingQueue:
            # print(ismemoryenough(process=i))
            if ismemoryenough(process=i) is True:
                Global_var.ReadyQueue.append(i)
                Global_var.isReadyQueueEmpty = False
                Global_var.ReadyQueue[len(Global_var.ReadyQueue)-1].status = 'Ready'
                memoryallocation(process=i)  # 分配内存
                Global_var.WaitingQueue.remove(i)  # remove是移除指定元素，pop是指定下标的元素
                try:
                    Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)  # key传进函数的是列表中的每一个元素
                    UiUpdateFlag.waitingqueue = True
                except ValueError:
                    print('valueerror_w')
                # 入就绪队列后，对就绪队列优先级排序
                try:
                    Global_var.ReadyQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
                    UiUpdateFlag.readyqueue = True
                except ValueError:
                    print('valueerror_r')
    #print(Global_var.ReadyQueue)


def cputiming():  # cpu计时，要在检测就绪队列之后启动
    while True:
        if len(Global_var.Runningprocess) != 0:
            sleep(1)
            for n, i in enumerate(Global_var.Runningprocess):
                if i.runningtime <= 0:
                    memoryrelease(Global_var.Runningprocess[n])
                    Global_var.Runningprocess.pop(n)
                else:
                    Global_var.Runningprocess[n].runningtime -= 1
                    # print('-1s')
            UiUpdateFlag.runningprocesstime = True


def detectreadyprocessqueue():  # 检测就绪队列有无需要抢占当前运行进程
    while True:
        # 反复排序会导致ui闪烁，将对ReadyQueue的排序移动到每次对其抢占操作后
        if len(Global_var.ReadyQueue):
            try:
                if len(Global_var.Runningprocess) < 3:
                    Global_var.Runningprocess.append(Global_var.ReadyQueue[0])
                    Global_var.Runningprocess[len(Global_var.Runningprocess)-1].status = 'Running'
                    Global_var.ReadyQueue.pop(0)
                    UiUpdateFlag.runningprocess = True
                    UiUpdateFlag.readyqueue = True
                elif len(Global_var.Runningprocess) != 0 and len(Global_var.ReadyQueue) != 0:
                    if max(Global_var.ReadyQueue, key=lambda x: x.priority).priority >\
                            min(Global_var.Runningprocess, key=lambda x: x.priority).priority:  # 有正在运行的进程
                        min(Global_var.Runningprocess, key=lambda x: x.priority).status = 'Ready'
                        Global_var.ReadyQueue.append(min(Global_var.Runningprocess, key=lambda x: x.priority))
                        Global_var.Runningprocess.remove(min(Global_var.Runningprocess, key=lambda x: x.priority))
                        Global_var.ReadyQueue[0].status = 'Running'
                        Global_var.Runningprocess.append(Global_var.ReadyQueue[0])
                        Global_var.ReadyQueue.pop(0)
                        UiUpdateFlag.runningprocess = True
                        UiUpdateFlag.readyqueue = True
                        try:
                            # 抢占操作会打乱ReadyQueue，抢占后排一次序
                            Global_var.ReadyQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
                        except ValueError:
                            print('valueerror_r')
            except AttributeError:
                print('Runningprocess has been removed')


def hangingprocess(n):
    Global_var.Runningprocess[n].status = 'Hanging'
    Global_var.HangingQueue.append(Global_var.Runningprocess[n])
    memoryrelease(Global_var.Runningprocess[n])
    Global_var.Runningprocess.pop(n)
    UiUpdateFlag.runningprocess = True
    UiUpdateFlag.hangingqueue = True


def unhangingprocess(process):
    process.status = 'Waiting'
    Global_var.WaitingQueue.append(process)
    try:
        # 打乱Queue，排一次序
        Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
    except ValueError:
        print('valueerror_w')
    Global_var.HangingQueue.remove(process)
    UiUpdateFlag.hangingqueue = True
    UiUpdateFlag.waitingqueue = True