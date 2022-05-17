from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sys
import Window
from Class import *
import Global_var
from Memory import *
from MultiThread import *
from Core import *


# 添加新进程到后备队列
def pressaddbutton():                                                                                       # 反斜杠续行
    if ui.NewProgressName.text() != '' and ui.NewProgressMemory.text() != '' and ui.NewProgressTime.text() \
            != '':
        Global_var.WaitingQueue.append(PCB(ui.NewProgressName.text(), ui.NewProgressTime.text(),
                                           ui.NewProgressMemory.text(), ui.NewProgressPriority.currentText()))
    else:
        # 报错弹窗
        print('error')


if __name__ == '__main__':     # mainThread
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Window.Ui_MainWindow()  # 创建ui对象
    ui.setupUi(Mainwindow)

    # 绑定槽函数
    ui.AddButton.clicked.connect(pressaddbutton)

    Mainwindow.show()
    sys.exit(app.exec_())  # exe cycle/circulation

