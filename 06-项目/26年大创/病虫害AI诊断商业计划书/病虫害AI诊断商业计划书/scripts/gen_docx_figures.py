# -*- coding: utf-8 -*-
"""生成 Word 版项目计划书需要的两张配图：
   1) func_loop.png      四功能闭环（拍照识别 → 防治建议 → 搜索查询 → 预防推送）
   2) tech_roadmap.png   技术路线总览（端侧 → 服务端 → 数据层 + 模型管线 + 农机协同）
   用无头 Edge 渲染 HTML 后截图，风格与文档内其它配图保持一致。
"""
import subprocess
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "figures" / "docx"
OUT.mkdir(parents=True, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 品牌配色（与文档内既有配图一致）
DARK = "#1c3d2e"      # 主深绿：表头 / 主链路
GREEN = "#2e7d32"     # 强调绿
MINT = "#4a7c59"      # 次级绿
CARD = "#f4f7f5"      # 卡片底
CARD2 = "#edf1ee"     # 次级底
LINE = "#dde2e0"      # 描边
INK = "#3a4a44"       # 正文墨色
GRAY = "#778b82"      # 辅助灰
FONT = "'Microsoft YaHei','PingFang SC',sans-serif"

SHELL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{background:#fff;font-family:{font};-webkit-font-smoothing:antialiased;}}
.wrap{{width:1160px;padding:34px 38px 22px;}}
.h1{{font-size:25px;font-weight:700;color:{dark};letter-spacing:.3px;}}
.sub{{font-size:13px;color:{gray};margin-top:9px;padding-left:1px;}}
.foot{{margin-top:20px;padding-top:12px;border-top:1px solid {line};
      font-size:11.5px;color:{gray};line-height:1.7;}}
{extra}
</style></head><body><div class="wrap">
<div class="h1">{title}</div>
<div class="sub">{subtitle}</div>
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def render(name, html, w=1160, h=1500):
    f = OUT / f"{name}.html"
    f.write_text(html, encoding="utf-8")
    png = OUT / f"{name}.png"
    subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--default-background-color=FFFFFFFF", "--virtual-time-budget=4000",
         "--force-device-scale-factor=2",
         f"--window-size={w},{h}", f"--screenshot={png}", f.as_uri()],
        capture_output=True, timeout=90)
    # 裁掉底部空白
    im = Image.open(png).convert("RGB")
    bbox = im.point(lambda p: 255 - p).getbbox()
    if bbox:
        im = im.crop((0, 0, im.width, min(im.height, bbox[3] + 26)))
        im.save(png)
    print(f"OK  {name}.png  {im.size[0]}x{im.size[1]}  {png.stat().st_size} bytes")


# ============================================================
# 图 1：四功能闭环
# ============================================================
LOOP_CSS = f"""
.bd{{border:1px solid {LINE};border-radius:14px;padding:20px 22px 16px;margin-top:22px;}}
.tag{{font-size:12.5px;color:{GRAY};letter-spacing:2px;margin-bottom:14px;}}
.grid{{display:grid;grid-template-columns:1fr 372px;gap:0 34px;}}
.step{{background:{CARD};border-radius:10px;padding:14px 18px 14px 20px;
      border-left:4px solid {DARK};position:relative;}}
.step h3{{font-size:16.5px;color:{DARK};font-weight:700;}}
.step p{{font-size:12.5px;color:{INK};line-height:1.72;margin-top:5px;}}
.arrow{{text-align:center;color:{LINE};font-size:15px;line-height:1;margin:9px 0;}}
.arrow span{{font-size:11.5px;color:{GRAY};margin-left:8px;letter-spacing:.2px;}}
.side{{display:flex;flex-direction:column;justify-content:space-between;gap:16px;}}
.mini{{background:#fff;border:1px solid {LINE};border-radius:10px;padding:15px 17px;}}
.mini h4{{font-size:14.5px;color:{DARK};font-weight:700;}}
.mini p{{font-size:12px;color:{INK};line-height:1.7;margin-top:5px;}}
.mini .ix{{font-size:12px;color:{MINT};font-weight:700;margin-right:6px;}}
.loop{{margin-top:14px;background:{CARD2};border-radius:9px;padding:11px 16px;
      font-size:12.5px;color:{GREEN};font-weight:700;text-align:center;}}
.hint{{margin-top:9px;font-size:11.5px;color:{GRAY};}}
.pill{{display:inline-block;background:#fff;border:1px solid {LINE};border-radius:20px;
      padding:2px 11px;font-size:11.5px;color:{MINT};margin-right:6px;}}
"""

