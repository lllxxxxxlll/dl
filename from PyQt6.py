from PyQt6.QtWidgets import QApplication, QMainWindow, QAction
from PyQt6.QtGui import QIcon
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图标主题示例")

        # 从系统图标主题获取图标
        view_logs_action = QAction(QIcon.fromTheme("view-list-details"), "查看日志", self)
        self.addAction(view_logs_action)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
