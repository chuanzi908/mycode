#利用完成对班级人员信息的采集,通过利用集合,可以对人员信息的删除
#需要记录,人员姓名,性别,年龄,班级,成绩
#打印此班级历史信息,及删除后当前信息
# 定义学生信息集合
students = set()
history = []
deleted = []

# 添加学生信息
def add_student(name, gender, age, class_name, score):
    student = (name, gender, age, class_name, score)
    students.add(student)
    history.append(f"添加：{name}, {gender}, {age}岁，{class_name}, {score}分")

# 删除学生信息
def remove_student(name):
    for s in list(students):
        if s[0] == name:
            students.remove(s)
            deleted.append(s)
            history.append(f"删除：{name}")
            return

# 采集数据
add_student("张三", "男", 18, "三年一班", 95)
add_student("李四", "女", 17, "三年一班", 88)
add_student("王五", "男", 18, "三年一班", 92)
add_student("赵六", "女", 17, "三年一班", 85)

# 打印历史信息
print("="*50)
print("📋 班级历史信息:")
print("="*50)
for h in history:
    print(h)

# 删除部分学生
remove_student("王五")
remove_student("赵六")

# 打印当前信息
print("\n" + "="*50)
print("👥 当前班级信息 (删除后):")
print("="*50)
print(f"总人数：{len(students)}")
for s in students:
    print(f"姓名:{s[0]}, 性别:{s[1]}, 年龄:{s[2]}, 班级:{s[3]}, 成绩:{s[4]}")

# 打印已删除信息
print("\n" + "="*50)
print("🗑️ 已删除学生:")
print("="*50)
for d in deleted:
    print(f"姓名:{d[0]}, 性别:{d[1]}, 年龄:{d[2]}, 班级:{d[3]}, 成绩:{d[4]}")


