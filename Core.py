import Global_var
from time import *
from Memory import *
# 该模块为与ui无关的逻辑函数


def detectwaitingprocessqueue():  # 检测后备队列有无可调入就绪队列的进程
    while True:
        if len(Global_var.WaitingQueue) != 0:
            Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)  # key传进函数的是列表中的每一个元素
            for i in Global_var.WaitingQueue:
                if ismemoryenough(process=i) is True:
                    Global_var.ReadyQueue.append(i)
                    memoryallocation(process=i)  # 分配内存
                    Global_var.WaitingQueue.remove(i)  # remove是移除指定元素，pop是指定下标的元素


def cputiming():  # cpu计时，要在检测就绪队列之后启动
    while Global_var.Runningprocess and Global_var.Runningprocess.runningtime > 0:
        sleep(0.2)
        Global_var.Runningprocess.runningtime -= 0.2
    if Global_var.Runningprocess and Global_var.Runningprocess.runningtime <= 0:
        memoryrelease(Global_var.Runningprocess)
        Global_var.Runningprocess = None


def detectreadyprocessqueue():  # 检测就绪队列有无需要抢占当前运行进程
    while len(Global_var.ReadyQueue):
        Global_var.ReadyQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
        if Global_var.Runningprocess is None:  # 当前无正在运行进程
            Global_var.Runningprocess = Global_var.ReadyQueue[0]
        elif Global_var.ReadyQueue[0].priority > Global_var.Runningprocess.priority:  # 有正在运行的进程
            Global_var.ReadyQueue.append(Global_var.Runningprocess)
            Global_var.Runningprocess = Global_var.ReadyQueue[0]
            Global_var.ReadyQueue.remove(0)


def hanginggrogress():
    pass


def unhangingprocess():
    pass


