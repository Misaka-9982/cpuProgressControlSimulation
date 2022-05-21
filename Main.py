from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys
import Window
from MultiThread import *
from Core import *


# 添加新进程到后备队列
def pressaddbutton():                                                                                       # 反斜杠续行
    if ui.NewProcessName.text() != '' and ui.NewProcessMemory.text() != '' and ui.NewProcessTime.text() \
            != '':
        Global_var.WaitingQueue.append(PCB(ui.NewProcessName.text(), float(ui.NewProcessTime.text()),
                                           float(ui.NewProcessMemory.text()), ui.NewProcessPriority.currentText()))

        ui.NewProcessName.setText('')
        ui.NewProcessMemory.setText('')
        ui.NewProcessTime.setText('')
        ui.NewProcessPriority.setCurrentIndex(0)
        print(Global_var.WaitingQueue[0])
    else:
        # 报错弹窗
        print('error')


# 限制输入框输入数据类型
def edittextvaluecontrol():
    ui.NewProcessMemory.setValidator(Window.QtGui.QDoubleValidator())
    ui.NewProcessTime.setValidator(Window.QtGui.QDoubleValidator())


# 检测剩余内存总量
def memorydetect():
    beforememory = 0
    while True:
        sumusedmemory = 0
        for i in Global_var.UsedPartition:
            sumusedmemory += i.size
        if sumusedmemory != beforememory:
            beforememory = sumusedmemory
            # 下行调用概率导致解释器崩溃
            ui.MemoryBar.setProperty('value', (sumusedmemory/Global_var.SumSpace)*100)
            # setvalue 是设置进度条步进步数的！！！！
            ui.MemoryBar.update()  # 不刷新控件会导致百分比数字重叠
            #print('updatesuccess')


def uiupdatequeuedetect():
    temp_W = None
    temp_Wlen = None
    temp_R = None
    temp_Rlen = None
    temp_running = None
    temp_runningtime = None
    if Global_var.Runningprocess is not None:
        temp_runningtime = Global_var.Runningprocess.runningtime
    while True:
        # 刷新等待队列ui
        if len(Global_var.WaitingQueue) != temp_Wlen or Global_var.WaitingQueue != temp_W:
            if temp_W is not None:
                for i in range(temp_Wlen):  # 修改前先置空表
                    ui.WaitingQueue.removeRow(i)
            temp_W = Global_var.WaitingQueue
            temp_Wlen = len(Global_var.WaitingQueue)
            ui.WaitingQueue.setRowCount(temp_Wlen)  # 先添加要更新的行数
            for n, i in enumerate(Global_var.WaitingQueue):
                print('Waiting', i.processname)
                ui.WaitingQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.WaitingQueue.setItem(n, 1, QTableWidgetItem(i.priority))
                ui.WaitingQueue.setItem(n, 2, QTableWidgetItem(str(i.runningtime)))
                ui.WaitingQueue.setItem(n, 3, QTableWidgetItem(str(i.memory)))
            ui.WaitingQueue.viewport().update()
        # 刷新就绪队列ui
        if len(Global_var.ReadyQueue) != temp_Rlen or Global_var.ReadyQueue != temp_R:
            if temp_R is not None:
                for i in range(temp_Rlen):  # 修改前先置空表
                    ui.ReadyQueue.removeRow(i)
            print('temp_R:',temp_R)
            print('len_temp_R',temp_Rlen)
            temp_R = Global_var.ReadyQueue
            temp_Rlen = len(Global_var.ReadyQueue)
            ui.ReadyQueue.setRowCount(temp_Rlen)  # 先添加要更新的行数
            for n, i in enumerate(Global_var.ReadyQueue):
                ui.ReadyQueue.setItem(n, 0, QTableWidgetItem(i.processname))
                ui.ReadyQueue.setItem(n, 1, QTableWidgetItem(i.priority))
                ui.ReadyQueue.setItem(n, 2, QTableWidgetItem(str(i.runningtime)))
                ui.ReadyQueue.setItem(n, 3, QTableWidgetItem(str(i.memory)))
            ui.ReadyQueue.viewport().update()
        # 刷新运行中ui
        if Global_var.Runningprocess != temp_running:
            ui.RunningQueue.removeRow(0)
            temp_running = Global_var.Runningprocess
            if temp_running is not None:
                ui.RunningQueue.setRowCount(1)
                ui.RunningQueue.setItem(0, 0, QTableWidgetItem(Global_var.Runningprocess.processname))
                ui.RunningQueue.setItem(0, 1, QTableWidgetItem(str(Global_var.Runningprocess.runningtime)))
                ui.RunningQueue.setItem(0, 2, QTableWidgetItem(str(Global_var.Runningprocess.memory)))
            ui.RunningQueue.viewport().update()
            # 刷新运行时间ui
        try:  # 使用try except防止运行到if中间时runningprocess被释放报错
            if Global_var.Runningprocess is not None and \
                    Global_var.Runningprocess.runningtime != temp_runningtime:
                temp_runningtime = Global_var.Runningprocess.runningtime
                ui.RunningQueue.setItem(0, 1, QTableWidgetItem(str(temp_runningtime)))
                ui.RunningQueue.viewport().update()
        except AttributeError:
            print('Runningprocess has been removed')


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
    #t_memorydetect = threading.Thread(target=memorydetect, args=(), daemon=True)
    #t_memorydetect.start()
    t_uiupdatequeuedetect = threading.Thread(target=uiupdatequeuedetect, args=(), daemon=True)
    t_uiupdatequeuedetect.start()

    Mainwindow.show()
    sys.exit(app.exec_())  # exe cycle/circulation
