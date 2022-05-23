from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtGui import QColor
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
        UiUpdateFlag.waitingqueue = True
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
        sleep(1)
        sumusedmemory = 0
        y = 0
        for x in Global_var.FreePartition:
            y += x.size
        if y != beforememory:
            beforememory = y
            Global_var.FreeMemory = y
            print('freememory', y)
            UiUpdateFlag.memorybar = True


def getdeleterunningprocess():
    try:
        pid = ui.RunningQueue.selectedItems()[1].text()
        deleterunningprocess(int(pid))
    except IndexError:
        print('None was selected')


def getdeletereadyprocess():
    try:
        pid = ui.ReadyQueue.selectedItems()[1].text()
        deletereadyprocess(int(pid))  # 这里记得要转换类型str->int！！！！
    except IndexError:
        print('None was selected')


def getdeletewaitprocess():
    try:
        pid = ui.WaitingQueue.selectedItems()[1].text()
        deletewaitprocess(int(pid))
    except IndexError:
        print('None was selected')


def gethangingprocess():
    try:
        pid = ui.RunningQueue.selectedItems()[1].text()
        hangingprocess(int(pid))
    except IndexError:
        print('None was selected')


def getunhangingprocess():
    try:
        pid = ui.HangingQueue.selectedItems()[1].text()
        unhangingprocess(int(pid))
    except IndexError:
        print('None was selected')


def getreset():
    reset()


def initialmemorybar():
    # 操作系统占用
    for z in range(50):
        ui.MemoryBar.setItem(0, z, QTableWidgetItem())
        ui.MemoryBar.setColumnWidth(z, 12)  # 编辑器里的默认行宽小于24会失效
    memoryallocation(Global_var.OperationSystem)
    for z in range(8):  # 操作系统内存占用的格子，16% 7格 range(8) 0-7
        ui.MemoryBar.setItem(0, z, QTableWidgetItem())
        ui.MemoryBar.item(0, z).setBackground(QColor(241, 162, 26))



