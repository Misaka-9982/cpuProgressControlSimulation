import Class
import Global_var
from Class import *


def ismemoryenough(process):
    freememory = 0
    # memorymerge()  # 检测前就执行一次内存合并，简化后续分配步骤，提高效率  # 合并可能本身比较费时间？# 如果要把这步拿出去，需要修改内存分配逻辑
    # 合并移动到分配函数中，该函数只负责检查，提高效率
    for i in Global_var.FreePartition:
        freememory += i.size
        if freememory >= process.memory:
            '''
            # 临时调试用代码 输出完整剩余内存大小
            y = 0
            for x in Global_var.FreePartition:
                y += x.size
            print('freememory2', y)
            '''
            return True
    if freememory < process.memory:
        #print(freememory)
        return False


def memoryallocation(process):   # 分配前要先用调用检查，这里只分配不检查是否足够
    memorymerge()
    for n, i in enumerate(Global_var.FreePartition):
        # condition_1防越界
        if process.memory <= i.size:
            Global_var.UsedPartition.append(Class.MemoryPartition(start=i.start, size=process.memory,
                                                                  usingprocess=process.processname))

            Global_var.FreePartition[n].start += process.memory
            Global_var.FreePartition[n].size -= process.memory
            break
        elif process.memory > i.size:
            return False  # 检测内存是否足够时已经合并可用分区


def memoryrelease(process):
    totalrelease = 0
    for n, i in enumerate(Global_var.UsedPartition):
        if i.usingprocess == process.processname:
            Global_var.UsedPartition[n].usingprocess = None
            Global_var.FreePartition.append(Global_var.UsedPartition[n])
            Global_var.UsedPartition.pop(n)
            totalrelease += i.size
    print('totalrelease:', totalrelease)


# 合并内存碎片
def memorymerge():
    try:
        Global_var.FreePartition.sort(key=lambda x: x.start)  # 按照起址排序
    except ValueError:
        print('valueerror_m')
    if len(Global_var.FreePartition) != 1:  # 不是一整块就执行合并
        for n, i in enumerate(Global_var.FreePartition):
            # condition_1为了防止越界
            if n != len(Global_var.FreePartition)-1 and i.start + i.size == Global_var.FreePartition[n+1].start:
                Global_var.FreePartition[n].size += Global_var.FreePartition[n+1].size
                Global_var.FreePartition.pop(n+1)

