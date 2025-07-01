
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ File        : test_QPlainTextEdit_Log.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""

#使用QPlainTextEdit创建一个基本的测试窗口
import sys
import logging
from typing import Callable

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QTextBrowser,QTextEdit
from PyQt6.QtCore import pyqtSignal, QObject

class LogSignal(QObject):
    log_signal = pyqtSignal(str)#连接日志信号

class QtHandler(logging.Handler):
    #日志处理器
    def __init__(self,signal):
        super().__init__()
        self.signal = signal
    
    def emit(self,record):
        log_entry = self.format(record)
        self.signal.log_signal.emit(log_entry)
#初始化日志系统    
def init_log(update_log: Callable):
    log_signal = LogSignal()
    log_signal.log_signal.connect(update_log)  # 日志信号连接用于更新显示的槽函数

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # 创建文件处理器，将日志写入文件（不需要可删除）
    file_handler = logging.FileHandler('application.log', encoding="utf-8")  # 文件处理器
    file_handler.setLevel(logging.ERROR)  # 设置文件日志的级别
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # 创建自定义处理器，就日志输出到 Qt 页面显示
    qt_handler = QtHandler(log_signal)  # 使用自定义的日志处理器
    qt_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(qt_handler)

    # 控制台输出（不需要可删除，删除后控制台将不在输出日志信息，仅显示 print 打印）
    stream_handler = logging.StreamHandler()  # 输出到控制台
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s "))
    logger.addHandler(stream_handler)

    return logger

#使用Qwidget创建窗口
class LogWindow(QWidget):
    """显示日志的窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("日志输出")
        self.resize(800, 600)
        # self.log = QPlainTextEdit(self)
        self.log = QTextEdit(self)
        self.log.setReadOnly(True)  # 设置为只读模式
        layout = QVBoxLayout()
        layout.addWidget(self.log)
        self.setLayout(layout)
        self.logger = init_log(self.update_log)  # 初始化日志
        self.logger.info("这是一个消息")
    def update_log(self, log_text):
        # self.log.appendPlainText(log_text)  # 更新 QPlainTextEdit 内容
        self.log.append(log_text)  # 更新 QTextEdit 内容
        # 将光标移动到文本的最后一行
        cursor = self.log.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)  # 移动光标到最后
        self.log.setTextCursor(cursor)
        # 导出日志到文件
        with open("exported_logs.txt", "a", encoding="utf-8") as f:
            f.write(log_text + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogWindow()
    window.show()
    sys.exit(app.exec())
