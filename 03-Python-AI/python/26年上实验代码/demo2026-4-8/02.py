import pandas as pd
from pandas import DataFrame
from pandas import Series

# 用列表形式存储小米三年6个学期的成绩
grades = [
    ['一年级上学期', 90, 95, 88],
    ['一年级下学期', 92, 93, 90],
    ['二年级上学期', 88, 96, 92],
    ['二年级下学期', 94, 91, 89],
    ['三年级上学期', 91, 94, 93],
    ['三年级下学期', 93, 97, 95]
]

df_grades = DataFrame(grades, columns=['学期', '语文', '数学', '英语'])

# 获取前两行数据
print("小米前两行成绩数据：")
print(df_grades.head(2).to_string(index=False))