def uiupdatequeuedetect():
    while True:
        # 刷新等待队列ui
        if UiUpdateFlag.waitingqueue:
            sleep(0.5)  # 防止等待队列执行过快导致未能从ui移除
            for i in range(ui.WaitingQueue.rowCount()):  # 修改前先置空表
                ui.WaitingQueue.removeRow(i)
            ui.WaitingQueue.setRowCount(len(Global_var.WaitingQueue))  # 先添加要更新的行数
            for n, i in enumerate(Global_var.WaitingQueue):
                ui.WaitingQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.WaitingQueue.setItem(n, 1, QTableWidgetItem(str(i.pid)))
                ui.WaitingQueue.setItem(n, 2, QTableWidgetItem(i.priority))
                ui.WaitingQueue.setItem(n, 3, QTableWidgetItem(str(i.runningtime)))
                ui.WaitingQueue.setItem(n, 4, QTableWidgetItem(str(i.memory)))
            ui.WaitingQueue.viewport().update()  # 刷新两次防止出现因为多线程调度导致刷新不完全的情况
            ui.WaitingQueue.viewport().update()
            UiUpdateFlag.waitingqueue = False

        # 刷新就绪队列ui
        if UiUpdateFlag.readyqueue:
            for i in range(ui.ReadyQueue.rowCount()):  # 修改前先置空表
                ui.ReadyQueue.removeRow(i)
            ui.ReadyQueue.setRowCount(len(Global_var.ReadyQueue))  # 先添加要更新的行数
            for n, i in enumerate(Global_var.ReadyQueue):
                ui.ReadyQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.ReadyQueue.setItem(n, 1, QTableWidgetItem(str(i.pid)))
                ui.ReadyQueue.setItem(n, 2, QTableWidgetItem(i.priority))
                ui.ReadyQueue.setItem(n, 3, QTableWidgetItem(str(i.runningtime)))
                ui.ReadyQueue.setItem(n, 4, QTableWidgetItem(str(i.memory)))
            ui.ReadyQueue.viewport().update()
            ui.ReadyQueue.viewport().update()
            UiUpdateFlag.readyqueue = False

        # 刷新运行中ui
        if UiUpdateFlag.runningprocess:
            for i in range(ui.RunningQueue.rowCount()):
                ui.RunningQueue.removeRow(i)
            ui.RunningQueue.setRowCount(len(Global_var.Runningprocess))
            for n, i in enumerate(Global_var.Runningprocess):
                ui.RunningQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.RunningQueue.setItem(n, 1, QTableWidgetItem(str(i.pid)))
                ui.RunningQueue.setItem(n, 2, QTableWidgetItem(i.priority))
                ui.RunningQueue.setItem(n, 3, QTableWidgetItem(str(i.runningtime)))
                ui.RunningQueue.setItem(n, 4, QTableWidgetItem(str(i.memory)))
            ui.RunningQueue.viewport().update()
            ui.RunningQueue.viewport().update()
            UiUpdateFlag.runningprocess = False

            # 刷新运行时间ui
        if UiUpdateFlag.runningprocesstime:
            for n, i in enumerate(Global_var.Runningprocess):
                ui.RunningQueue.setItem(n, 3, QTableWidgetItem(str(Global_var.Runningprocess[n].runningtime)))
            ui.RunningQueue.viewport().update()
            ui.RunningQueue.viewport().update()
            UiUpdateFlag.runningprocesstime = False

        # 刷新挂起队列UI
        if UiUpdateFlag.hangingqueue:
            for i in range(ui.HangingQueue.rowCount()):
                ui.HangingQueue.removeRow(i)
            ui.HangingQueue.setRowCount(len(Global_var.HangingQueue))
            for n, i in enumerate(Global_var.HangingQueue):
                ui.HangingQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.HangingQueue.setItem(n, 1, QTableWidgetItem(str(i.pid)))
                ui.HangingQueue.setItem(n, 2, QTableWidgetItem(i.priority))
                ui.HangingQueue.setItem(n, 3, QTableWidgetItem(str(i.runningtime)))
                ui.HangingQueue.setItem(n, 4, QTableWidgetItem(str(i.memory)))
            ui.HangingQueue.viewport().update()
            ui.HangingQueue.viewport().update()
            UiUpdateFlag.hangingqueue = False

        # 内存占用条更新
        if UiUpdateFlag.memorybar:
            # 一格对应2%
            for i in range(8, 50):  # 去掉操作系统占用的格子
                ui.MemoryBar.item(0, i).setBackground(QColor(255, 255, 255))
            for i in range(8, int(((Global_var.SumSpace-Global_var.FreeMemory)/Global_var.SumSpace)*50)):
                ui.MemoryBar.item(0, i).setBackground(QColor(132, 170, 10))
            ui.MemoryBar.viewport().update()
            UiUpdateFlag.memorybar = False


if __name__ == '__main__':     # mainThread
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Window.Ui_MainWindow()  # 创建ui对象
    ui.setupUi(Mainwindow)

    # 初始化进度条
    initialmemorybar()

    # 限制输入框数据类型
    edittextvaluecontrol()

    # 绑定槽函数
    ui.AddButton.clicked.connect(pressaddbutton)  # 添加
    ui.DeleteReadyProgressButton.clicked.connect(getdeletereadyprocess)  # 删除就绪
    ui.DeleteWaitingProgressButton.clicked.connect(getdeletewaitprocess)  # 删除后备
    ui.DeleteRunningProcess.clicked.connect(getdeleterunningprocess)  # 删除运行中
    ui.HangButton.clicked.connect(gethangingprocess)  # 挂起
    ui.UnhangButton.clicked.connect(getunhangingprocess)  # 解挂
    ui.ResetButton.clicked.connect(getreset)  # 重置

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
