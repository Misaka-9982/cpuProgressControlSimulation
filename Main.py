from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys

import Global_var
import Window
from MultiThread import *
from Core import *


# 添加新进程到后备队列
def pressaddbutton():                                                                                       # 反斜杠续行
    if ui.NewProcessName.text() != '' and ui.NewProcessMemory.text() != '' and ui.NewProcessTime.text() \
            != '':
        Global_var.WaitingQueue.append(PCB(ui.NewProcessName.text(), float(ui.NewProcessTime.text()),
                                           float(ui.NewProcessMemory.text()), ui.NewProcessPriority.currentText()))

        try:
            Global_var.WaitingQueue.sort(reverse=True, key=lambda pcb: pcb.priority)  # key传进函数的是列表中的每一个元素
        except ValueError:
            print('valueerror_w')
        ui.NewProcessName.setText('')
        ui.NewProcessMemory.setText('')
        ui.NewProcessTime.setText('')
        ui.NewProcessPriority.setCurrentIndex(0)
    else:
        # 报错弹窗
        print('error')


# 限制输入框输入数据类型
def edittextvaluecontrol():
    ui.NewProcessMemory.setValidator(Window.QtGui.QDoubleValidator())
    ui.NewProcessTime.setValidator(Window.QtGui.QDoubleValidator())


# 检测剩余内存总量
def memorydetect():
    beforememory = Global_var.SumSpace
    while True:
        sleep(2)
        sumusedmemory = 0
        y = 0
        for x in Global_var.FreePartition:
            y += x.size
        if y != beforememory:
            beforememory = y
            print('freememory', y)
        '''
        if sumusedmemory != beforememory:
            beforememory = sumusedmemory
            # 下行调用概率导致解释器崩溃
            ui.MemoryBar.setProperty('value', (sumusedmemory/Global_var.SumSpace)*100)
            # setvalue 是设置进度条步进步数的！！！！
            ui.MemoryBar.update()  # 不刷新控件会导致百分比数字重叠
            #print('updatesuccess')
        '''


def uiupdatequeuedetect():
    while True:
        # 刷新等待队列ui
        if UiUpdateFlag.waitingqueue:
            for i in range(ui.WaitingQueue.columnCount()):  # 修改前先置空表
                ui.WaitingQueue.removeRow(i)
            ui.WaitingQueue.setRowCount(len(Global_var.WaitingQueue))  # 先添加要更新的行数
            for n, i in enumerate(Global_var.WaitingQueue):
                ui.WaitingQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.WaitingQueue.setItem(n, 1, QTableWidgetItem(str(i.pid)))
                ui.WaitingQueue.setItem(n, 2, QTableWidgetItem(i.priority))
                ui.WaitingQueue.setItem(n, 3, QTableWidgetItem(str(i.runningtime)))
                ui.WaitingQueue.setItem(n, 4, QTableWidgetItem(str(i.memory)))
            ui.WaitingQueue.viewport().update()
            UiUpdateFlag.waitingqueue = False

        # 刷新就绪队列ui
        if UiUpdateFlag.readyqueue:
            for i in range(ui.ReadyQueue.columnCount()):  # 修改前先置空表
                ui.ReadyQueue.removeRow(i)
            ui.ReadyQueue.setRowCount(len(Global_var.ReadyQueue))  # 先添加要更新的行数
            for n, i in enumerate(Global_var.ReadyQueue):
                ui.ReadyQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.ReadyQueue.setItem(n, 1, QTableWidgetItem(str(i.pid)))
                ui.ReadyQueue.setItem(n, 2, QTableWidgetItem(i.priority))
                ui.ReadyQueue.setItem(n, 3, QTableWidgetItem(str(i.runningtime)))
                ui.ReadyQueue.setItem(n, 4, QTableWidgetItem(str(i.memory)))
            ui.ReadyQueue.viewport().update()
            UiUpdateFlag.readyqueue = False
        # 刷新运行中ui
        if UiUpdateFlag.runningprocess:
            for i in range(ui.RunningQueue.columnCount()):
                ui.RunningQueue.removeRow(i)
            ui.RunningQueue.setRowCount(len(Global_var.Runningprocess))
            for n, i in enumerate(Global_var.Runningprocess):
                ui.RunningQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.RunningQueue.setItem(n, 1, QTableWidgetItem(str(i.pid)))
                ui.RunningQueue.setItem(n, 2, QTableWidgetItem(i.priority))
                ui.RunningQueue.setItem(n, 3, QTableWidgetItem(str(i.runningtime)))
                ui.RunningQueue.setItem(n, 4, QTableWidgetItem(str(i.memory)))
            ui.RunningQueue.viewport().update()
            UiUpdateFlag.runningprocess = False
            # 刷新运行时间ui
        if UiUpdateFlag.runningprocesstime:
            for n, i in enumerate(Global_var.Runningprocess):
                ui.RunningQueue.setItem(n, 3, QTableWidgetItem(str(Global_var.Runningprocess[n].runningtime)))
            ui.RunningQueue.viewport().update()
            UiUpdateFlag.runningprocesstime = False



if __name__ == '__main__':     # mainThread
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Window.Ui_MainWindow()  # 创建ui对象
    ui.setupUi(Mainwindow)

    # 限制输入框数据类型
    edittextvaluecontrol()

    # 绑定槽函数
    ui.AddButton.clicked.connect(pressaddbutton)

    # 创建线程
    t_detectwaitingprocessqueue.start()
    t_detectreadyprocessqueue.start()
    t_cputiming.start()
    t_memorydetect = threading.Thread(target=memorydetect, args=(), daemon=True)
    t_memorydetect.start()
    t_uiupdatequeuedetect = threading.Thread(target=uiupdatequeuedetect, args=(), daemon=True)
    t_uiupdatequeuedetect.start()

    Mainwindow.show()
    sys.exit(app.exec_())  # exe cycle/circulation
