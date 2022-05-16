import Global_var
from time import *
from Memory import *
# 该模块为与ui无关的逻辑函数


def detectwaitingprogressqueue():  # 检测后备队列有无可调入就绪队列的进程
    while True:
        if len(Global_var.WaitingQueue) != 0:
            Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)  # key传进函数的是列表中的每一个元素
            for i in Global_var.WaitingQueue:
                if ismemoryenough(i) is True:
                    Global_var.ReadyQueue.append(i)
                    Global_var.WaitingQueue.remove(i)  # remove是移除指定元素，pop是指定下标的元素


def cputiming():  # cpu计时，要在检测就绪队列之后启动
    while Global_var.RunningProgress and Global_var.RunningProgress.runningtime > 0:
        sleep(0.2)
        Global_var.RunningProgress.runningtime -= 0.2
    if Global_var.RunningProgress and Global_var.RunningProgress.runningtime <= 0:
        Global_var.RunningProgress = None


def detectreadyprogressqueue():  # 检测就绪队列有无需要抢占当前运行进程
    while len(Global_var.ReadyQueue):
        Global_var.ReadyQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
        if Global_var.RunningProgress is None:  # 当前无正在运行进程
            Global_var.RunningProgress = Global_var.ReadyQueue[0]
        elif Global_var.ReadyQueue[0].priority > Global_var.RunningProgress.priority:  # 有正在运行的进程
            Global_var.ReadyQueue.append(Global_var.RunningProgress)
            Global_var.RunningProgress = Global_var.ReadyQueue[0]


