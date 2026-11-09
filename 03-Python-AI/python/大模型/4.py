import json
import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer
)

# 【关键】先设置国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 配置
MODEL_ID = "qwen/Qwen2.5-0.5B-Instruct"
project_dir = "output/legal_consultation_model_cpu"
DATA_PATH = project_dir + "/data/processed/train.jsonl"
OUTPUT_DIR = project_dir + "/models/legal_model_cpu"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 训练参数
BATCH_SIZE = 1
NUM_EPOCHS = 1
LEARNING_RATE = 5e-5
MAX_LENGTH = 512
device = "cpu"

print("1. 加载模型和分词器...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
    dtype=torch.float32,
    low_cpu_mem_usage=True
).to(device)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
print(" 模型加载成功")

print("2. 加载数据集...")


def load_jsonl(path):
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


data = load_jsonl(DATA_PATH)
print(f" 加载了{len(data)} 条数据")


def tokenize_function(examples):
    texts = [
        f"{ex['system']}\n问题:{ex['user']}\n回答:{ex['assistant']}{tokenizer.eos_token}"
        for ex in examples
    ]
    tokenized = tokenizer(
        texts,
        truncation=True,
        max_length=MAX_LENGTH,
        padding="max_length",
        return_tensors="pt"
    )
    tokenized["labels"] = tokenized["input_ids"].clone()
    return tokenized


print("3. 处理数据...")
tokenized_data = tokenize_function(data)
input_ids = tokenized_data["input_ids"].to(device)
attention_mask = tokenized_data["attention_mask"].to(device)
labels = tokenized_data["labels"].to(device)
print(f" 数据处理完成")

print("4. 配置优化器...")
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

print("5. 开始训练（原生PyTorch循环）...")
model.train()
for epoch in range(NUM_EPOCHS):
    print(f"\n--- Epoch {epoch + 1}/{NUM_EPOCHS} ---")
    optimizer.zero_grad()

    # 前向传播
    outputs = model(
        input_ids=input_ids,
        attention_mask=attention_mask,
        labels=labels
    )
    loss = outputs.loss

    # 反向传播
    loss.backward()
    optimizer.step()

    print(f" 训练损失: {loss.item():.4f}")

print("\n训练完成!")
print(f"6. 保存模型到: {OUTPUT_DIR}")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("模型已保存!")
print(f" 模型大小: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M 参数")