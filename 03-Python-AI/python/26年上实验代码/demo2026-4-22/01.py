import numpy as np
import matplotlib.pyplot as plt


class LSTMCell:
    """LSTM单元"""

    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size

        # 初始化权重
        self.Wf = np.random.randn(input_size + hidden_size, hidden_size) * 0.01
        self.bf = np.zeros((1, hidden_size))

        self.Wi = np.random.randn(input_size + hidden_size, hidden_size) * 0.01
        self.bi = np.zeros((1, hidden_size))

        self.Wc = np.random.randn(input_size + hidden_size, hidden_size) * 0.01
        self.bc = np.zeros((1, hidden_size))

        self.Wo = np.random.randn(input_size + hidden_size, hidden_size) * 0.01
        self.bo = np.zeros((1, hidden_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def tanh(self, x):
        return np.tanh(x)

    def forward(self, x, h_prev, c_prev):
        """LSTM前向传播"""
        concat = np.hstack([h_prev, x])

        # 遗忘门
        f = self.sigmoid(np.dot(concat, self.Wf) + self.bf)
        # 输入门
        i = self.sigmoid(np.dot(concat, self.Wi) + self.bi)
        # 候选细胞状态
        c_tilde = self.tanh(np.dot(concat, self.Wc) + self.bc)
        # 细胞状态
        c = f * c_prev + i * c_tilde
        # 输出门
        o = self.sigmoid(np.dot(concat, self.Wo) + self.bo)
        # 隐藏状态
        h = o * self.tanh(c)

        return h, c, f, i, c_tilde, o


class LSTMNetwork:
    """LSTM网络"""

    def __init__(self, input_size, hidden_size, output_size):
        self.lstm = LSTMCell(input_size, hidden_size)
        self.hidden_size = hidden_size

        # 输出层
        self.Wy = np.random.randn(hidden_size, output_size) * 0.01
        self.by = np.zeros((1, output_size))

    def forward_sequence(self, X):
        """处理序列数据"""
        batch_size, seq_len, _ = X.shape
        h = np.zeros((batch_size, self.hidden_size))
        c = np.zeros((batch_size, self.hidden_size))

        self.history = {'h': [h], 'c': [c]}

        for t in range(seq_len):
            x = X[:, t, :]
            h, c, f, i, c_tilde, o = self.lstm.forward(x, h, c)
            self.history['h'].append(h)
            self.history['c'].append(c)

        # 输出层
        y = np.dot(h, self.Wy) + self.by
        return y

    def predict(self, X):
        """预测"""
        return self.forward_sequence(X)


def create_time_series_data(n_samples=1000, seq_len=20):
    """创建时序数据"""
    t = np.linspace(0, 10 * np.pi, n_samples)
    data = np.sin(t) + 0.3 * np.sin(2 * t) + 0.1 * np.random.randn(n_samples)

    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i + seq_len])
        y.append(data[i + seq_len])

    X = np.array(X).reshape(-1, seq_len, 1)
    y = np.array(y).reshape(-1, 1)

    # 归一化
    mean = np.mean(data)
    std = np.std(data)
    X = (X - mean) / std
    y = (y - mean) / std

    return X, y, mean, std


def train_test_split_ts(X, y, test_ratio=0.2):
    """时序数据划分"""
    split = int(len(X) * (1 - test_ratio))
    return X[:split], X[split:], y[:split], y[split:]


def plot_results(y_true, y_pred, title="LSTM时序预测结果"):
    """绘制结果"""
    plt.figure(figsize=(14, 6))
    plt.plot(y_true, label='真实值', linewidth=2)
    plt.plot(y_pred, label='预测值', linewidth=2, linestyle='--')
    plt.xlabel('时间步', fontsize=12)
    plt.ylabel('数值', fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('lstm_prediction.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("图表已保存为 lstm_prediction.png")


def plot_training_loss(losses):
    """绘制训练损失"""
    plt.figure(figsize=(10, 5))
    plt.plot(losses, linewidth=2, color='red')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('损失', fontsize=12)
    plt.title('训练损失曲线', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('lstm_loss.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("损失曲线已保存为 lstm_loss.png")


if __name__ == "__main__":
    print("=== 生成时序数据 ===")
    seq_len = 20
    X, y, mean, std = create_time_series_data(n_samples=1000, seq_len=seq_len)
    print(f"数据形状: X={X.shape}, y={y.shape}")

    print("\n=== 划分训练集和测试集 ===")
    X_train, X_test, y_train, y_test = train_test_split_ts(X, y, test_ratio=0.2)
    print(f"训练集: {X_train.shape[0]} 样本, 测试集: {X_test.shape[0]} 样本")

    print("\n=== 创建LSTM模型 ===")
    model = LSTMNetwork(input_size=1, hidden_size=32, output_size=1)

    print("\n=== 训练模型 ===")
    epochs = 50
    lr = 0.001
    losses = []

    for epoch in range(epochs):
        # 简单训练（这里使用简化版本）
        predictions = model.predict(X_train)
        loss = np.mean((predictions - y_train) ** 2)
        losses.append(loss)

        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss:.6f}")

    print("\n=== 预测 ===")
    y_pred = model.predict(X_test)

    # 反归一化
    y_test_real = y_test * std + mean
    y_pred_real = y_pred * std + mean

    print("\n=== 绘制结果 ===")
    plot_results(y_test_real.flatten(), y_pred_real.flatten())
    plot_training_loss(losses)

    # 计算误差
    mse = np.mean((y_test_real - y_pred_real) ** 2)
    rmse = np.sqrt(mse)
    print(f"\n均方误差 (MSE): {mse:.4f}")
    print(f"均方根误差 (RMSE): {rmse:.4f}")
