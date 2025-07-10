import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QInputDialog, QMessageBox

from PyQt6.QtCore import QDateTime, QTimer

class MainWindow(QMainWindow):

def __init__(self):

    super().__init__()

# 设置窗口大小

    self.setGeometry(100, 100, 300, 200)

    # 显示当前时间

    self.lbl_time = QLabel(self)

    self.lbl_time.setGeometry(50, 50, 200, 50)

    self.timer = QTimer(self)

    self.timer.timeout.connect(self.showTime)

    self.timer.start(1000)

    # 设置闹钟时间

    self.btn_alarm = QPushButton('设置闹钟', self)

    self.btn_alarm.setGeometry(50, 120, 100, 50)

    self.btn_alarm.clicked.connect(self.setAlarm)

    # 显示当前时间

    def showTime(self):

        now = QDateTime.currentDateTime()

        self.lbl_time.setText(now.toString('yyyy-MM-dd hh:mm:ss'))

        # 设置闹钟时间

    def setAlarm(self):

        time, ok = QInputDialog.getText(self, '设置闹钟', '请输入闹钟时间(格式：hh:mm:ss)')

        if ok:

            self.alarm_time = time

            QMessageBox.information(self, '提示', '闹钟已设置')

            # 启动闹钟线程

            self.alarm_thread = AlarmThread(self.alarm_time)

            self.alarm_thread.start()


class AlarmDialog(QDialog):

    def __init__(self, time):

        super().__init__()

        # 设置窗口大小

        self.setGeometry(100, 100, 300, 200)

        # 设置闹钟时间

        self.lbl_time = QLabel(self)

        self.lbl_time.setGeometry(50, 50, 200, 50)

        self.lbl_time.setText('闹钟时间：' + time)

        # 关闭闹钟按钮

        self.btn_close = QPushButton('关闭闹钟', self)

        self.btn_close.setGeometry(50, 120, 100, 50)

        self.btn_close.clicked.connect(self.closeAlarm)

        # 关闭闹钟

    def closeAlarm(self):

        self.close()