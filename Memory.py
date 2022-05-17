import Class
import Global_var
from Class import *


def ismemoryenough(progress):
    freememory = 0
    memorymerge()  # 检测前就执行一次内存合并，简化后续分配步骤，提高效率  # 合并可能本身比较费时间？# 如果要把这步拿出去，需要修改内存分配逻辑
    for i in Global_var.FreePartition:
        if freememory < progress.memory:
            freememory += i.size
        else:
            return True
    if freememory < progress.memory:
        return False


def memoryallocation(progress):   # 分配前要先用调用检查，这里只分配不检查是否足够
    for n, i in enumerate(Global_var.FreePartition):
        if progress.memory <= i.size:
            Global_var.UsedPartition.append(Class.MemoryPartition(start=i.start, size=progress.memory,
                                                                  usingprogress=progress.name))
            Global_var.FreePartition[n].start += progress.memory
            Global_var.FreePartition[n].size -= progress.memory
            break
        elif progress.memory > i.size:
            return False  # 检测内存是否足够时已经合并可用分区


def memoryrelease(progress):
    for n, i in enumerate(Global_var.UsedPartition):
        if i.usingprogress == progress.name:
            Global_var.UsedPartition[n].usingprogress = None
            Global_var.FreePartition.append(i)
            Global_var.UsedPartition.pop(n)


# 合并内存碎片
def memorymerge():
    Global_var.FreePartition.sort(key=lambda x: x.start)  # 按照起址排序
    for n, i in enumerate(Global_var.FreePartition):
        if i.start + i.size == Global_var.FreePartition[n+1].start:
            Global_var.FreePartition[n].size += Global_var.FreePartition[n+1].size
            Global_var.FreePartition.pop(n+1)