LOOP_BODY = f"""
<div class="bd">
  <div class="tag">主 链 路</div>
  <div class="grid">
    <div>
      <div class="step">
        <h3>① 农户拍照上传</h3>
        <p>拍摄作物异常部位，选择作物（可自动推荐）<br>全程 3 步以内完成，零学习成本</p>
      </div>
      <div class="arrow">▼<span>进入图像识别</span></div>
      <div class="step">
        <h3>② AI 图像识别 · 置信度判定</h3>
        <p>高置信度：直接输出病虫害种类与诊断结论<br>低置信度：提示补拍关键部位，仍不达标转人工复核，绝不“硬出方案”</p>
      </div>
      <div class="arrow">▼<span>识别与检索结果统一进入方案匹配</span></div>
      <div class="step">
        <h3>③ 防治方案匹配</h3>
        <p>用什么药（有效成分与商品名）、用多少（亩用量/稀释倍数）<br>什么时候打、安全间隔期与注意事项；绿色防控优先</p>
      </div>
      <div class="arrow">▼</div>
      <div class="step">
        <h3>④ 执行与反馈</h3>
        <p>防治效果记录 → 样本回流 → 专家标注 → 模型持续优化</p>
      </div>
    </div>
    <div class="side">
      <div class="mini">
        <h4><span class="ix">补充入口</span>搜索查询</h4>
        <p>已知病虫害名称或症状关键词检索（支持模糊词、方言词映射），
           服务农资店店员与农技员的“查证”场景</p>
      </div>
      <div class="mini">
        <h4><span class="ix">前置引导</span>预防推送</h4>
        <p>地理定位 + 作物种植结构 + 物候期 → 当地当季高发病虫害预警，
           防治窗口期前 7–15 天提醒，变“被动求医”为“主动预防”</p>
      </div>
      <div class="mini">
        <h4><span class="ix">闭环关键字</span>自增强</h4>
        <p>使用越多 → 样本回流越多 → 模型越准 → 用户越多</p>
      </div>
    </div>
  </div>
  <div class="loop">识别结果 → 用药反馈 → 样本标注回流，闭环自增强</div>
</div>
"""

# ============================================================
# 图 2：技术路线总览
# ============================================================
TECH_CSS = f"""
.tier{{border-radius:12px;padding:15px 20px;margin-top:13px;}}
.tier .hd{{font-size:15.5px;font-weight:700;letter-spacing:.4px;}}
.tier .bd2{{font-size:12.5px;line-height:1.75;margin-top:6px;}}
.t1{{background:{DARK};}}
.t1 .hd{{color:#fff;}} .t1 .bd2{{color:#cfe0d5;}}
.t2{{background:{GREEN};}}
.t2 .hd{{color:#fff;}} .t2 .bd2{{color:#dcefdd;}}
.t3{{background:{CARD2};border:1px solid {LINE};}}
.t3 .hd{{color:{DARK};}} .t3 .bd2{{color:{INK};}}
.tvarrow{{text-align:center;color:{LINE};font-size:16px;line-height:1.4;margin:2px 0;}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px;}}
.panel{{border:1px solid {LINE};border-radius:12px;padding:14px 18px;background:#fff;}}
.panel h4{{font-size:14.5px;color:{DARK};font-weight:700;padding-bottom:9px;
         border-bottom:1px dashed {LINE};}}
.panel ul{{list-style:none;margin-top:9px;}}
.panel li{{font-size:12.5px;color:{INK};line-height:1.95;padding-left:15px;position:relative;}}
.panel li:before{{content:'';position:absolute;left:0;top:9.5px;width:5px;height:5px;
                border-radius:50%;background:{MINT};}}
.kv{{font-size:12.5px;color:{GRAY};margin-top:15px;line-height:1.85;}}
.kv b{{color:{GREEN};}}
.chain{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:10px;}}
.node{{background:{CARD};border-radius:8px;padding:8px 13px;font-size:12.5px;
      color:{DARK};font-weight:700;white-space:nowrap;}}
.node.alt{{background:#fff;border:1px solid {LINE};font-weight:600;color:{MINT};}}
.che{{color:{LINE};font-size:13px;}}
"""

