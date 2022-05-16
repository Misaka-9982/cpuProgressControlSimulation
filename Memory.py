import Global_var
from Class import *


def ismemoryenough(needmemory):
    freememory = 0
    for i in Global_var.FreePartition:
        if freememory < needmemory:
            freememory += i.size
        else:
            return True
    if freememory < needmemory:
        return False


def memoryallocation(needmemory):
    freepartition = []
    freememory =  0
    for i in Global_var.FreePartition:
        if freememory < needmemory:
            freememory += i.size
        else:
            pass

# 释放时要能释放占用的对应分区


