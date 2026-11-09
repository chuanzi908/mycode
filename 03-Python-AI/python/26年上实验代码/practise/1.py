import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def score_analysis():
    # 读取数据
    df = pd.read_excel("scores.xlsx")
    course_cols = ['高等数学','大学英语','Python程序设计','体育']

    # 缺失值按专业课程平均分填充
    for major in df['专业'].unique():
        major_data = df[df['专业'] == major]
        for col in course_cols:
            avg_val = major_data[col].mean()
            df.loc[(df['专业']==major) & (df[col].isnull()), col] = avg_val

    # 计算总分、平均分
    df['总分'] = df[course_cols].sum(axis=1)
    df['平均分'] = df[course_cols].mean(axis=1).round(2)

    # 按平均分降序，输出前10名
    top10 = df.sort_values('平均分',ascending=True).head(10)
    print("===== 平均分前10名学生 =====")
    print(top10[['学号','姓名','专业','平均分']])

    # 各专业统计
    res = []
    for major in df['专业'].unique():
        d = df[df['专业']==major]
        avg_all = d['平均分'].mean().round(2)
        max_all = d['平均分'].max().round(2)
        min_all = d['平均分'].min().round(2)
        pass_rate = (d['平均分']>=60).sum() / len(d)
        res.append({
            '专业':major,
            '专业平均分':avg_all,
            '专业最高分':max_all,
            '专业最低分':min_all,
            '及格率':round(pass_rate,2)
        })
    stat_df = pd.DataFrame(res)
    print("\n===== 各专业成绩统计 =====")
    print(stat_df)

    # 绘图
    plt.figure(figsize=(10,6))
    plt.barh(stat_df['专业'], stat_df['专业平均分'])
    plt.xlabel('平均分')
    plt.ylabel('专业')
    plt.title('各专业平均分对比')
    plt.grid(axis='x',alpha=0.3)
    plt.savefig("major_avg.png",dpi=300,bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    score_analysis()