#将本人的学科成绩进行登记,完成数据录入,其中包括:姓名,课程名称,成绩,放入列表当中
if __name__ == '__main__':

    # 创建空列表用于存储学生成绩信息
    students_scores = []

    # 输入学生数量
    num_students = int(input("请输入学生人数: "))

    print(f"\n请录入{num_students}位同学的成绩信息：")
    print("-" * 50)

    for i in range(num_students):
        print(f"\n第{i + 1}位同学:")
        name = input("  姓名: ")
        course = input("  课程名称: ")
        score = float(input("  成绩: "))

        # 将信息放入字典，再添加到列表中
        student_info = {
            '姓名': name,
            '课程名称': course,
            '成绩': score
        }
        students_scores.append(student_info)

    # 显示录入的所有信息
    print("\n" + "=" * 50)
    print("所有同学的成绩信息:")
    print("=" * 50)

    for idx, student in enumerate(students_scores, 1):
        print(f"\n{idx}. 姓名：{student['姓名']}")
        print(f"   课程名称：{student['课程名称']}")
        print(f"   成绩：{student['成绩']}")

    # 或者以表格形式显示
    print("\n" + "=" * 50)
    print("表格形式展示:")
    print("=" * 50)
    print(f"{'序号':<6} {'姓名':<10} {'课程名称':<15} {'成绩':<8}")
    print("-" * 50)

    for idx, student in enumerate(students_scores, 1):
        print(f"{idx:<6} {student['姓名']:<10} {student['课程名称']:<15} {student['成绩']:<8}")

    # 显示列表数据结构
    print("\n" + "=" * 50)
    print("列表数据结构:")
    print("=" * 50)
    print(students_scores)

