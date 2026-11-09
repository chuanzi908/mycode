# 自动作诗最终优化版 | 训练更充分 + 生成更通顺
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# ===================== 1. 【关键】再扩充唐诗语料，增加句式多样性 =====================
poetry_corpus = """
床前明月光，疑是地上霜。举头望明月，低头思故乡。
白日依山尽，黄河入海流。欲穷千里目，更上一层楼。
春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。
松下问童子，言师采药去。只在此山中，云深不知处。
空山不见人，但闻人语响。返景入深林，复照青苔上。
独坐幽篁里，弹琴复长啸。深林人不知，明月来相照。
红豆生南国，春来发几枝。愿君多采撷，此物最相思。
慈母手中线，游子身上衣。临行密密缝，意恐迟迟归。
海内存知己，天涯若比邻。无为在歧路，儿女共沾巾。
离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。
远芳侵古道，晴翠接荒城。又送王孙去，萋萋满别情。
日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。
朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不住，轻舟已过万重山。
好雨知时节，当春乃发生。随风潜入夜，润物细无声。
野径云俱黑，江船火独明。晓看红湿处，花重锦官城。
千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。
众鸟高飞尽，孤云独去闲。相看两不厌，只有敬亭山。
鸣筝金粟柱，素手玉房前。欲得周郎顾，时时误拂弦。
终南阴岭秀，积雪浮云端。林表明霁色，城中增暮寒。
移舟泊烟渚，日暮客愁新。野旷天低树，江清月近人。
人闲桂花落，夜静春山空。月出惊山鸟，时鸣春涧中。
木末芙蓉花，山中发红萼。涧户寂无人，纷纷开且落。
时人不识余心乐，将谓偷闲学少年。
清明时节雨纷纷，路上行人欲断魂。借问酒家何处有，牧童遥指杏花村。
向晚意不适，驱车登古原。夕阳无限好，只是近黄昏。
"""

# 清理文本
text = poetry_corpus.replace("\n", "").replace(" ", "")

# 字 ↔ 数字 映射
chars = sorted(list(set(text)))
vocab_size = len(chars)
char2idx = {c: i for i, c in enumerate(chars)}
idx2char = {i: c for i, c in enumerate(chars)}

# ===================== 2. 【优化】序列长度适配五言诗，平衡上下文长度 =====================
SEQ_LENGTH = 10  # 平衡上下文信息，既不会太短学不到规律，也不会太长导致训练困难
step = 1

sentences = []
next_chars = []

for i in range(0, len(text) - SEQ_LENGTH, step):
    sentences.append(text[i: i + SEQ_LENGTH])
    next_chars.append(text[i + SEQ_LENGTH])

# 转为数字序列
x = np.zeros((len(sentences), SEQ_LENGTH), dtype=np.int32)
y = np.zeros(len(sentences), dtype=np.int32)

for i, s in enumerate(sentences):
    for t, c in enumerate(s):
        x[i, t] = char2idx[c]
    y[i] = char2idx[next_chars[i]]

# ===================== 3. 【优化】模型结构升级，训练更稳定 =====================
model = Sequential([
    Embedding(vocab_size, 128, input_length=SEQ_LENGTH),
    LSTM(256, return_sequences=True),  # 双层LSTM，学习能力更强
    Dropout(0.2),
    LSTM(128),
    Dropout(0.2),
    Dense(vocab_size, activation='softmax')
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ===================== 4. 【优化】训练参数，保证模型学透规律 =====================
print("开始训练...")
# 增加训练轮次，让模型学到足够的诗歌规律；batch_size适中，训练更稳定
model.fit(x, y, batch_size=16, epochs=50)

# ===================== 5. 【核心】生成函数优化，平衡通顺度与创造性 =====================
def generate_poem(start_text, gen_len=20, temperature=1.0):
    """
    start_text: 开头诗句（建议5-10个字，和SEQ_LENGTH匹配）
    gen_len: 生成字数
    temperature: 创作风格（1.0为最佳，既不重复，也不乱来）
    """
    generated = start_text

    for _ in range(gen_len):
        # 严格取最后SEQ_LENGTH个字作为输入
        x_input = np.zeros((1, SEQ_LENGTH))
        for t, char in enumerate(generated[-SEQ_LENGTH:]):
            x_input[0, t] = char2idx[char]

        # 预测下一个字的概率
        preds = model.predict(x_input, verbose=0)[0]

        # 温度采样优化，避免数值错误，同时控制随机性
        preds = np.clip(preds, 1e-8, None)
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)

        # 随机采样下一个字
        next_index = np.random.choice(vocab_size, p=preds)
        next_char = idx2char[next_index]

        generated += next_char

    return generated

# ===================== 6. 开始写诗 =====================
print("\n【生成诗歌】")
poem = generate_poem(start_text="床前明月光", gen_len=20, temperature=1.0)
print(poem)