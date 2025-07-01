import logging
import os
from logging.handlers import RotatingFileHandler
from PyQt6.QtCore import QObject, pyqtSignal

class QtLogHandler(QObject, logging.Handler):
    """ 将日志发送到Qt界面的处理器 """
    log_signal = pyqtSignal(str, str)  # 信号: (日志级别, 消息)

    def __init__(self):
        super().__init__()
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.log_signal.emit(record.levelname, msg)

class LogSystem:
    def __init__(self, log_dir="logs"):
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)
        
        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "application.log")
        
        # 文件处理器 - 自动轮转
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
        # Qt界面处理器
        self.qt_handler = QtLogHandler()
        self.logger.addHandler(self.qt_handler)
    
    def log(self, level, message, **kwargs):
        extra_data = kwargs.pop('extra', {})
        
        if level == 'DEBUG':
            self.logger.debug(message, extra={'extra': extra_data})
        elif level == 'INFO':
            self.logger.info(message, extra={'extra': extra_data})
        elif level == 'WARNING':
            self.logger.warning(message, extra={'extra': extra_data})
        elif level == 'ERROR':
            self.logger.error(message, extra={'extra': extra_data})
        elif level == 'CRITICAL':
            self.logger.critical(message, extra={'extra': extra_data})
    
    def query_logs(self, level=None, keyword=None, max_lines=100):
        """ 查询日志内容 """
        results = []
        log_file = "logs/application.log"
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-max_lines:]  # 获取最后N行
                
                for line in reversed(lines):  # 从最新开始显示
                    if level and f" - {level} - " not in line:
                        continue
                    if keyword and keyword.lower() not in line.lower():
                        continue
                    results.append(line.strip())
        except FileNotFoundError:
            pass
            
        return results