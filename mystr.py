class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def __str__(self):
        return f"Student(name: {self.name}, age: {self.age}, grade: {self.grade})"

# 创建一个学生对象
student = Student("Alice", 20, "A+")

# 打印学生对象
print(student.grade)