TECH_BODY = f"""
<div class="tier t1">
  <div class="hd">端侧 · 网页平台（免安装、扫码即用）</div>
  <div class="bd2">拍照上传 → 图像预处理 → 轻量模型推理 ≤1 秒 · 包体增量 ≤5MB · 弱网可离线初判</div>
</div>
<div class="tvarrow">▼</div>
<div class="tier t2">
  <div class="hd">服务端 · 诊断与方案输出</div>
  <div class="bd2">识别服务 ｜ 防治方案引擎 ｜ 知识库服务 ｜ 预警推送服务 ｜ 人工复核队列</div>
</div>
<div class="tvarrow">▼</div>
<div class="tier t3">
  <div class="hd">数据层</div>
  <div class="bd2">病虫害影像样本库 ｜ 农药登记数据库 ｜ 防治知识库 ｜ 地理与物候库 ｜ 用户反馈样本库</div>
</div>

<div class="two">
  <div class="panel">
    <h4>AI 识别模型管线</h4>
    <ul>
      <li>OpenCV 预处理：颜色空间转换、光照校正、去噪、叶片与病斑分割</li>
      <li>轻量主干：MobileNetV3 / EfficientNet-Lite，YOLO-nano 辅助检测</li>
      <li>INT8 量化压缩 + 置信度双阈值判定</li>
      <li>训练数据：公开数据集 + 植保机构合作 + 试点众包回流标注</li>
    </ul>
  </div>
  <div class="panel">
    <h4>农业机械协同（空地一体）</h4>
    <ul>
      <li>无人机低空巡检，可见光 / 多光谱相机批量采集</li>
      <li>机载端 OpenCV 拼接、几何校正、光照归一化</li>
      <li>轻量模型批量识别 → 发病区域定位 → 变量施药处方图</li>
      <li>对接飞防组织，实现巡检与精准施药闭环</li>
    </ul>
  </div>
</div>

<div class="kv">
  <b>防治知识库</b>：中国农药信息网登记数据库、《农药管理条例》、全国农技中心年度防治技术方案（权威数据源）<br>
  <b>结构化口径</b>：作物 × 病虫害 → 推荐药剂 → 用法用量 → 安全间隔期 → 注意事项，初期 ≥400 条
</div>
<div class="chain">
  <span class="node">拍照</span><span class="che">→</span>
  <span class="node">OpenCV 预处理</span><span class="che">→</span>
  <span class="node">轻量模型推理</span><span class="che">→</span>
  <span class="node alt">置信度双阈值</span><span class="che">→</span>
  <span class="node">方案匹配</span><span class="che">→</span>
  <span class="node alt">人工复核兜底</span>
</div>
"""


def main():
    render("func_loop", SHELL.format(
        font=FONT, dark=DARK, gray=GRAY, line=LINE,
        extra=LOOP_CSS,
        title="拍照即诊断 · 诊断即给方案 —— 四功能闭环",
        subtitle="主链路 3 步以内完成；搜索查询与预防推送为补充入口，执行反馈回流构成自增强闭环",
        body=LOOP_BODY,
        foot="主链路（深色卡片）：拍照识别 → 防治建议；补充入口（浅色卡片）：搜索查询、预防推送。"
             "识别结果与检索、预警结果统一汇入防治方案匹配，用药反馈与样本回流再优化模型。"))

    render("tech_roadmap", SHELL.format(
        font=FONT, dark=DARK, gray=GRAY, line=LINE,
        extra=TECH_CSS,
        title="技术路线总览 —— 端云协同的轻量化诊断架构",
        subtitle="端侧推理 ≤1 秒｜包体增量 ≤5MB｜弱网可离线初判｜置信度双阈值兜底，低置信结果转人工复核",
        body=TECH_BODY,
        foot="总体架构与模型路线依据正文（三）技术路线；防治知识库数据源为官方登记与全国农技中心防治技术方案。"))


if __name__ == "__main__":
    main()
