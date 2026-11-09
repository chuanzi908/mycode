# -*- coding: utf-8 -*-
"""生成商业计划书第七章所需的技术/模型图表（matplotlib 科学图）。"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, patches, colors
from matplotlib.colors import LinearSegmentedColormap

# ---- 中文字体 ----
for f in [r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\msyh.ttc",
          r"C:\Windows\Fonts\NotoSansSC-VF.ttf"]:
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Noto Sans SC"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"

OUT = os.path.join(os.path.dirname(__file__), "..", "figures", "model")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

# 统一配色（贴合“农业/科技”主题）
C_MAIN = "#2e7d32"   # 深绿
C_SUB = "#66bb6a"    # 浅绿
C_ACC = "#f9a825"    # 金黄
C_RED = "#e53935"    # 红
C_BLUE = "#1e88e5"
C_GRAY = "#90a4ae"

def save(fig, name):
    fig.savefig(os.path.join(OUT, name))
    plt.close(fig)
    print("saved", name)


# ============================================================
# 1. 标准卷积 vs 深度可分离卷积 参数量对比
# ============================================================
def conv_param_compare():
    Dk = 3
    channels = [32, 64, 128, 256, 512]
    std = [Dk * Dk * c * c for c in channels]
    ds = [Dk * Dk * c + c * c for c in channels]
    ratio = [s / d for s, d in zip(std, ds)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.6),
                                   gridspec_kw={"width_ratios": [1.6, 1]})
    x = np.arange(len(channels))
    w = 0.38
    b1 = ax1.bar(x - w / 2, np.array(std) / 1000, w, label="标准卷积", color=C_GRAY)
    b2 = ax1.bar(x + w / 2, np.array(ds) / 1000, w, label="深度可分离卷积", color=C_MAIN)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"M=N={c}" for c in channels])
    ax1.set_ylabel("参数量（千）")
    ax1.set_title("(a) 参数量对比（卷积核 $D_K=3$）")
    ax1.legend(frameon=False)
    for b in list(b1) + list(b2):
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 5,
                 f"{b.get_height():.0f}", ha="center", fontsize=7)

    ax2.plot(channels, ratio, "o-", color=C_ACC, lw=2)
    ax2.set_xlabel("通道数 M=N")
    ax2.set_ylabel("压缩倍数")
    ax2.set_title("(b) 参数量压缩倍数")
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0, max(ratio) * 1.15)
    for xi, r in zip(channels, ratio):
        ax2.text(xi, r + 0.3, f"{r:.1f}×", ha="center", fontsize=8)
    fig.tight_layout()
    save(fig, "conv_param_compare.png")


# ============================================================
# 2. Softmax 置信度输出示例
# ============================================================
def softmax_confidence():
    labels = ["稻瘟病", "纹枯病", "稻曲病", "胡麻叶斑病", "其他"]
    probs = [0.873, 0.062, 0.031, 0.018, 0.016]
    colors_ = [C_MAIN, C_SUB, C_SUB, C_SUB, C_GRAY]
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    bars = ax.barh(labels[::-1], probs[::-1], color=colors_[::-1], alpha=0.9)
    ax.set_xlabel("置信度 $p_k$")
    ax.set_xlim(0, 1)
    ax.set_title("Softmax 识别置信度输出（Top-5）")
    for b, p in zip(bars, probs[::-1]):
        ax.text(b.get_width() + 0.015, b.get_y() + b.get_height() / 2,
                f"{p * 100:.1f}%", va="center", fontsize=9)
    ax.axvline(0.5, ls="--", color=C_RED, alpha=0.6, lw=1)
    ax.text(0.505, -0.4, "判定阈值", color=C_RED, fontsize=8)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    save(fig, "softmax_confidence.png")


# ============================================================
# 3. 交叉熵训练损失收敛曲线
# ============================================================
def training_loss():
    np.random.seed(1)
    ep = np.arange(1, 61)
    train = 2.4 * np.exp(-ep / 14) + 0.18 + np.random.normal(0, 0.02, len(ep))
    val = 2.5 * np.exp(-ep / 13) + 0.22 + np.random.normal(0, 0.025, len(ep))
    val[-8:] += np.linspace(0, 0.06, 8)  # 轻微过拟合
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(ep, train, lw=2, color=C_BLUE, label="训练损失")
    ax.plot(ep, val, lw=2, color=C_ACC, label="验证损失")
    ax.axvline(40, ls=":", color=C_GRAY, alpha=0.8)
    ax.text(40.8, 1.6, "早停点", color=C_GRAY, fontsize=8)
    ax.set_xlabel("训练轮次 Epoch")
    ax.set_ylabel("交叉熵损失 $Loss$")
    ax.set_title("模型训练损失收敛曲线")
    ax.legend(frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "training_loss.png")


# ============================================================
# 4. LSTM 病虫害发生概率时序预测
# ============================================================
def lstm_forecast():
    np.random.seed(3)
    t = np.arange(60)
    season = 0.28 * np.sin(2 * np.pi * t / 30) + 0.1 * np.sin(2 * np.pi * t / 7)
    trend = 0.003 * t
    actual = 0.45 + season + trend + np.random.normal(0, 0.04, len(t))
    actual = np.clip(actual, 0, 1)
    hist, fut = t[:45], t[45:]
    pred = 0.45 + (0.28 * np.sin(2 * np.pi * fut / 30)
                   + 0.1 * np.sin(2 * np.pi * fut / 7) + 0.003 * fut)
    pred = np.clip(pred + np.random.normal(0, 0.02, len(fut)), 0, 1)
    lo = np.clip(pred - 0.06, 0, 1)
    hi = np.clip(pred + 0.06, 0, 1)

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(hist, actual[:45], lw=2, color=C_BLUE, label="历史观测")
    ax.plot(fut, pred, lw=2, color=C_RED, label="LSTM 预测")
    ax.fill_between(fut, lo, hi, color=C_RED, alpha=0.15, label="置信区间")
    ax.axhline(0.65, ls="--", color=C_ACC, lw=1.4, label="预警阈值 0.65")
    ax.axvline(45, ls=":", color=C_GRAY, lw=1)
    ax.text(45.3, 0.95, "预测起点", color=C_GRAY, fontsize=8)
    # 标注预警触发点
    trig = np.where(pred > 0.65)[0]
    if len(trig):
        ti = trig[0]
        ax.plot(fut[ti], pred[ti], "o", color=C_ACC, ms=8, zorder=5)
        ax.annotate("触发预警", (fut[ti], pred[ti]), xytext=(fut[ti] - 4, pred[ti] + 0.22),
                    arrowprops=dict(arrowstyle="->", color=C_ACC), fontsize=9, color=C_ACC)
    ax.set_xlabel("时间（天）")
    ax.set_ylabel("发生概率")
    ax.set_title("LSTM 病虫害发生概率预测（未来 15 天）")
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "lstm_forecast.png")


# ============================================================
# 5. 熵权法多属性决策：属性权重 + Top3 方案得分
# ============================================================
def entropy_madm():
    attrs = ["药效", "成本", "毒性", "窗口期适配", "持效期"]
    weights = [0.34, 0.22, 0.19, 0.16, 0.09]
    schemes = ["方案 A\n(苯醚甲环唑)", "方案 B\n(吡唑醚菌酯)", "方案 C\n(噻呋酰胺)"]
    scores = [0.874, 0.812, 0.769]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.6),
                                   gridspec_kw={"width_ratios": [1.1, 1]})
    ax1.bar(attrs, weights, color=[C_MAIN, C_SUB, C_SUB, C_SUB, C_SUB], alpha=0.9)
    ax1.set_ylabel("熵权 $w_j$")
    ax1.set_title("(a) 熵权法属性权重")
    ax1.set_ylim(0, 0.4)
    for i, wj in enumerate(weights):
        ax1.text(i, wj + 0.01, f"{wj:.2f}", ha="center", fontsize=9)
    ax1.grid(axis="y", alpha=0.3)

    bars = ax2.barh(schemes[::-1], scores[::-1],
                    color=[C_MAIN, C_SUB, C_GRAY], alpha=0.9)
    ax2.set_xlabel("综合得分 $S_i$")
    ax2.set_xlim(0, 1)
    ax2.set_title("(b) 防治方案综合得分 Top-3")
    for b, s in zip(bars, scores[::-1]):
        ax2.text(b.get_width() + 0.015, b.get_y() + b.get_height() / 2,
                 f"{s:.3f}", va="center", fontsize=9)
    ax2.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    save(fig, "entropy_madm.png")


# ============================================================
# 6. 知识蒸馏 + INT8 量化：模型体积 / 精度 / 延迟
# ============================================================
def model_compress():
    names = ["云端大模型\n(教师)", "端侧小模型\n(学生)", "知识蒸馏后", "INT8量化后"]
    size = [86.0, 8.6, 8.2, 2.4]       # MB
    acc = [96.4, 93.1, 95.0, 94.8]     # %
    lat = [0.0, 180, 175, 68]          # ms（教师云端不显示端侧延迟）

    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.4))
    colors_ = [C_GRAY, C_BLUE, C_SUB, C_MAIN]

    axes[0].bar(names, size, color=colors_, alpha=0.9)
    axes[0].set_ylabel("模型体积（MB）")
    axes[0].set_title("(a) 模型体积")
    axes[0].tick_params(axis="x", labelsize=7)
    for i, v in enumerate(size):
        axes[0].text(i, v + 2, f"{v:.1f}", ha="center", fontsize=8)

    axes[1].bar(names, acc, color=colors_, alpha=0.9)
    axes[1].set_ylabel("识别精度（%）")
    axes[1].set_ylim(88, 100)
    axes[1].set_title("(b) 识别精度")
    axes[1].tick_params(axis="x", labelsize=7)
    for i, v in enumerate(acc):
        axes[1].text(i, v + 0.2, f"{v:.1f}", ha="center", fontsize=8)

    axes[2].bar(names[1:], lat[1:], color=colors_[1:], alpha=0.9)
    axes[2].set_ylabel("端侧推理延迟（ms）")
    axes[2].set_title("(c) 端侧推理延迟")
    axes[2].tick_params(axis="x", labelsize=7)
    for i, v in enumerate(lat[1:]):
        axes[2].text(i, v + 5, f"{v}", ha="center", fontsize=8)

    fig.tight_layout()
    save(fig, "model_compress.png")


# ============================================================
# 7. YOLOv8-nano 目标检测示意（叶片 + 病斑框）
# ============================================================
def _draw_leaf(ax):
    leaf = patches.Ellipse((0.5, 0.5), 0.72, 0.36, angle=18, fc="#7cb342",
                           ec="#33691e", lw=1.5, alpha=0.85)
    ax.add_patch(leaf)
    # 主叶脉
    ax.plot([0.2, 0.8], [0.32, 0.68], color="#558b2f", lw=1.6)
    for j, dy in enumerate([0.06, 0.12, -0.06, -0.12]):
        ax.plot([0.4, 0.62], [0.5 + dy * 0.5, 0.5 + dy], color="#558b2f", lw=1.0, alpha=0.7)

def yolo_detection():
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    _draw_leaf(ax)
    spots = [(0.42, 0.55, 0.05), (0.60, 0.46, 0.045), (0.35, 0.38, 0.04)]
    for sx, sy, r in spots:
        ax.add_patch(patches.Ellipse((sx, sy), r * 1.6, r, angle=20,
                     fc="#8d6e63", ec="#5d4037", alpha=0.9))
    boxes = [((0.36, 0.34, 0.14, 0.24), "稻瘟病 0.91"),
             ((0.54, 0.40, 0.14, 0.18), "稻瘟病 0.87")]
    for (x, y, w, h), lbl in boxes:
        ax.add_patch(patches.Rectangle((x, y), w, h, fill=False, ec=C_RED, lw=2))
        ax.text(x, y + h + 0.03, lbl, color=C_RED, fontsize=9, fontweight="bold")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("YOLOv8-nano 田间病斑目标检测示意", fontsize=11)
    for s in ax.spines.values():
        s.set_edgecolor("#cfd8dc")
    fig.tight_layout()
    save(fig, "yolo_detection.png")


# ============================================================
# 8. CBAM 注意力机制示意（通道 + 空间注意力）
# ============================================================
def _make_leaf_img():
    np.random.seed(7)
    y, x = np.mgrid[0:80, 0:120]
    img = np.zeros((80, 120, 3))
    # 叶片形状掩膜
    cx, cy, a, b = 60, 40, 46, 20
    mask = ((x - cx) / a) ** 2 + ((y - cy) / b) ** 2 <= 1
    base = 0.55 + 0.2 * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 900)
    img[..., 1] = base * mask          # 绿色通道
    img[..., 0] = 0.25 * base * mask   # 少量红
    img[..., 2] = 0.15 * base * mask
    # 病斑
    for (sx, sy, r) in [(45, 32, 6), (72, 45, 5), (38, 48, 5)]:
        d = ((x - sx) ** 2 + (y - sy) ** 2) <= r ** 2
        img[d, 0] = 0.45; img[d, 1] = 0.28; img[d, 2] = 0.12
    img *= mask[..., None]
    return img

def cbam_attention():
    img = _make_leaf_img()
    # 空间注意力：病斑位置高响应
    y, x = np.mgrid[0:80, 0:120]
    att = np.zeros((80, 120))
    for (sx, sy, r) in [(45, 32, 6), (72, 45, 5), (38, 48, 5)]:
        att += np.exp(-((x - sx) ** 2 + (y - sy) ** 2) / (2 * r ** 2))
    att = att / att.max()

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2))
    axes[0].imshow(img); axes[0].set_title("(a) 原图", fontsize=10)
    axes[0].axis("off")
    axes[1].imshow(img, alpha=0.5)
    axes[1].imshow(att, cmap="jet", alpha=0.6)
    axes[1].set_title("(b) 通道注意力加权", fontsize=10)
    axes[1].axis("off")
    hm = axes[2].imshow(att, cmap="jet")
    axes[2].set_title("(c) 空间注意力热力图", fontsize=10)
    axes[2].axis("off")
    fig.colorbar(hm, ax=axes[2], fraction=0.046, pad=0.04)
    fig.suptitle("CBAM 卷积注意力：聚焦病斑区域、抑制背景", fontsize=11, y=1.02)
    fig.tight_layout()
    save(fig, "cbam_attention.png")


# ============================================================
# 9. 混淆矩阵（验证集评估）
# ============================================================
def confusion_matrix():
    classes = ["稻瘟病", "纹枯病", "稻曲病", "胡麻叶斑", "健康"]
    # 行=真实, 列=预测（每行和=100）
    cm = np.array([
        [93, 3, 2, 1, 1],
        [4, 90, 3, 1, 2],
        [2, 3, 92, 2, 1],
        [2, 2, 3, 91, 2],
        [1, 1, 1, 2, 95],
    ])
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    im = ax.imshow(cm, cmap=LinearSegmentedColormap.from_list(
        "g", ["#ffffff", C_SUB, C_MAIN]), vmin=0, vmax=100)
    ax.set_xticks(range(len(classes))); ax.set_yticks(range(len(classes)))
    ax.set_xticklabels(classes); ax.set_yticklabels(classes)
    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    ax.set_xlabel("预测类别"); ax.set_ylabel("真实类别")
    for i in range(len(classes)):
        for j in range(len(classes)):
            ax.text(j, i, f"{cm[i, j]}", ha="center", va="center",
                    color="white" if cm[i, j] > 55 else "#333", fontsize=9)
    ax.set_title("病虫害识别混淆矩阵（验证集，%）")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    save(fig, "confusion_matrix.png")


if __name__ == "__main__":
    conv_param_compare()
    softmax_confidence()
    training_loss()
    lstm_forecast()
    entropy_madm()
    model_compress()
    yolo_detection()
    cbam_attention()
    confusion_matrix()
    print("ALL MODEL CHARTS DONE ->", OUT)
