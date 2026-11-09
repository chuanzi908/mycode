import numpy as np
import matplotlib.pyplot as plt

# ===================== 步骤1：生成模拟数据 =====================
# 生成x轴数据与噪声数据
x = np.linspace(0, 10, 100)
np.random.seed(42)  # 固定随机种子

# 带噪声的线性数据
y_true = 2 * x + 5 + np.random.normal(0, 1, len(x))
# 带噪声的非线性数据（二次）
y_nonlinear = 0.5 * x**2 + 2 * x + 3 + np.random.normal(0, 2, len(x))

# ===================== 步骤2：线性拟合与评估 =====================
# 线性拟合（一次多项式）
linear_params = np.polyfit(x, y_true, 1)
linear_fit = np.poly1d(linear_params)

# 计算拟合误差（MSE）
linear_mse = np.mean((linear_fit(x) - y_true)**2)

print(f"拟合参数: {linear_params}")
print(f"均方误差: {linear_mse:.4f}")

# ===================== 可选：简单可视化 =====================
plt.scatter(x, y_true, color='gray', label='带噪声的原始数据')
plt.plot(x, linear_fit(x), 'r-', label='线性拟合结果')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()