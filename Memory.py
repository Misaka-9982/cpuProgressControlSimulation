import Class
import Global_var
from Class import *


def ismemoryenough(process):
    freememory = 0
    memorymerge()  # 检测前就执行一次内存合并，简化后续分配步骤，提高效率  # 合并可能本身比较费时间？# 如果要把这步拿出去，需要修改内存分配逻辑
    for i in Global_var.FreePartition:
        if freememory < process.memory:
            freememory += i.size
        else:
            return True
    if freememory < process.memory:
        return False


def memoryallocation(process):   # 分配前要先用调用检查，这里只分配不检查是否足够
    for n, i in enumerate(Global_var.FreePartition):
        if process.memory <= i.size:
            Global_var.UsedPartition.append(Class.MemoryPartition(start=i.start, size=process.memory,
                                                                  usingprocess=process.name))
            Global_var.FreePartition[n].start += process.memory
            Global_var.FreePartition[n].size -= process.memory
            break
        elif process.memory > i.size:
            return False  # 检测内存是否足够时已经合并可用分区


def memoryrelease(process):
    for n, i in enumerate(Global_var.UsedPartition):
        if i.usingprocess == process.name:
            Global_var.UsedPartition[n].usingprocess = None
            Global_var.FreePartition.append(i)
            Global_var.UsedPartition.pop(n)


# 合并内存碎片
def memorymerge():
    Global_var.FreePartition.sort(key=lambda x: x.start)  # 按照起址排序
    for n, i in enumerate(Global_var.FreePartition):
        if i.start + i.size == Global_var.FreePartition[n+1].start:
            Global_var.FreePartition[n].size += Global_var.FreePartition[n+1].size
            Global_var.FreePartition.pop(n+1)

# 检测剩余内存总量
def memorydetect():
    sumfreememory = 0
    for i in Global_var.FreePartition:
        sumfreememory += i.size
    return sumfreememory
