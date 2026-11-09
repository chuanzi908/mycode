# course_chat.py 课程咨询主程序
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import tkinter as tk

# 1.加载数据集
try:
    df = pd.read_csv("course_data.csv", encoding="utf-8")
    questions = df["question"].tolist()
    labels = df["label"].tolist()
    answers = df["answer"].tolist()
except FileNotFoundError:
    print("错误：找不到 course_data.csv 文件！")
    print("请先创建课程数据文件")
    exit()

# 分词处理
def cut_word(text):
    return " ".join(jieba.cut(text))
cut_q = [cut_word(i) for i in questions]

# TF-IDF特征+模型训练
tfidf = TfidfVectorizer()
x_train = tfidf.fit_transform(cut_q)
model = MultinomialNB()
model.fit(x_train,labels)

# 问答查询函数
def get_ans(input_text):
    cut_in = cut_word(input_text)
    vec = tfidf.transform([cut_in])
    pred = model.predict(vec)[0]
    # 找到预测标签对应的索引
    try:
        idx = labels.index(pred)
        return answers[idx]
    except ValueError:
        return "抱歉，暂时无法回答您的问题"

# GUI界面
def send_msg():
    msg = entry.get()
    res = get_ans(msg)
    text_box.insert(tk.END,f"用户：{msg}\n机器人：{res}\n")

root = tk.Tk()
root.title("专业课智能咨询系统")
entry = tk.Entry(root,width=50)
entry.pack()
tk.Button(root,text="发送咨询",command=send_msg).pack()
text_box = tk.Text(root,width=70,height=15)
text_box.pack()
root.mainloop()
