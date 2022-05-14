import Global_var
# 该模块为与ui无关的逻辑函数


def detectwaitingprogressqueue():
    while True:
        if len(Global_var.WaitingQueue) != 0:
            Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)  # key传进函数的是列表中的每一个元素
            for i in Global_var.WaitingQueue:
                if ismemoryenough(i) is True:
                    Global_var.ReadyQueue.append(i)
                    Global_var.WaitingQueue.remove(i)  # remove是移除指定元素，pop是指定下标的元素

# cpu调度算法位置
def cpuselect():
    while True:
        if len(Global_var.ReadyQueue) != 0:
            Global_var.ReadyQueue.sort(reverse=True,key=lambda pcb:pcb.priority)
            for i in Global_var.ReadyQueue:pass




def ismemoryenough(n):
    pass
