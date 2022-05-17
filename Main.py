from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys
import Window
from Class import *
import Global_var
from Memory import *
from MultiThread import *
from Core import *


# 添加新进程到后备队列
def pressaddbutton():
    if ui.NewProgressName is not None and ui.NewProgressMemory is not None and ui.NewProgressTime is not None:
        Global_var.WaitingQueue.append(PCB(ui.NewProgressName, ui.NewProgressTime, ui.NewProgressMemory,
                                           ui.NewProgressPriority))
    else:
        # 报错弹窗
        pass


if __name__ == '__main__':     # mainThread
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Window.Ui_MainWindow()  # 创建ui对象
    ui.setupUi(Mainwindow)

    # 绑定槽函数
    ui.AddButton.clicked.connect(pressaddbutton)

    Mainwindow.show()
    sys.exit(app.exec_())  # exe cycle/circulation

