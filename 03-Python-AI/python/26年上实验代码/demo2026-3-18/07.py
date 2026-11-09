#通过控制台输入要记录的内容,并生成每日笔记
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

print(f"📝 {today} 每日笔记")
print("="*40)

# 一次性输入所有内容
content = input("请输入今日总结:\n")

# 保存笔记
filename = f"笔记_{today}.txt"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(f"日期：{today}\n")
    f.write("="*40 + "\n")
    f.write(content)

print(f"\n✓ 笔记已保存：{filename}")
