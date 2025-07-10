import sys
from PyQt6.QtWidgets import (  QLineEdit, QPushButton,
QListWidget, QMessageBox,QDialog,QWidget,QApplication, QMainWindow, 
QWidget, QVBoxLayout, QHBoxLayout, 
QLabel, QStackedWidget, QScrollArea,QFrame, 
QTextEdit, QComboBox, QToolBar, QMenu,QFileDialog)
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QCursor
from mylog_manager import LogManager

class LogSearchUI(QWidget):
    def __init__(self):
        super().__init__()
        self.log_manager = LogManager()
        self.log_manager.load_from_file()  # 从文件加载日志
        self.initUI()

    def initUI(self):
        # 布局
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        # 搜索输入框
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("输入植物名称进行搜索")

         # 返回按钮布局
        back_layout = QHBoxLayout()
        back_button = QPushButton("返回", self)
        back_button.clicked.connect(self.close)  # 连接关闭窗口的槽函数
        back_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(back_layout)

        # 搜索按钮
        self.search_button = QPushButton("搜索", self)
        self.search_button.clicked.connect(self.search_logs)

        # 归档按钮
        self.archive_button = QPushButton("归档旧日志", self)
        self.archive_button.clicked.connect(self.archive_old_logs)

        # 结果列表
        self.result_list = QListWidget(self)

        # 添加组件到布局
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.archive_button)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.result_list)

        self.setLayout(main_layout)
        self.setWindowTitle("养花日志搜索与归档")
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def search_logs(self):
        plant_name = self.search_input.text().strip()
        if not plant_name:
            QMessageBox.warning(self, "警告", "请输入正确植物名称")
            return

        # 调用 LogManager 类的方法获取特定植物的日志
        logs = self.log_manager.get_logs_by_plants(plant_name)
        self.result_list.clear()
        if not logs:
            QMessageBox.information(self, "提示", "未找到相关日志")
        else:
            # 创建主窗口和布局
            dialog = QDialog(self)
            dialog.setWindowTitle("日志记录")
            dialog.resize(800, 600)
        
            # 创建可滚动区域
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
        
            # 创建内容部件
            content_widget = QWidget()
            layout = QVBoxLayout(content_widget)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # 顶部对齐
        
            for log in logs:
                # 创建日志条目容器
                log_frame = QFrame()
                log_frame.setFrameShape(QFrame.Shape.Box)
                log_layout = QVBoxLayout(log_frame)
                
                # 添加日志基本信息
                log_info = QLabel(f"{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content}")
                log_layout.addWidget(log_info)
                
                # 添加图片（如果有）
                if log.image:
                    pixmap = QPixmap(log.image)
                    if not pixmap.isNull():
                        # 缩放图片（保持宽高比）
                        scaled = pixmap.scaled(
                            640, 
                            480, 
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        image_label = QLabel()
                        image_label.setPixmap(scaled)
                        log_layout.addWidget(image_label)
                
                # 添加间距分隔符
                log_layout.addSpacing(20)
                layout.addWidget(log_frame)
        
        # 设置滚动区域内容
        scroll_area.setWidget(content_widget)
        
        # 设置对话框主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.addWidget(scroll_area) 
        dialog.exec()
                # log_info = f"[{log.date}] {log.content}"
                # self.result_list.addItem(log_info)

    def archive_old_logs(self):
        try:
            self.log_manager.archive_old_logs()
            self.log_manager.save_to_file()
            QMessageBox.information(self, "成功", "旧日志归档成功")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"归档旧日志时出错: {str(e)}")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = LogSearchUI()
#     sys.exit(app.exec())
