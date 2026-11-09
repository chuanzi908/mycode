#定义一个函数,完成学生成绩的排名,将最高和最低成绩进行输出.
def student_ranking(scores):
    # 计算最高和最低成绩
    max_score = max(scores)
    min_score = min(scores)

    # 对成绩进行排序（降序）
    sorted_scores = sorted(scores, reverse=True)

    print(f"学生成绩排名（降序）: {sorted_scores}")
    print(f"最高成绩: {max_score}")
    print(f"最低成绩: {min_score}")

# 测试函数
if __name__ == "__main__":
    # 示例成绩数据
    student_scores = [85, 92, 78, 100, 88, 73, 90]
    student_ranking(student_scores)





