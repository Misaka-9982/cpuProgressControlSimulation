import Global_var
from time import *
# 该模块为与ui无关的逻辑函数


def detectwaitingprogressqueue():
    while True:
        if len(Global_var.WaitingQueue) != 0:
            Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)  # key传进函数的是列表中的每一个元素
            for i in Global_var.WaitingQueue:
                if ismemoryenough(i) is True:
                    Global_var.ReadyQueue.append(i)
                    Global_var.WaitingQueue.remove(i)  # remove是移除指定元素，pop是指定下标的元素


def cputiming():  # cpu计时，要在检测就绪队列之后启动
    while Global_var.runningprogress and Global_var.runningprogress.runningtime > 0:
        sleep(0.5)
        Global_var.runningprogress.runningtime -= 0.5
    if Global_var.runningprogress and Global_var.runningprogress.runningtime <= 0:
        Global_var.runningprogress = None


def detectreadyprogressqueue():  # 检测就绪队列有无需要抢占当前运行进程
    while len(Global_var.ReadyQueue):
        Global_var.ReadyQueue.sort(reverse=True, key=lambda pcb: pcb.priority)
        if Global_var.runningprogress is None:  # 当前无正在运行进程
            Global_var.runningprogress = Global_var.ReadyQueue[0]
        elif Global_var.ReadyQueue[0].priority > Global_var.runningprogress.priority:  # 有正在运行的进程
            Global_var.ReadyQueue.append(Global_var.runningprogress)
            Global_var.runningprogress = Global_var.ReadyQueue[0]




def ismemoryenough(n):
    pass
