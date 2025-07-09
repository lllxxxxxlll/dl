"""
@ File        : log_manager.py
@ Author      : 示例
@ Version     : V1.0.0
@ Description : 日志管理类，用于管理养花日志的添加、加载和保存操作
"""
import json
import os
from datetime import datetime


class LogEntry:
    """日志条目类，用于表示单条日志信息"""
    __slots__ = ('plant_name', 'content', 'weather', 'growth', 'date', 'image','next')
    def __init__(self, plant_name, content, weather, growth,image,date=None):
        self.plant_name = plant_name
        self.content = content
        self.weather = weather
        self.growth = growth
        self.date = date if date else datetime.now()
        self.image = image
        self.next = None # 指向下一个日志条目的指针

    def to_dict(self):
        return {
            'plant_name': self.plant_name,
            'content': self.content,
            'weather': self.weather,
            'growth': self.growth,
            'date': self.date.isoformat(),
            'image': self.image
        }#转换成字典方便存储

    @classmethod
    def from_dict(cls, data):
        """从字典创建日志条目"""
        return cls(
            data['plant_name'],
            data['content'],
            data['weather'],
            data['growth'],
            data['image'],
            datetime.fromisoformat(data['date'])
        )

class LogNode:
    """日志节点类，用于链表结构"""
    def __init__(self,log_entry):
        self.log_entry = log_entry
        self.next = None

class LogLinkedList:
    """日志链表类，用于管理日志节点"""
    def __init__(self):
        self.head = None
        self.size = 0
        self.last_added = None#跟踪最近日志
    def add_log(self,log_entry):
        """添加日志节点到头部"""
        log_node = LogNode(log_entry)
        log_node.next = self.head
        self.head = log_node
        self.size+=1#指针指向下一个链表,链表长度增加
    
    def add_log_tail(self,log_entry):
        """添加日志节点到链表尾部"""
        log_node = LogNode(log_entry)
        if not self.head:
            self.head = log_node
        else:
            current = self.head
            while current.next:#使用临时变量完成对链表的遍历,遍历到最后一个节点接入新的节点
                current = current.next
            current.next = log_node
        self.size+=1#指针指向下一个链表,链表长度增加
    
    def get_all_logs(self):
        """获取所有日志节点"""
        logs = []
        current = self.head
        while current:
            logs.append(current.log_entry)
            current = current.next
        return logs

    def remove_log(self,log_entry):
        if not self.head:
            return False
        #如果删除的是头节点
        if self.head.log_entry ==log_entry:
            self.head = self.head.next
            self.size -=1
            if self.size == 0:
                self.last_added = None
            return True
        #如果删除的是中间节点或者尾节点
        else:
            current = self.head
            while current.next:
                current = current.next
                if current.next.log_entry == log_entry:
                    #如果删除的是最后一个节点,更新last_added
                    if current.next == self.last_added:
                        self.last_added = current if current.next.next is None else current.next.next
                    current.next = current.next.next
                    self.size -=1
                    return True
                current = current.next
            return False
         
        def get_logs_by_plants(self,plant):
            '''获取特定植物的日志'''
            logs = []
            current = self.head
            while current:
                if current.log_entry.plant_name == plant:
                    logs.append(current.log_entry)
                current = current.next
            return logs
        
        def get_logs_by_date(self,date):
            '''获取特定日期的日志'''
            logs = []
            current = self.head
            while current:
                if current.log_entry.date == date:
                    logs.append(current.log_entry)
                current = current.next
            return logs
        
        def get_recent_logs(self,num=10):
            logs = []
            current = self.head
            for i in range(count):
                logs.append(current.log_entry)
                current = current.next
            return logs
        
        def to_list(self):
            '''转换为列表,便于存储'''
            return [log.to_dict() for log in self.logs]

        def __str__(self):
            '''可视化列表'''
            result = []
            current = self.head
            while current:
                log = current.log_entry
                result.append(f"[{log.date}] {log.plant_name} - {log.content}")
                current = current.next
            return "\n".join(result)
        
        def print_list(self):
            current = self.head
            while current:
                print(current.log_entry,end = "->")
                current = current.next
            print("None")

