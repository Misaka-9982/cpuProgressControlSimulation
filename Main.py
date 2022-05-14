from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import threading

import Window

if __name__ == '__main__':     # mainThread
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Window.Ui_MainWindow()  # 创建ui对象
    ui.setupUi(Mainwindow)

    Mainwindow.show()
    sys.exit(app.exec_())  # exe cycle/circulation
