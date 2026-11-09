# -*- coding: utf-8 -*-
"""生成商业计划书业务图表（ECharts Web 图）并用无头 Edge 渲染成 PNG。"""
import json
import subprocess
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
WEB = BASE / "figures" / "web"
WEB.mkdir(parents=True, exist_ok=True)
ECHARTS_JS = "../../node_modules/echarts/dist/echarts.min.js"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 品牌配色
GREEN, LGREEN, GOLD, BLUE, RED, GRAY, CYAN, ORANGE = (
    "#2e7d32", "#66bb6a", "#f9a825", "#1e88e5", "#e53935", "#90a4ae",
    "#26c6da", "#ff7043")
PALETTE = [GREEN, GOLD, BLUE, ORANGE, LGREEN, CYAN, RED, GRAY]

FONT = "Microsoft YaHei, 'PingFang SC', sans-serif"

BASE_STYLE = {
    "textStyle": {"fontFamily": FONT, "color": "#37474f"},
    "color": PALETTE,
}


def _t(option):
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="{ECHARTS_JS}"></script>
<style>html,body{{margin:0;padding:0;background:#ffffff;}} #chart{{width:100vw;height:100vh;}}</style>
</head><body><div id="chart"></div>
<script>
var ch = echarts.init(document.getElementById('chart'));
ch.setOption({json.dumps(option, ensure_ascii=False)});
</script></body></html>"""


def render(name, w, h, option):
    option = dict(BASE_STYLE, **option)
    html = WEB / f"{name}.html"
    html.write_text(_t(option), encoding="utf-8")
    png = WEB / f"{name}.png"
    out = str(png).replace("\\", "/")
    uri = html.as_uri()
    r = subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--default-background-color=FFFFFFFF", "--virtual-time-budget=4500",
         f"--window-size={w},{h}", f"--screenshot={out}", uri],
        capture_output=True, timeout=60)
    ok = png.exists() and png.stat().st_size > 2000
    print(("OK  " if ok else "FAIL") + f"  {name}.png  ({png.stat().st_size if png.exists() else 0} bytes)")
    return ok


# ------------------------------------------------------------
# 1. 市场规模与增速
# ------------------------------------------------------------
def market_size():
    years = ["2024", "2025", "2026", "2027", "2028"]
    mkt = [8500, 10000, 11500, 13000, 14800]
    grow = [17.6, 17.6, 15.0, 13.0, 13.8]
    opt = {
        "title": {"text": "中国智慧农业市场规模及增速", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["市场规模", "同比增速"], "top": 44},
        "grid": {"left": 60, "right": 60, "top": 80, "bottom": 40},
        "xAxis": {"type": "category", "data": years},
        "yAxis": [
            {"type": "value", "name": "亿元", "axisLabel": {"formatter": "{value}"}},
            {"type": "value", "name": "%", "max": 25, "axisLabel": {"formatter": "{value}%"},
             "splitLine": {"show": False}},
        ],
        "series": [
            {"name": "市场规模", "type": "bar", "data": mkt, "barWidth": "46%",
             "itemStyle": {"color": GREEN, "borderRadius": [6, 6, 0, 0]},
             "label": {"show": True, "position": "top", "formatter": "{c}"}},
            {"name": "同比增速", "type": "line", "yAxisIndex": 1, "data": grow,
             "symbolSize": 8, "lineStyle": {"width": 3, "color": GOLD},
             "itemStyle": {"color": GOLD},
             "label": {"show": True, "position": "top", "formatter": "{c}%"}},
        ],
    }
    render("market_size", 1000, 620, opt)


# ------------------------------------------------------------
# 2. 小农户痛点
# ------------------------------------------------------------
def painpoints():
    items = ["现有农业APP门槛过高、用不起来", "病虫害凭经验识别不准", "从未关注过农业信息渠道",
             "常错过防治最佳窗口期", "曾因用药错误造成损失"]
    vals = [73, 68, 66, 47, 41]
    opt = {
        "title": {"text": "小农户病虫害防治核心痛点（调研占比）", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "grid": {"left": 250, "right": 70, "top": 50, "bottom": 30},
        "xAxis": {"type": "value", "max": 100, "axisLabel": {"formatter": "{value}%"}},
        "yAxis": {"type": "category", "data": items, "axisLabel": {"fontSize": 13}},
        "series": [{
            "name": "占比", "type": "bar", "data": vals, "barWidth": "58%",
            "itemStyle": {"borderRadius": [0, 6, 6, 0],
                          "color": {"type": "linear", "x": 0, "y": 0, "x2": 1, "y2": 0,
                                    "colorStops": [{"offset": 0, "color": LGREEN},
                                                   {"offset": 1, "color": GREEN}]}},
            "label": {"show": True, "position": "right", "formatter": "{c}%", "fontSize": 13},
        }],
    }
    render("painpoints", 1000, 620, opt)


# ------------------------------------------------------------
# 3. 竞品雷达对比
# ------------------------------------------------------------
def competitive_radar():
    inds = [{"name": "识别精度", "max": 100}, {"name": "操作便捷性", "max": 100},
            {"name": "防治方案落地", "max": 100}, {"name": "本地化预警", "max": 100},
            {"name": "价格/使用门槛", "max": 100}]
    opt = {
        "title": {"text": "竞争格局雷达对比", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "legend": {"data": ["本项目", "传统农技服务", "现有农业APP"], "bottom": 10},
        "radar": {"indicator": inds, "radius": "62%", "center": ["50%", "54%"],
                  "axisName": {"fontSize": 13}},
        "series": [{
            "type": "radar",
            "data": [
                {"value": [92, 95, 90, 88, 85], "name": "本项目",
                 "areaStyle": {"color": "rgba(46,125,50,0.28)"},
                 "lineStyle": {"color": GREEN, "width": 3}, "itemStyle": {"color": GREEN}},
                {"value": [70, 40, 85, 60, 50], "name": "传统农技服务",
                 "areaStyle": {"color": "rgba(144,164,174,0.18)"},
                 "lineStyle": {"color": GRAY}, "itemStyle": {"color": GRAY}},
                {"value": [78, 55, 60, 45, 65], "name": "现有农业APP",
                 "areaStyle": {"color": "rgba(30,136,229,0.15)"},
                 "lineStyle": {"color": BLUE}, "itemStyle": {"color": BLUE}},
            ],
        }],
    }
    render("competitive_radar", 900, 620, opt)


# ------------------------------------------------------------
# 4. 目标用户画像（作物结构环形图）
# ------------------------------------------------------------
def user_profile():
    data = [{"name": "水稻", "value": 34}, {"name": "小麦", "value": 22},
            {"name": "玉米", "value": 18}, {"name": "果蔬", "value": 20},
            {"name": "其他", "value": 6}]
    opt = {
        "title": {"text": "目标用户作物结构", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c}%"},
        "legend": {"bottom": 10, "textStyle": {"fontSize": 13}},
        "series": [{
            "type": "pie", "radius": ["42%", "66%"], "center": ["50%", "52%"],
            "data": data,
            "label": {"formatter": "{b}\n{c}%", "fontSize": 12},
            "itemStyle": {"borderRadius": 6, "borderColor": "#fff", "borderWidth": 2},
            "emphasis": {"scaleSize": 6},
        }],
        "graphic": [{
            "type": "text", "left": "center", "top": "46%",
            "style": {"text": "小农户", "fontSize": 16, "fontWeight": "bold",
                      "fill": "#37474f", "textAlign": "center"},
        }],
    }
    render("user_profile", 900, 620, opt)


# ------------------------------------------------------------
# 5. 未来三年营收预测（堆叠柱 + 总额线）
# ------------------------------------------------------------
def revenue_forecast():
    years = ["第1年\n(2026)", "第2年\n(2027)", "第3年\n(2028)"]
    rev = {
        "农资渠道佣金": [2, 12, 55],
        "品牌精准推广": [3, 15, 45],
        "增值会员服务": [2, 8, 30],
        "政府项目采购": [5, 20, 50],
    }
    total = [12, 55, 180]
    opt = {
        "title": {"text": "未来三年营业收入预测（万元）", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 44},
        "grid": {"left": 60, "right": 60, "top": 80, "bottom": 40},
        "xAxis": {"type": "category", "data": years},
        "yAxis": {"type": "value", "name": "万元"},
        "series": [
            *[{"name": k, "type": "bar", "stack": "r", "data": v,
               "barWidth": "48%", "itemStyle": {"borderRadius": 0}}
              for k, v in rev.items()],
            {"name": "总营收", "type": "line", "data": total, "symbolSize": 10,
             "lineStyle": {"width": 3, "color": RED}, "itemStyle": {"color": RED},
             "label": {"show": True, "position": "top", "formatter": "{c}",
                       "fontSize": 13, "fontWeight": "bold"}},
        ],
    }
    render("revenue_forecast", 1000, 620, opt)


# ------------------------------------------------------------
# 6. 收入结构（玫瑰图，第3年）
# ------------------------------------------------------------
def revenue_structure():
    data = [{"name": "农资渠道佣金", "value": 55}, {"name": "品牌精准推广", "value": 45},
            {"name": "政府项目采购", "value": 50}, {"name": "增值会员服务", "value": 30}]
    opt = {
        "title": {"text": "第3年收入结构（万元）", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "item", "formatter": "{b}: {c}万元 ({d}%)"},
        "legend": {"bottom": 10, "textStyle": {"fontSize": 13}},
        "series": [{
            "type": "pie", "roseType": "radius", "radius": ["18%", "68%"],
            "center": ["50%", "52%"],
            "data": data,
            "label": {"formatter": "{b}\n{d}%", "fontSize": 12},
            "itemStyle": {"borderRadius": 6, "borderColor": "#fff", "borderWidth": 2},
        }],
    }
    render("revenue_structure", 900, 620, opt)


# ------------------------------------------------------------
# 7. 成本结构
# ------------------------------------------------------------
def cost_structure():
    data = [{"name": "技术研发", "value": 35}, {"name": "市场推广", "value": 30},
            {"name": "数据与运营", "value": 15}, {"name": "人力管理", "value": 12},
            {"name": "其他", "value": 8}]
    opt = {
        "title": {"text": "成本结构占比", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "item", "formatter": "{b}: {d}%"},
        "legend": {"orient": "vertical", "right": 30, "top": "middle",
                   "textStyle": {"fontSize": 13}},
        "series": [{
            "type": "pie", "radius": ["40%", "66%"], "center": ["42%", "52%"],
            "data": data,
            "label": {"formatter": "{d}%", "fontSize": 13, "fontWeight": "bold"},
            "itemStyle": {"borderRadius": 6, "borderColor": "#fff", "borderWidth": 2},
        }],
    }
    render("cost_structure", 900, 620, opt)


# ------------------------------------------------------------
# 8. 盈亏平衡（累计成本 vs 累计收入）
# ------------------------------------------------------------
def breakeven():
    m = np.arange(1, 37)
    # 累计成本：第 1/2/3 年合计 45 / 65 / 125 万元（累计 45 / 110 / 235）
    cum_cost = np.interp(m, [0, 12, 24, 36], [0, 45, 110, 235])
    # 累计收入：收入自第 6 个月起产生，第 1/2/3 年合计 12 / 55 / 180 万元（累计 12 / 67 / 247）
    cum_rev = np.interp(m, [0, 6, 12, 24, 36], [0, 0, 12, 67, 247])
    # 单月盈亏平衡：当月收入首次覆盖当月成本
    monthly_cost = np.diff(np.concatenate([[0.0], cum_cost]))
    monthly_rev = np.diff(np.concatenate([[0.0], cum_rev]))
    be_m = int(m[np.where(monthly_rev >= monthly_cost)[0][0]])
    # 累计盈亏平衡：累计收入曲线首次追上累计成本
    be_cum = int(m[np.where(cum_rev >= cum_cost)[0][0]])
    opt = {
        "title": {"text": "盈亏平衡分析（累计，万元）", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 44},
        "grid": {"left": 60, "right": 40, "top": 80, "bottom": 40},
        "xAxis": {"type": "category", "name": "月份",
                  "data": [str(i) for i in m]},
        "yAxis": {"type": "value", "name": "万元"},
        "series": [
            {"name": "累计成本", "type": "line", "data": [round(v, 1) for v in cum_cost],
             "lineStyle": {"width": 3, "color": RED}, "itemStyle": {"color": RED},
             "symbol": "none", "areaStyle": {"color": "rgba(229,57,53,0.06)"}},
            {"name": "累计收入", "type": "line", "data": [round(v, 1) for v in cum_rev],
             "lineStyle": {"width": 3, "color": GREEN}, "itemStyle": {"color": GREEN},
             "symbol": "none"},
        ],
        "graphic": [{
            "type": "text", "left": "center", "top": 130,
            "style": {"text": f"单月盈亏平衡 ≈ 第 {be_m} 个月\n累计盈亏平衡 ≈ 第 {be_cum} 个月",
                      "fontSize": 14, "fontWeight": "bold", "fill": "#e53935",
                      "lineHeight": 22, "textAlign": "center"},
        }],
    }
    render("breakeven", 1000, 620, opt)


# ------------------------------------------------------------
# 9. 用户增长
# ------------------------------------------------------------
def user_growth():
    m = np.arange(1, 37)
    anchors_m = np.array([0, 6, 12, 18, 24, 30, 36])
    anchors_r = np.array([0, 0.6, 2, 4, 8, 15, 25])
    reg = np.interp(m, anchors_m, anchors_r)          # 累计注册用户（万人）
    mau = reg * 0.35                                  # 月活
    opt = {
        "title": {"text": "用户增长预测（万人）", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 44},
        "grid": {"left": 60, "right": 40, "top": 80, "bottom": 40},
        "xAxis": {"type": "category", "name": "月份", "data": [str(i) for i in m]},
        "yAxis": {"type": "value", "name": "万人"},
        "series": [
            {"name": "累计注册用户", "type": "line", "data": [round(v, 1) for v in reg],
             "lineStyle": {"width": 3, "color": GREEN}, "itemStyle": {"color": GREEN},
             "symbol": "none", "areaStyle": {"color": "rgba(46,125,50,0.10)"}},
            {"name": "月活跃用户", "type": "line", "data": [round(v, 1) for v in mau],
             "lineStyle": {"width": 3, "color": GOLD}, "itemStyle": {"color": GOLD},
             "symbol": "none"},
        ],
    }
    render("user_growth", 1000, 620, opt)


# ------------------------------------------------------------
# 10. 融资资金用途
# ------------------------------------------------------------
def fund_usage():
    data = [{"name": "技术研发与模型迭代", "value": 40}, {"name": "市场推广与渠道", "value": 24},
            {"name": "数据采集与标注", "value": 16}, {"name": "团队与运营", "value": 12},
            {"name": "储备资金", "value": 8}]
    opt = {
        "title": {"text": "种子轮融资资金用途（%）", "left": "center", "top": 12,
                  "textStyle": {"fontSize": 18}},
        "tooltip": {"trigger": "item", "formatter": "{b}: {d}%"},
        "legend": {"bottom": 10, "textStyle": {"fontSize": 12}},
        "series": [{
            "type": "pie", "radius": ["38%", "64%"], "center": ["50%", "50%"],
            "data": data,
            "label": {"formatter": "{d}%", "fontSize": 13, "fontWeight": "bold"},
            "itemStyle": {"borderRadius": 6, "borderColor": "#fff", "borderWidth": 2},
        }],
    }
    render("fund_usage", 900, 620, opt)


if __name__ == "__main__":
    market_size()
    painpoints()
    competitive_radar()
    user_profile()
    revenue_forecast()
    revenue_structure()
    cost_structure()
    breakeven()
    user_growth()
    fund_usage()
    print("ALL WEB CHARTS DONE ->", WEB)
