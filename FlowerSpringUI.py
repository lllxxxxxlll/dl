#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ File        : FlowerSpring.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :界面集成7.2,需要从my_logmanger中导入具体内容
"""

import os
import sys
import json
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QScrollArea,QFrame, 
    QTextEdit, QComboBox, QToolBar, QMenu, QMessageBox,QFileDialog,QDialog,QListWidget,QListWidgetItem
)
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QCursor
from mylog_manager import LogManager
from testui import LogSearchUI



class LogWriter(QWidget):
    """日志写入界面"""
    def __init__(self, log_manager, plant_name, parent=None):
        super().__init__(parent)
        print(f"创建LogWriter，植物名称: {plant_name}")  # 调试打印
        print(f"父控件状态: {'有效' if parent else '无'}")  # 新增调试
        self.log_manager = log_manager
        self.plant_name = plant_name
        self.log_list_widget = QListWidget()#提前初始化控件
        print(f"log_list_widget对象ID(初始化): {id(self.log_list_widget)}")  # 新增对象ID检查
        self.selected_image = None
        # self.log_list_widget = None  # 新增日志列表控件
        
        # 创建UI组件
        self.setup_ui()
        print(f"初始化完成，log_list_widget状态: {'存在' if hasattr(self, 'log_list_widget') else '不存在'}")  # 新增调试
        print(f"log_list_widget对象ID(初始化后): {id(self.log_list_widget)}")  # 新增对象ID检查

    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel(f"记录「{self.plant_name}」的养护日志")
        title.setStyleSheet("color: #2e7d32;")
        main_layout.addWidget(title)
        
        # 内容编辑区
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("在这里详细记录您的养护过程...")
        self.editor.setFont(QFont("Arial", 12))
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #fffde7; 
                border: 1px solid #fff59d;
                border-radius: 5px;
                padding: 15px;
                min-height: 200px;
            }
        """)
        main_layout.addWidget(self.editor, 1)  # 设置拉伸因子
        
        # 信息工具栏
        self.setup_toolbar(main_layout)
        select_image_button = QPushButton("选择照片")
        select_image_button.clicked.connect(self.select_image)
        main_layout.addWidget(select_image_button)

        # 新增：日志列表显示
        # self.log_list_widget = QListWidget()
        print(f"log_list_widget创建完成: {self.log_list_widget}")  # 新增调试
        main_layout.addWidget(self.log_list_widget)
        print(f"log_list_widget已添加到布局")  # 新增调试

        print("初始化日志列表")
        self.log_list_widget.setVisible(True)
        self.log_list_widget.setEnabled(True)
        self.update_log_list()  # 初始化日志列表
        
        # 新增：创建底部水平布局
        bottom_layout = QHBoxLayout()

        # 新增：添加伸缩项，将按钮推向两侧
        bottom_layout.addStretch(1)

        # 删除按钮
        delete_button = QPushButton("删除日志")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        delete_button.clicked.connect(self.delete_log)
        # 新增：将删除按钮添加到底部布局，左对齐
        bottom_layout.addWidget(delete_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # 保存按钮
        save_button = QPushButton("保存日志")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        save_button.clicked.connect(self.save_log)
        # 新增：将保存按钮添加到底部布局，右对齐
        bottom_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)

        # 将底部布局添加到主布局
        main_layout.addLayout(bottom_layout)
        # 撤销删除按钮
        undo_delete_button = QPushButton("撤销删除")
        undo_delete_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        undo_delete_button.clicked.connect(self.undo_delete_log)
        bottom_layout.addWidget(undo_delete_button, alignment=Qt.AlignmentFlag.AlignLeft)

    def update_log_list(self):
        """更新日志列表显示"""
        print(f"开始更新日志列表，控件状态: {'存在' if self.log_list_widget is not None else '不存在'}")  # 修改判断条件
        print(f"update_log_list中的log_list_widget对象ID: {id(self.log_list_widget) if hasattr(self, 'log_list_widget') else '无'}")
        
        if self.log_list_widget is not None:  # 修改为显式的None检查
            print(f"控件实际状态: 可见={self.log_list_widget.isVisible()}, 启用={self.log_list_widget.isEnabled()}")
            self.log_list_widget.clear()
            print(f"正在获取植物 [{self.plant_name}] 的日志...")
            plant_logs = self.log_manager.get_logs_by_plants(self.plant_name)
            print(f"获取到的日志数量: {len(plant_logs)}")
            if not plant_logs:
                print("警告: 未找到该植物的任何日志")
            for i, log in enumerate(plant_logs):
                log_text = f"{log.date.strftime('%m-%d %H:%M')} {log.content}"
                print(f"添加日志 #{i+1}: {log_text}")
                self.log_list_widget.addItem(log_text)
        else:
            print("错误: log_list_widget为None")

    def delete_log(self):
        """删除日志"""
         #获取当前植物的日志
        plant_logs =  self.log_manager.get_logs_by_plants(self.plant_name)
        # 确认删除
        confirm = QMessageBox.question(self, "确认删除", "确定要删除当前选中的日志吗？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.No:
            return
        
        # 获取用户选中的日志索引
        selected_items = self.log_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择要删除的日志！")
            return
        
        selected_index = self.log_list_widget.row(selected_items[0])
        # # 获取当前植物的日志
        plant_logs =  self.log_manager.get_logs_by_plants(self.plant_name)

        if 0 <= selected_index < len(plant_logs):
            log_entry_to_delete = plant_logs[selected_index]
            if self.log_manager.delete_log(log_entry_to_delete):
                self.log_manager.save_to_file()
                self.update_log_list()  # 更新日志列表显示
                QMessageBox.information(self, "成功", "日志已删除！")
                self.editor.clear()
                self.selected_image = None  # 删除后清空选中的图片路径
            else:
                QMessageBox.warning(self, "警告", "删除日志失败！")
        else:
            QMessageBox.warning(self, "警告", "没有可删除的日志！")
    def setup_toolbar(self, main_layout):
        """设置信息工具栏"""
        toolbar = QHBoxLayout()
        
        # 天气选择
        weather_label = QLabel("天气:")
        self.weather_combo = QComboBox()
        self.weather_combo.addItems(["晴", "多云", "阴", "小雨", "大雨", "雪"])
        self.weather_combo.setCurrentIndex(0)
        
        # 生长阶段
        growth_label = QLabel("生长阶段:")
        self.growth_combo = QComboBox()
        self.growth_combo.addItems(["幼苗期", "生长期", "成熟期", "开花期", "休眠期"])
        self.growth_combo.setCurrentIndex(0)
        
        toolbar.addWidget(weather_label)
        toolbar.addWidget(self.weather_combo)
        toolbar.addWidget(growth_label)
        toolbar.addWidget(self.growth_combo)
        toolbar.addStretch()
        
        # 表情按钮
        emoji_button = QPushButton("😊")
        emoji_button.setFont(QFont("Arial", 16))
        emoji_button.setFixedSize(40, 40)
        emoji_button.setStyleSheet("border-radius: 20px;")
        emoji_button.clicked.connect(self.show_emoji_panel)
        
        toolbar.addWidget(emoji_button)
        main_layout.addLayout(toolbar)
    
    def show_emoji_panel(self):
        """显示表情面板"""
        # 简化的表情选择器（实际中可以扩展为带多个表情的面板）
        emojis = ["😊", "😢", "😡", "😎", "😍", "🤔", "🥰", "🤩", "🥳"]
        
        menu = QMenu(self)
        for emoji in emojis:
            action = QAction(emoji, self)
            action.triggered.connect(lambda _, e=emoji: self.insert_emoji(e))
            menu.addAction(action)
        
        menu.exec(QCursor.pos())
    
    def insert_emoji(self, emoji):
        """在当前位置插入表情符号"""
        self.editor.insertPlainText(emoji)
    def get_image_file_path(self):
        """选择照片并获取图片路径"""
        try:
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)")
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

            if file_dialog.exec():
                file_paths = file_dialog.selectedFiles()
                if file_paths:
                    file_path = file_paths[0]
                    if os.path.exists(file_path):
                        return file_path
                    else:
                        QMessageBox.warning(self, "警告", "选择的文件不存在，请重新选择。")
                else:
                    QMessageBox.warning(self, "警告", "未选择任何文件，请重新选择。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"选择图片时发生错误: {str(e)}")
        return None
    def select_image(self):
        '''选择照片'''
        file_path  = self.get_image_file_path()
        if file_path:
            self.selected_image = file_path
        # file_dialog = QFileDialog()
        # file_dialog.setNameFilter("图片文件(*.png *.jpg *.jpeg)")
        # if file_dialog.exec():
        #     file_path = file_dialog.selectedFiles()
        #     if file_path:
        #         self.selected_image = file_path[0]
    def save_log(self):
        """保存日志"""
        content = self.editor.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "警告", "日志内容不能为空！")
            return

        # 添加天气信息
        weather = self.weather_combo.currentText()
        growth = self.growth_combo.currentText()
        if not weather or not growth:
            QMessageBox.warning(self, "warning", "weather and groth!")
            return
        # 在日志内容前添加标签
        final_content = f"[{growth}][{weather}] {content}"
        # 创建日志条目
        self.log_manager.add_log(self.plant_name, final_content,weather,growth,self.selected_image)     #调用了log_manager,并给image参数传入了由select_image得到的文件路径
        # # 更新日志内容
        # if self.log_manager.logs.last_added:
        #     self.log_manager.logs.last_added.content = final_content
        
        # 保存到文件
        self.log_manager.save_to_file()
        
        QMessageBox.information(self, "成功", "日志已保存！")
        self.editor.clear()
        self.selected_image = None  # 保存后清空选中的图片路径
    
    def undo_delete_log(self):
        """撤销删除日志"""
        # 确认撤销删除
        confirm = QMessageBox.question(self, "确认撤销删除", "确定要撤销删除当前日志吗？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.No:
            return
        # 撤销删除当前日志
        if self.log_manager.undo_delete():
            self.log_manager.save_to_file()
            QMessageBox.information(self, "成功", "日志已撤销删除！")
        else:
            QMessageBox.warning(self, "警告", "没有可撤销删除的日志！")
    

#设置页面内容
class MainWindow(QMainWindow):
    """主窗口集成日志功能"""
    def __init__(self):
        super().__init__()
        self.log_manager = LogManager()
        self.log_manager.load_from_file()  # 从文件加载现有日志
        # self.search_ui = LogSearchUI() #直接初始化会导致日志搜索界面显示异常
        self.search_ui = None
        self.setWindowTitle("养花日志系统")
        self.setGeometry(100, 100, 800, 600)
        
        self.setup_ui()
    
    def setup_ui(self):
        # 中心部件
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # 植物选择视图
        self.plants_view = self.create_plants_view()
        self.stack.addWidget(self.plants_view)
        
        # 日志编写视图
        self.log_writer = None
        
        # 创建工具栏
        self.create_toolbar()
        #  '''创建顶部工具栏'''
    def create_toolbar(self):
        toolbar = self.addToolBar("操作")
        # 返回按钮
        back_action = QAction(QIcon.fromTheme("go-previous"), "返回", self)
        back_action.triggered.connect(self.show_plants_view)
        toolbar.addAction(back_action)
        
        # 日志查看按钮
        view_logs_action = QAction(QIcon.fromTheme("view-list-details"), "查看上一次日志", self)
        view_logs_action.triggered.connect(self.show_recentlog_view)
        toolbar.addAction(view_logs_action)

        # 日志记录按钮
        view_logs_action = QAction(QIcon.fromTheme("view-list-details"), "查看所有日志", self)
        view_logs_action.triggered.connect(self.show_logs_view)
        toolbar.addAction(view_logs_action)
        
        # 保存所有日志按钮
        save_action = QAction(QIcon.fromTheme("document-save"), "保存所有", self)
        save_action.triggered.connect(lambda: self.log_manager.save_to_file())
        toolbar.addAction(save_action)
        # 搜索日志按钮
        search_action = QAction(QIcon.fromTheme("system-search"), "搜索日志", self)
        search_action.triggered.connect(self.show_search_ui)
        toolbar.addAction(search_action)

        # 归档旧日志按钮
        archive_action = QAction(QIcon.fromTheme("archive"), "归档旧日志", self)
        archive_action.triggered.connect(self.archive_old_logs)
        toolbar.addAction(archive_action)
        # # 导出日志按钮
        # export_action = QAction(QIcon.fromTheme("document-export"), "导出日志", self)
        # export_action.triggered.connect(self.export_logs)
        # toolbar.addAction(export_action)
    def show_search_ui(self):
        """显示日志搜索界面"""
        if not self.search_ui:
            self.search_ui = LogSearchUI()
        self.search_ui.show()
    def archive_old_logs(self):
        """归档旧日志"""
        # 确认归档
        confirm = QMessageBox.question(self, "确认归档", "确定要归档旧日志吗？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.No:
            return
        # 调用 LogManager 类的方法归档旧日志
        self.log_manager.archive_old_logs()
        # 刷新显示
        self.refresh_logs_display()
        QMessageBox.information(self, "成功", "旧日志已归档！")
    # def export_logs(self):
    #     """导出日志"""
    #     # 确认导出
    #     confirm = QMessageBox.question(self, "确认导出", "确定要导出所有日志吗？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    #     if confirm == QMessageBox.StandardButton.No:
    #         return
    #     # 调用 LogManager 类的方法导出日志
    #     self.log_manager.export_logs()
    #     QMessageBox.information(self, "成功", "日志已导出！")
    # def refresh_logs_display(self):
    #     """刷新日志显示"""
    #     # 清空当前显示
    #     self.log_list.clear()
    #     # 重新加载日志
    #     self.log_manager.load_from_file()
    #     # 刷新显示
    #     self.display_logs()
    
    def create_plants_view(self):
        """创建植物选择视图"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("My Flower Spring")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 植物网格容器
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        plants_layout = QHBoxLayout(scroll_content)
        
        # 添加示例植物（实际应用中应从数据源加载）
        plant_names = ["玫瑰", "百合", "兰花", "多肉"]
        for name in plant_names:
            plant_card = QPushButton(name)
            plant_card.setFont(QFont("Arial", 14))
            plant_card.setFixedSize(150, 150)
            plant_card.setStyleSheet("""
                QPushButton {
                    background-color: #e8f5e9;
                    border: 2px solid #c8e6c9;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton:hover {
                    border: 2px solid #4CAF50;
                    background-color: #dcf0dd;
                }
            """)
            plant_card.clicked.connect(lambda checked, n=name: self.open_log_writer(n))
            plants_layout.addWidget(plant_card)
        
        # 添加植物按钮
        add_plant_btn = QPushButton("＋添加植物")
        add_plant_btn.setFixedSize(150, 150)
        add_plant_btn.setFont(QFont("Arial", 14))
        add_plant_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border: 2px dashed #c8e6c9;
                border-radius: 10px;
                padding: 20px;
                color: #757575;
            }
            QPushButton:hover {
                border: 2px dashed #4CAF50;
                background-color: #f0fff4;
            }
        """)
        plants_layout.addWidget(add_plant_btn)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        return widget
    
    def open_log_writer(self, plant_name):
        """打开日志编写界面"""
        self.log_writer = LogWriter(self.log_manager, plant_name, self)
        self.stack.addWidget(self.log_writer)
        self.stack.setCurrentWidget(self.log_writer)
    
    def show_recentlog_view(self):
        """显示日志查看界面"""
        # 简化实现，实际应创建完整日志浏览界面
        # last_logs = self.log_manager.get_recent_logs(10)
        last_log = self.log_manager.get_recent_logs()
        if last_log:
            recent_log = last_log[0]
            dialog = QDialog(self)
            dialog.setWindowTitle("日志记录")
            layout = QVBoxLayout(dialog)

            log_info = QLabel(f"{recent_log.date.strftime('%m-%d %H:%M')} {recent_log.plant_name}: {recent_log.content}")
            layout.addWidget(log_info)

            if recent_log.image:
                pixmap = QPixmap(recent_log.image)
                if not pixmap.isNull():
                     # 获取图片原始尺寸
                    original_width = pixmap.width()
                    original_height = pixmap.height()
                    # 限制最大缩放尺寸
                    max_width = 640
                    max_height = 640
                    # 计算缩放比例
                    scale_width = max_width / original_width
                    scale_height = max_height / original_height
                    scale_factor = min(scale_width, scale_height, 1.0)  # 确保不超过原始尺寸
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)
                    # 使用高质量抗锯齿缩放算法
                    pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    image_label = QLabel()
                    image_label.setPixmap(pixmap)
                    layout.addWidget(image_label)
                    # pixmap = pixmap.scaled(640, 640, Qt.AspectRatioMode.KeepAspectRatio)
                    # image_label = QLabel()
                    # image_label.setPixmap(pixmap)
                    # layout.addWidget(image_label)

            dialog.exec()
        else:
            QMessageBox.information(self, "日志记录", "还没有输入日志。")

        # msg = "你写入的日志:\n"
        # for log in last_logs:
        #     msg += f"\n{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content[:]}"
            # dialog.exec()
            # if log:
            #     dialog = QDialog(self)
            #     dialog.setWindowTitle("日志记录")
            #     layout = QVBoxLayout(dialog)

            #     log_info = QLabel(f"{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content}")
            #     layout.addWidget(log_info)
            # if log.image:
            #     dialog = QDialog(self)
            #     pixmap = QPixmap(log.image)
            #     if not pixmap.isNull():
            #         # 获取图片原始尺寸
            #         original_width = pixmap.width()
            #         original_height = pixmap.height()
            #         # 限制最大缩放尺寸
            #         max_width = 640
            #         max_height = 640
            #         # 计算缩放比例
            #         scale_width = max_width / original_width
            #         scale_height = max_height / original_height
            #         scale_factor = min(scale_width, scale_height, 1.0)  # 确保不超过原始尺寸
            #         new_width = int(original_width * scale_factor)
            #         new_height = int(original_height * scale_factor)
            #         # 使用高质量抗锯齿缩放算法
            #         pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            #         image_label = QLabel()
            #         image_label.setPixmap(pixmap)
            #         layout.addWidget(image_label)
                        # pixmap = pixmap.scaled(640, 640, Qt.AspectRatioMode.KeepAspectRatio)
                        # image_label = QLabel()
                        # image_label.setPixmap(pixmap)
                        # layout.addWidget(image_label)

            # dialog.exec()
        # QMessageBox.information(self, "日志记录", msg)
    # def show_logs_view(self):
    #     """显示日志列表视图"""
    #     last_logs = self.log_manager.get_recent_logs(10)
    #     msg = "你写入的日志:\n"
    #     for log in last_logs:
    #         if log.image:
    #             dialog  = QDialog(self)
    #             layout = QVBoxLayout(dialog)
    #             log_info = QLabel(f"{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content}")
    #             layout.addWidget(log_info)
    #             pixmap = QPixmap(log.image)
    #             if not pixmap.isNull():
    #                  # 获取图片原始尺寸
    #                 original_width = pixmap.width()
    #                 original_height = pixmap.height()
    #                 # 限制最大缩放尺寸
    #                 max_width = 640
    #                 max_height = 640
    #                 # 计算缩放比例
    #                 scale_width = max_width / original_width
    #                 scale_height = max_height / original_height
    #                 scale_factor = min(scale_width, scale_height, 1.0)  # 确保不超过原始尺寸
    #                 new_width = int(original_width * scale_factor)
    #                 new_height = int(original_height * scale_factor)
    #                 # 使用高质量抗锯齿缩放算法
    #                 pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    #                 image_label = QLabel()
    #                 image_label.setPixmap(pixmap)
    #                 layout.addWidget(image_label)
    #                 # pixmap = pixmap.scaled(640, 640, Qt.AspectRatioMode.KeepAspectRatio)
    #                 # image_label = QLabel()
    #                 # image_label.setPixmap(pixmap)
    #                 # layout.addWidget(image_label)
    #                 dialog.exec()
    #         msg += f"\n{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content[:]}"
    #     QMessageBox.information(self, "日志记录", msg)
    def show_logs_view(self):
    # """显示日志列表视图"""
        last_logs = self.log_manager.get_recent_logs()
    
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
    
        # 添加所有日志
        if not last_logs:
            layout.addWidget(QLabel("暂无日志记录"))
        else:
            for log in last_logs:
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
        
        # 添加确定按钮
        btn_ok = QPushButton("确定")
        btn_ok.clicked.connect(dialog.accept)
        main_layout.addWidget(btn_ok)
        
        dialog.exec()
    
    def show_plants_view(self):
        """显示植物列表视图"""
        self.stack.setCurrentWidget(self.plants_view)
        

class FlowerSpring(QApplication):
    """养花日志应用"""
    def __init__(self, argv):
        super().__init__(argv)
        self.window = MainWindow()
        self.window.resize(800,600)
        self.window.show()


if __name__ == "__main__":
    app = FlowerSpring(sys.argv)
    sys.exit(app.exec())