class LogManager:
    """日志管理系统（使用链表、栈、队列）"""
    def __init__(self):
        self.logs = LogLinkedList()  # 链表存储所有日志
        self.undo_stack = []        # 栈用于日志删除撤销
        self.archive_queue = []      # 队列用于日志归档
    
    def add_log(self, plant_name, content):
        """添加新日志"""
        new_log = LogEntry(plant_name, content)
        self.logs.add_log(new_log)
        return new_log
    
    def delete_log(self, log_entry):
        """删除日志"""
        if self.logs.remove_log(log_entry):
            # 将删除操作压入撤销栈
            self.undo_stack.append(log_entry)
            return True
        return False
    
    def undo_delete(self):
        """撤销最后一次删除"""
        if not self.undo_stack:
            return False
        
        # 从栈中弹出最后删除的日志
        deleted_log = self.undo_stack.pop()
        # 添加回日志链表
        self.logs.add_log_tail(deleted_log)
        return True
    
    def archive_old_logs(self, max_logs_per_plant=100):
        """归档旧日志（队列处理）"""
        current = self.logs.head
        plant_counts = {}
        
        while current:
            plant = current.plant_name
            plant_counts[plant] = plant_counts.get(plant, 0) + 1
            
            # 如果某个植物的日志过多，归档最早的
            if plant_counts[plant] > max_logs_per_plant:
                # 找到最旧的日志（链表尾部）
                to_archive = self._find_oldest_log(plant)
                if to_archive:
                    # 从链表中移除
                    self.logs.remove_log(to_archive)
                    # 加入归档队列
                    self.archive_queue.append(to_archive)
            
            current = current.next
    
    def _find_oldest_log(self, plant_name):
        """查找特定植物最旧的日志（链表尾部）"""
        oldest = None
        current = self.logs.head
        while current:
            if current.plant_name == plant_name:
                # 没有找到更旧的日志，直接更新
                if oldest is None or current.date < oldest.date:
                    oldest = current
            current = current.next
        return oldest
    
    def save_to_file(self, filename="logs.json"):
        """保存日志到文件"""
        data = {
            "logs": self.logs.to_list(),
            "undo_stack": [log.to_dict() for log in self.undo_stack],
            "archive_queue": [log.to_dict() for log in self.archive_queue]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filename="logs.json"):
        """从文件加载日志"""
        if not os.path.exists(filename):
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # print(data.shape)
        
        # 重新构建日志链表
        self.logs = LogLinkedList()
        for log_dict in data.get("logs", []):
            log = LogEntry.from_dict(log_dict)
            self.logs.add_log_tail(log)  # 按原始顺序添加
        
        # 重新构建撤销栈
        self.undo_stack = [
            LogEntry.from_dict(log_dict)
            for log_dict in data.get("undo_stack", [])
        ]
        
        # 重新构建归档队列
        self.archive_queue = [
            LogEntry.from_dict(log_dict)
            for log_dict in data.get("archive_queue", [])
        ]


# class LogManager:
#     """日志管理类，负责日志的添加、加载和保存"""
#     def __init__(self, log_file="logs.json"):
#         self.log_file = log_file
#         self.logs = []
#         self.last_added = None
#         self.load_from_file()

#     def add_log(self, plant_name, content, weather=None, growth=None,image=None):
#         """添加新的日志条目"""
#         # image = image_path
#         log_entry = LogEntry(plant_name, content, weather, growth,image)
#         self.logs.append(log_entry)
#         self.last_added = log_entry
#         return log_entry

#     def get_recent_logs(self, num=10):
#         """获取最近的指定数量的日志"""
#         return self.logs[-num:]

#     def load_from_file(self):
#         """从文件加载日志"""
#         if os.path.exists(self.log_file):
#             try:
#                 with open(self.log_file, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                     for entry in data:
#                         log_entry = LogEntry(
#                             entry['plant_name'],
#                             entry['content'],
#                             entry['weather'],
#                             entry['growth'],
#                             entry.get('image',None),
#                             datetime.fromisoformat(entry['date'])
#                         )
#                         self.logs.append(log_entry)
#             except Exception as e:
#                 print(f"加载日志文件时出错: {e}")

#     def save_to_file(self):
#         """保存日志到文件"""
#         data = []
#         for entry in self.logs:
#             data.append({
#                 'plant_name': entry.plant_name,
#                 'content': entry.content,
#                 'weather': entry.weather,
#                 'growth': entry.growth,
#                 'date': entry.date.isoformat(),
#                 'image': entry.image
#             })
#         try:
#             with open(self.log_file, 'w', encoding='utf-8') as f:
#                 json.dump(data, f, ensure_ascii=False, indent=4)
#         except Exception as e:
#             print(f"保存日志文件时出错: {e}")