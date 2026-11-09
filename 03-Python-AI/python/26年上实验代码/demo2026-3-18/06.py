#获取一段新闻,对新闻内容进行分词,将分词后的内容形成图片
import requests
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt

# 1. 获取新闻内容（这里使用示例新闻文本）
news_text = """
2026 年 3 月 18 日，科技创新大会在北京召开。会议强调了人工智能、大数据、云计算等技术的发展重要性。
专家指出，数字经济将成为未来发展的主要方向。各级政府正在加大对科技企业的支持力度，推动产业升级和转型。
在教育领域，在线教育平台快速发展，为学生提供了更多学习资源。医疗健康方面，远程医疗技术得到广泛应用，
提高了医疗服务的可及性。环境保护工作也在稳步推进，绿色发展理念深入人心。
"""


# 2. 对新闻内容进行分词
def segment_text(text):
    """使用 jieba 进行中文分词"""
    # 添加一些专业词汇到词典
    jieba.add_word("人工智能")
    jieba.add_word("大数据")
    jieba.add_word("云计算")
    jieba.add_word("数字经济")

    # 分词
    words = jieba.lcut(text)

    # 过滤掉标点符号和空白字符
    filtered_words = [word for word in words if word.strip() and len(word) > 1]

    return " ".join(filtered_words)


# 3. 生成词云图片
def create_wordcloud(text, output_file="wordcloud.png"):
    """根据分词后的文本生成词云"""
    # 进行分词
    segmented_text = segment_text(text)

    print("分词结果:")
    print(segmented_text)
    print("\n" + "=" * 50)

    # 创建词云对象
    wc = WordCloud(
        font_path="simhei.ttf",  # 中文字体路径（如果没有可以注释掉）
        width=800,
        height=600,
        background_color='white',
        max_words=100,
        colormap='viridis'
    )

    # 生成词云
    wc.generate_from_text(segmented_text)

    # 保存图片
    wc.to_file(output_file)
    print(f"✓ 词云图片已保存为：{output_file}")

    # 显示词云
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title("新闻词云图")
    plt.show()


# 主程序
if __name__ == "__main__":
    print("📰 新闻分词与词云生成系统")
    print("=" * 50)

    try:
        create_wordcloud(news_text)
    except Exception as e:
        print(f"发生错误：{e}")
        print("\n💡 提示：如果字体文件不存在，可以下载 simhei.ttf 或注释掉 font_path 参数")

