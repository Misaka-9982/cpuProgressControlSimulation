from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys
import Window
from MultiThread import *
from Core import *


# 添加新进程到后备队列
def pressaddbutton():                                                                                       # 反斜杠续行
    if ui.NewProcessName.text() != '' and ui.NewProcessMemory.text() != '' and ui.NewProcessTime.text() \
            != '':
        Global_var.WaitingQueue.append(PCB(ui.NewProcessName.text(), int(ui.NewProcessTime.text()),
                                           int(ui.NewProcessMemory.text()), ui.NewProcessPriority.currentText()))
        '''
        ui.NewProcessName.setText('')
        ui.NewProcessMemory.setText('')
        ui.NewProcessTime.setText('')
        ui.NewProcessPriority.setCurrentIndex(0)
        '''
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
            ui.MemoryBar.setProperty('value', (sumusedmemory/Global_var.SumSpace)*100)
            # setvalue 是设置进度条步进步数的！！！！
            ui.MemoryBar.update()  # 不刷新控件会导致百分比数字重叠
            #print('updatesuccess')


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

    Mainwindow.show()
    sys.exit(app.exec_())  # exe cycle/circulation
