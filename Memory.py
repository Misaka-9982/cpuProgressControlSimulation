import Class
import Global_var
from Class import *


def ismemoryenough(needmemory):
    freememory = 0
    memorymerge()  # 检测前就执行一次内存合并，简化后续分配步骤，提高效率
    for i in Global_var.FreePartition:
        if freememory < needmemory:
            freememory += i.size
        else:
            return True
    if freememory < needmemory:
        return False


def memoryallocation(progressname, needmemory):   # 分配前要先用调用检查，这里只分配不检查是否足够
    for n, i in enumerate(Global_var.FreePartition):
        if needmemory <= i.size:
            Global_var.UsedPartition.append(Class.MemoryPartition(start=i.start, size=needmemory,
                                                                  usingprogress=progressname))
            Global_var.FreePartition[n].start += needmemory
            Global_var.FreePartition[n].size -= needmemory
            break
        elif needmemory > i.size:
            return False  # 检测内存是否足够时已经合并可用分区






# 释放时要能释放占用的对应分区,释放和合并是两步
def memorymerge():
    pass

