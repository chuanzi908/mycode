import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def job_forecast():
    csv_path = "employment.csv"
    if not os.path.exists(csv_path):
        print(f"错误：找不到文件 '{csv_path}'")
        print("请确保 employment.csv 文件在当前目录下")
        return
    
    df = pd.read_csv(csv_path)
    demand = df['岗位需求数'].values

    n = len(demand)

    # 移动平均
    def ma_calc(data,win):
        return pd.Series(data).rolling(window=win).mean()
    ma3 = ma_calc(demand,3)
    ma6 = ma_calc(demand,6)
    ma12 = ma_calc(demand,12)

    # 绘图
    plt.figure(figsize=(12,6))
    plt.plot(demand,label='原始需求',color='black')
    plt.plot(ma3,label='MA3',color='red')
    plt.plot(ma6,label='MA6',color='green')
    plt.plot(ma12,label='MA12',color='blue')
    plt.legend()
    plt.title('岗位需求数及移动平均线')
    plt.xlabel('月份')
    plt.ylabel('岗位需求数')
    plt.grid(alpha=0.3)
    plt.savefig("market_ma.png",dpi=300)
    plt.show()

    # 取近24个月
    train_len = min(24,n)
    train_y = demand[-train_len:]
    train_x = np.arange(train_len)

    # 三次多项式拟合
    z = np.polyfit(train_x,train_y,3)
    p = np.poly1d(z)
    fit_y = p(train_x)

    # 预测未来3个月
    pred_x = np.arange(train_len, train_len+3)
    pred_y = np.round(p(pred_x)).astype(int)
    print("未来3个月岗位需求预测值：",pred_y)

    # 误差计算 RMSE MAPE
    rmse = np.sqrt(np.mean((train_y-fit_y)**2)).round(2)
    mape = np.mean(np.abs((train_y-fit_y)/train_y))*100
    mape = round(mape,2)
    print(f"均方根误差RMSE：{rmse}")
    print(f"平均绝对百分比误差MAPE：{mape}%")

    # 写入报告
    with open("forecast_report.txt","w",encoding="utf-8") as f:
        f.write("=== 就业市场预测分析报告 ===\n")
        f.write(f"拟合多项式系数：{z.round(2)}\n")
        f.write(f"RMSE：{rmse}\n")
        f.write(f"MAPE：{mape}%\n")
        f.write(f"未来3个月预测值：{pred_y.tolist()}\n")

if __name__ == "__main__":
    job_forecast()