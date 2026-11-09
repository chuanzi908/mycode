# 数据预处理 + DNN + LSTM 关键代码片段
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# 数据加载
df = pd.read_csv('data_stocks.csv')

# 划分与归一化
scaler = MinMaxScaler(feature_range=(-1,1))
data_scaled = scaler.fit_transform(df.drop(['DATE'], axis=1))
train_size = int(len(data_scaled)*0.8)
train_data = data_scaled[:train_size]
test_data = data_scaled[train_size:]

# DNN模型
model = Sequential()
model.add(Dense(1024, activation='relu', input_dim=data_scaled.shape[1]))
model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# LSTM模型
seq_len = 5
X_train, y_train = [], []
for i in range(seq_len, len(train_data)):
    X_train.append(train_data[i-seq_len:i, 0])
    y_train.append(train_data[i, 0])
X_train = np.array(X_train).reshape(-1, seq_len, 1)

model_lstm = Sequential()
model_lstm.add(LSTM(128, activation='relu', input_shape=(seq_len,1)))
model_lstm.add(Dense(1))
model_lstm.compile(optimizer='adam', loss='mse')