from scipy import stats
import matplotlib.pyplot as plt


def binomial_pmf(n=10, p=0.5):
    """
    二项分布概率质量函数可视化
    :param n: 试验次数
    :param p: 每次试验成功的概率
    """
    # 创建二项分布
    bin_dist = stats.binom(n, p)

    # x轴：可能的成功次数 (0到n)
    x = list(range(0, n + 1))

    # 计算每个成功次数的概率
    pmf = [bin_dist.pmf(k) for k in x]

    # 转换为字符串用于显示
    x_name = [str(k) for k in x]

    # 绘制柱状图
    plt.bar(x, pmf, width=0.5)

    # 设置标签和标题
    plt.xticks(x, x_name)
    plt.ylabel("probability")
    plt.xlabel("number of successes")
    plt.title(f"Binomial Distribution (n={n}, p={p})")
    plt.show()


# 示例：抛10次硬币，正面朝上的概率分布
binomial_pmf(n=10, p=0.5)
