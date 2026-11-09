# -*- coding: utf-8 -*-
"""
生成《业务场景信息系统建模实践》汇报 PPT。
可重复运行：改内容后重跑即可覆盖生成。

用法：  python build_ppt.py
输出：  业务场景信息系统建模实践_图书管理系统.pptx
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_kit import (  # noqa: E402
    DARK, GREEN, LIGHT, LIGHT2, LINE, GREY, WHITE, BODY,
    SW, SH, MARGIN, CW,
    tb, para, rich, text_at, card, bar, hline, picture, notes,
    blank, page, bullet_list, style_run,
)

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "业务场景信息系统建模实践_图书管理系统.pptx")

# ============ 只需要改这里 ============
MEMBERS = ["同学A", "同学B", "同学C", "同学D"]
DATE_TEXT = "2026 年 9 月"
# =====================================

A, B, C, D = MEMBERS
CAP = "图例：椭圆 = 用例　火柴人 = 参与者　连线 = 谁可以发起这个功能"


def main():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)

    # ==================== 01 封面 ====================
    s = blank(prs)
    bar(s, 0, 0, SW, 0.28, fill=DARK)
    bar(s, 0.85, 2.12, 0.062, 1.30, fill=GREEN)
    text_at(s, 1.18, 1.74, 9.5, 0.32, "《信息系统分析与设计》· 作业四",
            size=13, bold=True, color=GREEN)
    text_at(s, 1.15, 2.10, 10.5, 0.78, "业务场景信息系统建模实践",
            size=38, bold=True, color=DARK)
    text_at(s, 1.18, 3.02, 10.0, 0.45, "基于 UML 的图书管理系统建模",
            size=19, color=GREY)
    hline(s, 1.18, 3.92, 1.5, color=GREEN, h=0.035)
    text_at(s, 1.18, 4.26, 10.0, 0.34, "组员：" + "、".join(MEMBERS),
            size=15, color=BODY)
    text_at(s, 1.18, 4.72, 10.0, 0.30, DATE_TEXT, size=13, color=GREY)
    notes(s, "我们组这次汇报的是作业四，业务场景信息系统建模实践。"
             "选的案例是高校图书馆的图书管理系统。\n"
             "整个汇报分四块，由我们四个人分别来讲，大概十二分钟。")

    # ==================== 02 汇报框架 ====================
    s = page(prs, "CONTENTS", "这次汇报的内容与分工", page_no=2)
    items = [
        ("01", "背景与建模目标", "为什么选图书管理系统，这次要建出什么模型", A),
        ("02", "业务实体与用例图", "系统里有哪些角色，各自能干什么，一共 12 个用例", B),
        ("03", "借书流程的顺序图", "一次借书在系统内部经过哪几步，模块之间怎么调用", C),
        ("04", "类图与模型检查", "数据怎么组织，三张图对不对得上，以及 AI 使用说明", D),
    ]
    top = 1.70
    for no, title, desc, who in items:
        card(s, MARGIN, top, CW, 1.10, fill=LIGHT, radius=0.09)
        text_at(s, MARGIN + 0.32, top + 0.30, 0.85, 0.50, no,
                size=22, bold=True, color=GREEN, anchor=MSO_ANCHOR.MIDDLE)
        text_at(s, MARGIN + 1.30, top + 0.20, 7.6, 0.36, title,
                size=16, bold=True, color=DARK)
        text_at(s, MARGIN + 1.30, top + 0.60, 8.2, 0.32, desc,
                size=12.5, color=GREY)
        text_at(s, SW - MARGIN - 2.0, top + 0.40, 1.68, 0.30,
                "主讲 " + who, size=12, color=GREEN, align=PP_ALIGN.RIGHT)
        top += 1.27
    notes(s, "先说一下整体安排。我们把这个作业拆成四块：第一块交代背景和建模目标，"
             "第二块讲业务实体和用例图，第三块讲借书的顺序图，第四块讲类图，"
             "最后再对三张图做个交叉检查，把 AI 使用说明一起交代清楚。\n"
             "每块由一个人主讲，大概三分钟。下面先从背景开始。")

    # ==================== 03 项目背景 ====================
    s = page(prs, "PART 01 · 背景与建模目标", "为什么选图书管理系统", speaker=A, page_no=3)
    reasons = [
        ("业务边界干净", "主线就是学生借书、管理员管书，不牵扯采购、编目这些后台环节，"
                         "作业量能把它讲透。"),
        ("角色不重叠", "学生和图书管理员，能做的事几乎是两套，"
                       "建模时不容易把两边的功能搅在一起。"),
        ("数据有状态", "一本书从在架到借出再到归还，状态一直在变，"
                       "模型对不对，跑一遍流程就知道了。"),
    ]
    cw = (CW - 2 * 0.26) / 3
    for i, (t, d) in enumerate(reasons):
        l = MARGIN + i * (cw + 0.26)
        card(s, l, 1.70, cw, 2.52, fill=LIGHT, radius=0.07)
        bar(s, l + 0.32, 2.02, 0.52, 0.045, fill=GREEN)
        text_at(s, l + 0.32, 2.24, cw - 0.64, 0.36, t, size=16, bold=True, color=DARK)
        tf = tb(s, l + 0.32, 2.76, cw - 0.64, 1.2)
        para(tf, d, size=12.5, color=BODY, line=1.42, first=True)
    card(s, MARGIN, 4.56, CW, 1.52, fill=LIGHT2, radius=0.06)
    bar(s, MARGIN, 4.56, 0.068, 1.52, fill=GREEN)
    tf = tb(s, MARGIN + 0.48, 4.86, CW - 0.95, 1.0)
    para(tf, "我们四个平时都去图书馆借书，但对系统内部怎么运转其实没什么概念——"
             "屏幕上只弹一句「借阅成功」。这次作业就是把中间那几步拆开来看。",
         size=14, color=DARK, line=1.5, first=True)
    notes(s, "大家好，我们组选的案例是高校图书馆的借还书业务。\n"
             "选它有三个原因。第一，这个业务边界比较干净，主线就是学生借书、"
             "管理员管书，不像电商那样要牵扯支付、物流一大堆环节。\n"
             "第二，两类角色能做的事几乎不重叠，画用例图的时候不容易搅在一起。\n"
             "第三，图书是有状态的，在架还是借出，整个流程都在改这个状态，"
             "正好能反过来验证我们的模型对不对。\n"
             "另外说个很实际的出发点：我们平时借书，屏幕上只显示「借阅成功」，"
             "中间到底发生了什么完全看不到。这次作业就是想把中间那几步拆出来。")

    # ==================== 04 建模目标 ====================
    s = page(prs, "PART 01 · 背景与建模目标", "这次要建出什么", speaker=A, page_no=4)
    goals = [
        ("把角色和功能列全", "谁是参与者、各自能做什么，一条都不能漏"),
        ("把一条流程走通", "挑借书这条主线，把系统内部每一步的调用顺序捋清楚"),
        ("把数据落到类上", "哪些信息要存、由哪个类负责、谁改谁读"),
        ("让三张图对得上", "用例图里的功能，顺序图里找得到步骤，类图里找得到数据"),
    ]
    top = 1.72
    for i, (t, d) in enumerate(goals):
        card(s, MARGIN, top, CW, 1.00, fill=LIGHT, radius=0.08)
        text_at(s, MARGIN + 0.34, top + 0.24, 0.85, 0.52,
                "%02d" % (i + 1), size=20, bold=True, color=GREEN,
                anchor=MSO_ANCHOR.MIDDLE)
        text_at(s, MARGIN + 1.30, top + 0.18, 9.6, 0.34, t,
                size=15.5, bold=True, color=DARK)
        text_at(s, MARGIN + 1.30, top + 0.56, 9.8, 0.30, d, size=12.5, color=GREY)
        top += 1.17
    text_at(s, MARGIN, 6.52, CW, 0.30,
            "前三条对着作业要求 1 到 3，第四条是我们给自己加的检查。",
            size=13, bold=True, color=GREEN)
    notes(s, "基于这个选题，我们定了四个目标。\n"
             "前三个比较常规：把角色和用例列全、把借书这条流程走通、把数据落到类上，"
             "分别对应的就是作业要求里的参与者用例、实体提取和图例规范。\n"
             "第四个是我们自己加的——三张图要能互相印证。"
             "因为分开画三张图很容易出现「图里有、别的图里找不到」的元素，"
             "我们想让这三张图是同一个系统的三个侧面，不是三张互不相干的画。")

    # ==================== 05 建模方法 ====================
    s = page(prs, "PART 01 · 背景与建模目标", "为什么是 UML，为什么选这三张图",
             speaker=A, page_no=5)
    text_at(s, MARGIN, 1.68, CW, 0.32,
            "UML 是面向对象建模的通用语言，符号是标准化的，不用额外解释图例别人也看得懂。",
            size=13.5, color=BODY)

    colx = [MARGIN, MARGIN + 3.35, MARGIN + 8.75]
    colw = [3.35, 5.40, 3.02]
    heads = ["图", "回答的问题", "视角"]
    card(s, MARGIN, 2.28, CW, 0.42, fill=LIGHT2, radius=0.10)
    for x, w, h in zip(colx, colw, heads):
        text_at(s, x + 0.26, 2.35, w - 0.4, 0.28, h, size=12.5, bold=True, color=DARK)
    rows = [
        ("用例图", "系统为谁服务、提供哪些功能", "需求视角"),
        ("顺序图", "一条业务在系统内部怎么走", "动态视角"),
        ("类图", "系统里有哪些数据、谁负责", "静态视角"),
    ]
    top = 2.70
    for i, row in enumerate(rows):
        if i % 2 == 0:
            card(s, MARGIN, top, CW, 0.58, fill=LIGHT, radius=0.10)
        for x, w, cell in zip(colx, colw, row):
            bold = (cell == row[0])
            text_at(s, x + 0.26, top + 0.15, w - 0.4, 0.30, cell,
                    size=12.5, bold=bold, color=DARK if bold else BODY)
        top += 0.58

    card(s, MARGIN, 4.70, CW, 0.70, fill=LIGHT2, radius=0.08)
    text_at(s, MARGIN, 4.90, CW, 0.32, "用例图定范围，顺序图验流程，类图落数据。",
            size=17, bold=True, color=GREEN, align=PP_ALIGN.CENTER)

    card(s, MARGIN, 5.58, CW, 1.02, fill=LIGHT, radius=0.06)
    bar(s, MARGIN, 5.58, 0.068, 1.02, fill=GREEN)
    text_at(s, MARGIN + 0.42, 5.74, 11.0, 0.30,
            "顺序图为什么只画了借书这一条？", size=13, bold=True, color=DARK)
    text_at(s, MARGIN + 0.42, 6.08, 10.9, 0.32,
            "借书这条链上同时动了图书状态和借阅记录两份数据，还要先校验学生资格，"
            "是信息量最大的一段。把它走通，还书和续借就是同一套结构反着走一遍。",
            size=11.5, color=BODY)
    notes(s, "方法上我们选了 UML。理由很简单，它是标准，符号是约定俗成的，"
             "老师一看就懂，不用我们自己再造一套图例。\n"
             "三张图的分工是这样的：用例图从外面看系统，回答「为谁做什么」；"
             "顺序图看系统内部，回答「一次业务怎么走」；类图是静态的，回答「数据怎么组织」。\n"
             "一句话概括就是：用例图定范围，顺序图验流程，类图落数据。\n"
             "有同学可能会问，为什么顺序图只画了一条流程。我们的考虑是，"
             "借书是这条业务链上信息量最大的一段——它要校验学生资格，"
             "同时改图书状态和借阅记录两份数据。把这一条走通，"
             "还书和续借基本就是同一套结构反过来走一遍。")

    # ==================== 06 实体识别 ====================
    s = page(prs, "PART 02 · 业务实体与用例图", "从业务里提取类与对象",
             speaker=B, page_no=6)
    card(s, MARGIN, 1.66, CW, 0.62, fill=LIGHT2, radius=0.08)
    text_at(s, MARGIN + 0.34, 1.84, CW - 0.7, 0.32,
            "做法很直接：先把业务描述里的名词全圈出来，再逐个问一句"
            "「这东西需要单独存吗」，留下来的就是候选类。",
            size=12.5, color=BODY)

    colx = [MARGIN, MARGIN + 3.0, MARGIN + 5.5]
    colw = [3.0, 2.5, CW - 5.5]
    for x, w, h in zip(colx, colw, ["候选名词", "怎么处理", "理由"]):
        text_at(s, x + 0.26, 2.46, w - 0.4, 0.28, h, size=12, bold=True, color=GREY)

    rows = [
        ("学生、图书管理员", "保留为类", "有独立身份，也有自己的操作", DARK),
        ("图书", "保留为类", "有状态（在架 / 借出），要被反复查询", DARK),
        ("借阅记录", "保留为类", "借一次生成一条，要留痕、要统计", DARK),
        ("罚金", "并入借阅记录", "只在逾期时才算出来的一个数，离开记录没有意义", GREY),
        ("书架、借书证", "舍去", "位置信息本系统用不上；学号已经能唯一标识学生", GREY),
    ]
    top = 2.80
    for i, (name, act, why, col) in enumerate(rows):
        if i % 2 == 0:
            card(s, MARGIN, top, CW, 0.60, fill=LIGHT, radius=0.10)
        text_at(s, colx[0] + 0.26, top + 0.16, colw[0] - 0.4, 0.30, name,
                size=12.5, bold=True, color=col)
        text_at(s, colx[1] + 0.26, top + 0.16, colw[1] - 0.4, 0.30, act,
                size=12.5, color=GREEN if act != "舍去" else GREY)
        text_at(s, colx[2] + 0.26, top + 0.16, colw[2] - 0.5, 0.30, why,
                size=12, color=BODY)
        top += 0.60
    text_at(s, MARGIN, 6.02, CW, 0.32,
            "最后留下 4 个类：学生、图书、图书管理员、借阅记录。",
            size=14, bold=True, color=GREEN)

    card(s, MARGIN, 6.48, CW, 0.52, fill=LIGHT2, radius=0.10)
    text_at(s, MARGIN + 0.34, 6.61, CW - 0.7, 0.30,
            "另外「还书」「续借」这些是动作，不是名词，它们会变成类上的方法，不单独建类。",
            size=11.5, color=GREY)
    notes(s, "这部分讲我们怎么从业务里把类挑出来。\n"
             "做法其实挺笨的：先把业务描述里出现的名词全圈出来，学生、管理员、图书、"
             "借阅记录、罚金、书架、借书证……然后一个一个问，这个东西需要单独存吗。\n"
             "留下三个是比较好判断的：学生和管理员有独立身份，图书有在架借出这个状态，"
             "借阅记录要留痕、要统计。\n"
             "有两个是纠结过的。罚金，一开始我们想单独建一个类，后来发现它只在逾期的时候"
             "才算得出来，离开借阅记录就没有意义，所以并进借阅记录了。"
             "书架和借书证就直接舍掉了，位置信息这个系统不关心，学号已经能唯一标识一个学生。\n"
             "还有一个要注意的，还书、续借这些是动作不是名词，它们最后会变成类上的方法，"
             "不单独建类。")

    # ==================== 07 用例图 ====================
    s = page(prs, "PART 02 · 业务实体与用例图", "系统用例图", speaker=B,
             subtitle="左边是学生，右边是图书管理员，中间 12 个用例覆盖了两类角色的全部操作。",
             page_no=7)
    picture(s, os.path.join(FIG, "usecase.png"), 0.85, 2.00, h=4.85)

    rx, rw = 6.68, SW - 6.68 - MARGIN
    card(s, rx, 2.00, rw, 1.32, fill=LIGHT, radius=0.07)
    text_at(s, rx + 0.30, 2.18, rw - 0.6, 0.30, "学生 · 6 个用例",
            size=14, bold=True, color=DARK)
    tf = tb(s, rx + 0.30, 2.56, rw - 0.6, 0.64)
    para(tf, "登录、查询图书信息、借阅图书、归还图书", size=12, color=BODY,
         line=1.3, first=True)
    para(tf, "查看个人借阅记录、图书续借", size=12, color=BODY, line=1.3)

    card(s, rx, 3.46, rw, 1.32, fill=LIGHT, radius=0.07)
    text_at(s, rx + 0.30, 3.64, rw - 0.6, 0.30, "图书管理员 · 6 个用例",
            size=14, bold=True, color=DARK)
    tf = tb(s, rx + 0.30, 4.02, rw - 0.6, 0.64)
    para(tf, "登录、图书入库、图书信息修改 / 删除、读者信息管理", size=12,
         color=BODY, line=1.3, first=True)
    para(tf, "借阅记录查询、逾期图书处理", size=12, color=BODY, line=1.3)

    card(s, rx, 4.92, rw, 1.93, fill=LIGHT2, radius=0.07)
    text_at(s, rx + 0.30, 5.08, rw - 0.6, 0.30, "怎么看这张图", size=14,
            bold=True, color=DARK)
    tf = tb(s, rx + 0.30, 5.46, rw - 0.6, 1.3)
    bullet_list(tf, [
        "椭圆是用例，代表系统对外提供的一个完整功能",
        "火柴人是参与者，都在系统外部",
        "两个参与者各连各的用例，中间没有交叉，权限不重叠",
    ], size=11.5, gap=7, line=1.3)
    notes(s, "这是我们最终的用例图。\n"
             "左边是学生，六个用例：登录、查书、借书、还书、看自己的借阅记录、续借。\n"
             "右边是图书管理员，也是六个：登录、图书入库、图书信息修改删除、"
             "读者信息管理、借阅记录查询、逾期处理。\n"
             "大家可以注意一下，两个参与者各连各的用例，中间没有交叉线。"
             "因为我们梳理下来，这两类角色的权限确实不重叠——"
             "学生做的六件事管理员不做，管理员做的六件事学生不做。\n"
             "顺便说一下符号：椭圆是用例，火柴人是参与者，都在系统外面，"
             "连线表示这个人可以发起这个功能。")

    # ==================== 08 参与者说明 ====================
    s = page(prs, "PART 02 · 业务实体与用例图", "两类参与者", speaker=B, page_no=8)
    cw = (CW - 0.36) / 2
    blocks = [
        ("学生", "系统的使用者，图书馆服务的对象",
         [("能做的：", "查书、借书、还书、续借、查看自己的借阅记录"),
          ("看不到的：", "别人的借阅情况——只能操作自己的数据")]),
        ("图书管理员", "系统的维护者，管图书和读者两边的数据",
         [("能做的：", "图书入库、修改或删除图书、管理读者账号、查借阅记录、处理逾期"),
          ("边界：", "能改图书和读者数据，但不能替学生发起借还")]),
    ]
    for i, (name, role, pts) in enumerate(blocks):
        l = MARGIN + i * (cw + 0.36)
        card(s, l, 1.70, cw, 3.30, fill=LIGHT, radius=0.06)
        bar(s, l, 1.70, cw, 0.075, fill=GREEN)
        text_at(s, l + 0.40, 2.00, cw - 0.8, 0.40, name,
                size=19, bold=True, color=DARK)
        text_at(s, l + 0.40, 2.52, cw - 0.8, 0.30, role, size=12.5, color=GREY)
        hline(s, l + 0.40, 2.94, cw - 0.8)
        tf = tb(s, l + 0.40, 3.14, cw - 0.8, 1.7)
        bullet_list(tf, pts, size=12.5, gap=12, line=1.35)

    card(s, MARGIN, 5.32, CW, 1.32, fill=LIGHT2, radius=0.06)
    bar(s, MARGIN, 5.32, 0.068, 1.32, fill=GREEN)
    text_at(s, MARGIN + 0.46, 5.52, 11.0, 0.30,
            "两个登录用例为什么分开画？", size=13.5, bold=True, color=DARK)
    text_at(s, MARGIN + 0.46, 5.90, 10.9, 0.60,
            "学生和管理员走的账号表不一样，进去之后的权限也不一样。"
            "合并成一个「登录」，界面、校验、跳转这三个地方的差别就全都看不出来了，"
            "所以我们在图上分开处理。",
            size=12, color=BODY)
    notes(s, "这张图里的两类参与者，我们分开说一下。\n"
             "学生是系统的使用者，也就是图书馆服务的对象。能做的事是查书、借书、还书、"
             "续借、看自己的记录。这里有个边界要说清楚：学生只能操作自己的数据，"
             "看不到别人的借阅情况。\n"
             "图书管理员是系统的维护者，管的是图书和读者两边的数据，"
             "能入库新书、改图书信息、管读者账号、查所有人的借阅记录、处理逾期。"
             "管理员权限比学生高，但有一点——不能替学生发起借还，"
             "借还这个动作必须是学生本人做的。\n"
             "另外有人问过我们，为什么登录画了两个用例。因为学生和管理员走的账号表不一样，"
             "进去之后的权限也不一样，合并成一个会把差别抹掉。")

    # ==================== 09 用例一览 ====================
    s = page(prs, "PART 02 · 业务实体与用例图", "12 个用例一览", speaker=B,
             subtitle="每个用例都是系统对外提供的一个完整功能，下面是对应的参与者和使用说明。",
             page_no=9)
    data = [
        ("学生", [
            ("用户登录", "用学号加密码进入学生端"),
            ("查询图书信息", "按书名、作者或 ISBN 查图书状态"),
            ("借阅图书", "对状态为「在架」的图书发起借阅"),
            ("归还图书", "归还后图书状态回到「在架」"),
            ("查看个人借阅记录", "只看自己的，含应还日期和是否逾期"),
            ("图书续借", "没有逾期时可以延长应还日期"),
        ]),
        ("图书管理员", [
            ("管理员登录", "用员工号进入管理端"),
            ("图书入库", "新增图书，并写入馆藏状态"),
            ("图书信息修改 / 删除", "改书名、出版社等信息，或下架"),
            ("读者信息管理", "新增、修改学生账号"),
            ("借阅记录查询", "可以查任意学生的借阅情况"),
            ("逾期图书处理", "登记罚金、处理逾期图书"),
        ]),
    ]
    cw = (CW - 0.36) / 2
    for i, (group, rows) in enumerate(data):
        l = MARGIN + i * (cw + 0.36)
        text_at(s, l, 2.02, cw, 0.30, group, size=14, bold=True, color=GREEN)
        top = 2.38
        for j, (name, desc) in enumerate(rows):
            if j % 2 == 0:
                card(s, l, top, cw, 0.50, fill=LIGHT, radius=0.12)
            text_at(s, l + 0.24, top + 0.13, 1.85, 0.26, name,
                    size=11.5, bold=True, color=DARK)
            text_at(s, l + 2.18, top + 0.13, cw - 2.42, 0.26, desc,
                    size=11, color=BODY)
            top += 0.50

    card(s, MARGIN, 5.62, CW, 1.12, fill=LIGHT2, radius=0.06)
    bar(s, MARGIN, 5.62, 0.068, 1.12, fill=GREEN)
    text_at(s, MARGIN + 0.46, 5.78, 11.0, 0.30,
            "关于符号和关系", size=13.5, bold=True, color=DARK)
    text_at(s, MARGIN + 0.46, 6.14, 10.9, 0.46,
            "本图没有用 include / extend 关系。登录虽然是每个操作的前置，"
            "但它是独立入口，不是被别的用例调用的步骤；其余用例之间也没有真正复用的公共片段，"
            "强行抽取反而会把业务拆碎。",
            size=11.5, color=BODY)
    notes(s, "这页把 12 个用例一次列清楚，左边是学生的，右边是管理员的，"
             "每条都写了它具体干什么。\n"
             "重点讲一下最后一栏。老师可能会注意到，我们这张图上没有用 include 和 extend 关系。"
             "我们是这么想的：登录虽然每个操作之前都要做，但它是独立入口，"
             "不是被别的用例调用出来的步骤，所以我们按独立用例处理。"
             "其余的用例之间，我们也检查了一遍，没有找到真正被复用的公共片段。\n"
             "与其硬抽一个出来凑规范，不如保持平铺，这样业务反而更清楚。")

    # ==================== 10 顺序图 ====================
    s = page(prs, "PART 03 · 借书流程的顺序图", "借书流程顺序图", speaker=C,
             subtitle="横轴是参与这次交互的 5 个对象，纵轴是时间顺序。实线箭头是消息，虚线是对象的生命线。",
             page_no=10)
    picture(s, os.path.join(FIG, "sequence.png"), 2.19, 2.02, h=4.90)
    notes(s, "接下来我讲顺序图。\n"
             "我们画的是借书这个流程。横着看是五个对象：学生、图书借阅界面、"
             "图书业务模块、图书数据、借阅记录数据。竖着看是时间，从上往下走。\n"
             "中间这些虚线是对象的生命线，表示这个对象在这段时间里一直存在；"
             "箭头是消息，从一个对象发给另一个对象。\n"
             "整张图一共 8 步，下一页我们拆开讲。")

    # ==================== 11 八步拆解 ====================
    s = page(prs, "PART 03 · 借书流程的顺序图", "一次借书，系统内部发生了什么",
             speaker=C, page_no=11)
    stages = [
        ("发起", ["学生在借阅界面提交借书请求，带上学号 studentId 和图书 ISBN"], 0.78),
        ("校验", ["界面把请求转给图书业务模块，先判断这个学生有没有借书资格",
                  "资格通过，业务模块向图书数据查询这本书的状态",
                  "图书数据返回「可借」或「已借出」"], 1.38),
        ("写数据", ["确认可借，业务模块向借阅记录数据新增一条借阅记录",
                    "业务模块把这本书的状态更新为「已借出」",
                    ("这两步必须同成功或同失败，", "我们按放在同一个事务里处理。")], 1.38),
        ("返回", ["业务模块返回「借书成功」",
                  "界面提示成功，并显示应还日期"], 1.10),
    ]
    top = 1.68
    for i, (name, steps, h) in enumerate(stages):
        card(s, MARGIN, top, CW, h, fill=LIGHT if i % 2 == 0 else LIGHT2, radius=0.07)
        text_at(s, MARGIN + 0.36, top + 0.22, 1.35, 0.30, name,
                size=14, bold=True, color=GREEN)
        tf = tb(s, MARGIN + 1.85, top + 0.20, CW - 2.3, h - 0.34)
        bullet_list(tf, steps, size=12, gap=8, line=1.32)
        top += h + 0.13
    notes(s, "我们把借书拆成了四个阶段。\n"
             "第一步是发起。学生在界面上点借书，请求里带两个东西：学号，"
             "用来确认是谁；ISBN，用来确认借哪本书。\n"
             "然后是校验，这是最要紧的一段。界面自己不判断，它把请求转给业务模块。"
             "业务模块先查这个学生有没有借书资格——有没有超期没还的，有没有借满。"
             "资格过了，再去查这本书的状态，图书数据返回可借还是已借出。\n"
             "第三步写数据。这里注意，是两次写：先新增一条借阅记录，"
             "再把图书状态改成已借出。这两步必须同成功或者同失败，"
             "不然后面就会出现「有记录但书还在架上」这种脏数据，我们按放在一个事务里处理。\n"
             "最后返回结果，界面显示借阅成功和应还日期。")

    # ==================== 12 顺序图的设计考虑 ====================
    s = page(prs, "PART 03 · 借书流程的顺序图", "这张图里几个值得说的点",
             speaker=C, page_no=12)
    points = [
        ("分了四层", "界面只管收集输入和显示结果，判断逻辑全在业务模块，数据层只做存取。"
                     "以后换成手机端还是网页端，中间这两层不用动。"),
        ("校验在前，写库在后", "先查资格、再查图书状态，都过了才写借阅记录。"
                               "这样不会出现「记录写了，但书其实已经被别人借走」的情况。"),
        ("借书要动两份数据", "新增一条借阅记录，同时把图书状态改成已借出。"
                             "两份都要维护，所以后面的类图里它们是两个独立的类，不是一个。"),
        ("异常分支没画进图里", "「资格校验不通过」和「图书已借出」这两条分支在图上省略了，"
                               "只在文字里说明——都画上去图会太乱，反而看不清主流程。"),
    ]
    top = 1.72
    for i, (t, d) in enumerate(points):
        card(s, MARGIN, top, CW, 1.16, fill=LIGHT, radius=0.07)
        text_at(s, MARGIN + 0.36, top + 0.24, 0.62, 0.34,
                "%02d" % (i + 1), size=15, bold=True, color=GREEN)
        text_at(s, MARGIN + 1.10, top + 0.20, 9.9, 0.32, t,
                size=14.5, bold=True, color=DARK)
        text_at(s, MARGIN + 1.10, top + 0.60, 10.2, 0.48, d,
                size=12, color=BODY)
        top += 1.29
    notes(s, "这张图里我们想重点说四个地方。\n"
             "第一，整个系统分了四层：界面、业务、数据。界面只负责收集输入和显示结果，"
             "所有判断都在业务模块里，数据层只做存取。这样做的好处是，"
             "以后不管是做手机端还是网页端，中间的业务和数据这两层不用改。\n"
             "第二，校验在前，写库在后。先把资格和图书状态都查一遍，"
             "都通过了才写借阅记录。这样不会出现「记录写了，但书其实已经被别人借走」的情况。\n"
             "第三，借一次书要动两份数据：新增一条借阅记录，同时改图书状态。"
             "这也是为什么在后面的类图里，借阅记录和图书是两个独立的类。\n"
             "第四，异常分支我们没有画进图里。资格不通过、图书已借出这两条分支，"
             "如果都画上去图会很乱，所以省略了，只在文字里说明。")

    # ==================== 13 类图 ====================
    s = page(prs, "PART 04 · 类图与模型检查", "系统类图", speaker=D,
             subtitle="每个方框分三格：类名、属性、方法。线上的「1」和「0..*」表示两边数量上的对应关系。",
             page_no=13)
    picture(s, os.path.join(FIG, "classdiagram.png"), 2.24, 2.02, h=4.90)
    notes(s, "最后一块，类图。\n"
             "这张图上一共四个类。每个方框分三格：最上面是类名，中间是属性，"
             "下面是这个类能做的事，也就是方法。\n"
             "方框之间连的线上有数字，「1」和「0..*」，表示两边在数量上怎么对应。\n"
             "接下来两页我分别讲类的内部和类之间的关系。")

    # ==================== 14 四个类 ====================
    s = page(prs, "PART 04 · 类图与模型检查", "四个类分别管什么", speaker=D, page_no=14)
    cells = [
        ("学生", "学号 · 姓名 · 院系 · 当前已借图书数量",
         "「当前已借数量」是借书资格校验要用的。每次都去数据库数一遍记录太慢，"
         "直接记在对象上。"),
        ("图书", "图书编号 · 书名 · 作者 · 出版社 · 馆藏状态",
         "馆藏状态只有两个值：在架、已借出。整条借还流程改的都是这个字段。"),
        ("图书管理员", "管理员工号 · 姓名 · 权限等级",
         "方法：登录、新增图书、修改图书信息、管理读者账号、处理逾期。"),
        ("借阅记录", "记录编号 · 借阅日期 · 应还日期 · 实际归还日期 · 是否逾期",
         "借一次生成一条。「是否逾期」其实能用日期算出来，但存成字段查询更快，"
         "算是一个用空间换时间的取舍。"),
    ]
    cw = (CW - 0.32) / 2
    ch = 2.24
    for i, (name, attrs, desc) in enumerate(cells):
        l = MARGIN + (i % 2) * (cw + 0.32)
        top = 1.70 + (i // 2) * (ch + 0.26)
        card(s, l, top, cw, ch, fill=LIGHT, radius=0.07)
        bar(s, l, top, 0.062, ch, fill=GREEN)
        text_at(s, l + 0.34, top + 0.24, cw - 0.7, 0.34, name,
                size=16.5, bold=True, color=DARK)
        text_at(s, l + 0.34, top + 0.68, cw - 0.7, 0.56, attrs,
                size=12, color=GREEN, line=1.32)
        hline(s, l + 0.34, top + 1.32, cw - 0.7)
        text_at(s, l + 0.34, top + 1.48, cw - 0.7, 0.66, desc,
                size=11.5, color=BODY, line=1.34)
    notes(s, "这四个类，我一个个说。\n"
             "学生类，除了学号、姓名、院系，我们额外加了一个「当前已借图书数量」。"
             "因为借书资格校验的时候要判断他有没有借满，如果每次都去数据库把记录数一遍会很慢，"
             "所以我们把它直接记在对象上。\n"
             "图书类，关键属性是馆藏状态，它只有两个值：在架、已借出。"
             "整条借还流程改的都是这一个字段。\n"
             "图书管理员类，除了工号、姓名、权限等级，方法就是入库、改图书信息、"
             "管读者账号、处理逾期这几件事。\n"
             "借阅记录类，借一次生成一条记录。这里有一个我们要主动交代的取舍："
             "「是否逾期」这个属性，其实是能用应还日期和当前日期算出来的，"
             "严格说它冗余了。但每次查询都要算一遍开销大，我们把它存成字段，"
             "算是用空间换时间。")

    # ==================== 15 类间关系 ====================
    s = page(prs, "PART 04 · 类图与模型检查", "类与类之间怎么连", speaker=D, page_no=15)
    rels = [
        ("学生", "1", "0..*", "借阅记录",
         "一个学生可以有很多条借阅记录，一条记录只属于一个学生。新注册的学生还没借过书，所以是 0..*。"),
        ("图书", "1", "0..*", "借阅记录",
         "一本书会被反复借，每借一次生成一条记录。新入库的书还没被借过，同样是 0..*。"),
        ("图书管理员", "1", "0..*", "借阅记录",
         "管理员处理逾期、登记罚金的时候要操作借阅记录。"),
    ]
    top = 1.70
    for a, m1, m2, b, desc in rels:
        card(s, MARGIN, top, CW, 1.04, fill=LIGHT, radius=0.08)
        text_at(s, MARGIN + 0.40, top + 0.34, 1.7, 0.34, a,
                size=14.5, bold=True, color=DARK)
        text_at(s, MARGIN + 2.18, top + 0.34, 0.7, 0.34, m1,
                size=13, bold=True, color=GREEN)
        hline(s, MARGIN + 2.92, top + 0.50, 1.5, color=GREY, h=0.014)
        text_at(s, MARGIN + 4.46, top + 0.34, 0.9, 0.34, m2,
                size=13, bold=True, color=GREEN)
        text_at(s, MARGIN + 5.42, top + 0.34, 1.9, 0.34, b,
                size=14.5, bold=True, color=DARK)
        text_at(s, MARGIN + 0.40, top + 0.68, CW - 0.8, 0.28, desc,
                size=11.5, color=BODY)
        top += 1.19

    cw = (CW - 0.32) / 2
    card(s, MARGIN, 5.30, cw, 1.42, fill=LIGHT2, radius=0.06)
    bar(s, MARGIN, 5.30, 0.068, 1.42, fill=GREEN)
    text_at(s, MARGIN + 0.42, 5.47, cw - 0.8, 0.30,
            "为什么用关联，不用组合？", size=13, bold=True, color=DARK)
    text_at(s, MARGIN + 0.42, 5.82, cw - 0.84, 0.76,
            "借阅记录不属于学生本人——学生毕业离校之后，记录还要留在馆里做统计。"
            "所以这三条都是普通关联，不是组合。",
            size=11.5, color=BODY, line=1.36)

    l2 = MARGIN + cw + 0.32
    card(s, l2, 5.30, cw, 1.42, fill=LIGHT2, radius=0.06)
    bar(s, l2, 5.30, 0.068, 1.42, fill=GREY)
    text_at(s, l2 + 0.42, 5.47, cw - 0.8, 0.30,
            "一处可以改进的地方", size=13, bold=True, color=DARK)
    text_at(s, l2 + 0.42, 5.82, cw - 0.84, 0.76,
            "管理员和借阅记录这条关联偏弱，图上没体现「这条记录是哪个管理员办的」。"
            "要把责任落到人，可以在借阅记录里再加一个「经办人」属性。",
            size=11.5, color=BODY, line=1.36)
    notes(s, "类之间的关系，一共三条，都是 1 对 0..*。\n"
             "学生和借阅记录：一个学生可以有很多条借阅记录，一条记录只属于一个学生。"
             "这里标 0..* 是因为新注册的学生还没借过书，记录数可以是零。\n"
             "图书和借阅记录：一本书会被反复借，每借一次生成一条。"
             "新入库的书还没被借过，也是 0..*。\n"
             "第三条是管理员和借阅记录，因为处理逾期、登记罚金的时候要操作记录。\n"
             "有同学可能会问为什么不用组合关系。因为借阅记录不属于学生本人——"
             "学生毕业离校以后，这条记录还要留在馆里做统计，不能跟着学生一起消失，"
             "所以我们用的是普通关联。\n"
             "另外我们自己复盘的时候发现一个可以改进的点：管理员和借阅记录这条关联其实偏弱，"
             "图上没有体现这条记录是哪个管理员办的。如果要把责任落到人，"
             "可以在借阅记录里加一个经办人属性。")

    # ==================== 16 一致性检查 ====================
    s = page(prs, "PART 04 · 类图与模型检查", "三张图对得上吗", speaker=D,
             subtitle="这是我们给自己加的检查：用例图里的每个功能，能不能在另外两张图里找到落点。",
             page_no=16)
    heads = ["检查项", "用例图", "顺序图", "类图"]
    colw = [2.55, 2.95, 2.95, CW - 8.45]
    colx = [MARGIN]
    for w in colw[:-1]:
        colx.append(colx[-1] + w)
    card(s, MARGIN, 2.02, CW, 0.42, fill=LIGHT2, radius=0.10)
    for x, w, h in zip(colx, colw, heads):
        text_at(s, x + 0.24, 2.10, w - 0.4, 0.28, h,
                size=12, bold=True, color=DARK)
    rows = [
        ("借阅图书", "学生 → 借阅图书", "第 1 - 8 步完整流程", "新增借阅记录、图书状态改为已借出"),
        ("查询图书信息", "学生 → 查询图书信息", "第 3 - 4 步", "图书.查询图书状态()"),
        ("查看个人借阅记录", "学生 → 查看个人借阅记录", "未涉及", "学生.查询借阅记录(): List"),
        ("逾期图书处理", "管理员 → 逾期图书处理", "未涉及", "借阅记录.计算逾期罚金()"),
    ]
    top = 2.44
    for i, row in enumerate(rows):
        if i % 2 == 0:
            card(s, MARGIN, top, CW, 0.60, fill=LIGHT, radius=0.10)
        for x, w, cell in zip(colx, colw, row):
            bold = (cell == row[0])
            text_at(s, x + 0.24, top + 0.17, w - 0.42, 0.28, cell,
                    size=11.5, bold=bold, color=DARK if bold else BODY)
        top += 0.60

    card(s, MARGIN, 4.94, CW, 0.78, fill=LIGHT2, radius=0.08)
    text_at(s, MARGIN, 5.12, CW, 0.32,
            "用例图里的功能，在类图里都能找到属性或方法支撑；顺序图里的每个对象，都是类图里的一个类。",
            size=14, bold=True, color=GREEN, align=PP_ALIGN.CENTER)

    card(s, MARGIN, 5.92, CW, 0.92, fill=LIGHT, radius=0.06)
    bar(s, MARGIN, 5.92, 0.068, 0.92, fill=GREY)
    text_at(s, MARGIN + 0.42, 6.06, 11.0, 0.30,
            "有一处对不上，我们说明一下", size=13, bold=True, color=DARK)
    text_at(s, MARGIN + 0.42, 6.38, 10.9, 0.34,
            "顺序图里的「图书借阅界面」在类图里没有对应的类。这不是漏了——"
            "我们只建了业务领域的类，界面属于表示层，不在这次的建模范围里。",
            size=11.5, color=BODY)
    notes(s, "最后这页是我们给自己做的交叉检查。\n"
             "横着看每一行是一个功能，纵着看是三张图。比如借阅图书，用例图里是学生发起，"
             "顺序图里对应完整的 1 到 8 步，类图里对应新增借阅记录、改图书状态这两个动作。\n"
             "检查下来的结论是：用例图里的功能，在类图里都能找到属性或方法支撑；"
             "顺序图里的每一个对象，都能在类图里找到对应的类。\n"
             "不过我们确实发现一处对不上，要主动说明：顺序图里的「图书借阅界面」，"
             "在类图里没有对应的类。这不是漏掉了——我们这次只建业务领域的类，"
             "界面属于表示层，不在建模范围里。这个边界我们是有意识划的。")

    # ==================== 17 AI 使用说明与修改记录 ====================
    s = page(prs, "PART 04 · 类图与模型检查", "AI 使用说明与修改记录", speaker=D,
             subtitle="按作业要求附上，说明哪些环节用了 AI 辅助、哪些是我们自己做的。",
             page_no=17)
    cw = (CW - 0.36) / 2
    card(s, MARGIN, 1.98, cw, 4.92, fill=LIGHT, radius=0.06)
    bar(s, MARGIN, 1.98, cw, 0.068, fill=GREEN)
    text_at(s, MARGIN + 0.38, 2.18, cw - 0.76, 0.32, "AI 使用说明",
            size=16, bold=True, color=DARK)
    hline(s, MARGIN + 0.38, 2.58, cw - 0.76)
    tf = tb(s, MARGIN + 0.38, 2.72, cw - 0.76, 3.95)
    groups = [
        ("用在哪", [
            "梳理业务流程时，让 AI 列候选的参与者、用例和名词清单，我们再逐个筛",
            "核对用例图的符号用法是否符合 UML 规范",
            "汇报文字和说明文案的润色",
        ]),
        ("没用在", [
            "三张图全部由我们自己在 ProcessOn 上绘制",
            "类里的属性和方法对着业务一条条确定，没有让 AI 直接生成",
        ]),
        ("讨论后改掉的", [
            "AI 建议给「罚金」单独建类，我们认为它依附于借阅记录，合并了",
            "AI 建议用 include 抽公共步骤，我们判断用例之间没有真实复用，保留平铺",
        ]),
    ]
    first = True
    for gi, (gname, items) in enumerate(groups):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(0 if gi == 0 else 11)
        p.line_spacing = 1.2
        style_run(p.add_run(), 12, True, GREEN).text = gname
        for it in items:
            rich(tf, [("·  ", dict(size=10.5, bold=True, color=GREEN)),
                      (it, dict(size=10.5, color=BODY))],
                 line=1.24, before=4.5)

    l2 = MARGIN + cw + 0.36
    card(s, l2, 1.98, cw, 4.92, fill=LIGHT, radius=0.06)
    bar(s, l2, 1.98, cw, 0.068, fill=GREEN)
    text_at(s, l2 + 0.38, 2.18, cw - 0.76, 0.32, "修改记录",
            size=16, bold=True, color=DARK)
    hline(s, l2 + 0.38, 2.58, cw - 0.76)
    log = [
        ("V1.0", "第 1 周", "确定选题为图书管理系统，画出第一版用例图，当时只有 8 个用例"),
        ("V1.1", "第 2 周", "补上「图书续借」「逾期图书处理」，用例增至 12 个；拆出两个独立的登录用例"),
        ("V2.0", "第 3 周", "提取出 4 个类；「罚金」从独立类并入借阅记录"),
        ("V2.1", "第 3 周", "绘制借书顺序图，补上学生资格校验这一步"),
        ("V3.0", "第 4 周", "完成类图并标注多重性；三张图交叉检查，修正馆藏状态字段"),
    ]
    top = 2.84
    for v, wk, desc in log:
        text_at(s, l2 + 0.38, top, 0.72, 0.28, v, size=12, bold=True, color=GREEN)
        text_at(s, l2 + 1.16, top, 0.94, 0.28, wk, size=11, color=GREY)
        text_at(s, l2 + 2.16, top, cw - 2.58, 0.62, desc, size=11, color=BODY,
                line=1.28)
        top += 0.80
    notes(s, "按作业要求，最后说明一下 AI 的使用情况和修改过程。\n"
             "AI 主要用在三个地方：一是梳理业务流程的时候，让它帮忙列候选的参与者、"
             "用例和名词清单，相当于一个提示作用，列出来之后我们自己逐个筛；"
             "二是核对用例图的符号用法符不符合规范；三是汇报文稿的润色。\n"
             "没用在哪也说清楚：三张图全部是我们自己在 ProcessOn 上画的，"
             "类里的属性和方法是对着业务一条条定下来的，没有让 AI 直接生成。\n"
             "有两处是 AI 提了建议、我们讨论之后改掉的：一个是给罚金单独建类，"
             "我们判断它依附于借阅记录，合并了；另一个是建议用 include 抽公共步骤，"
             "我们判断这套用例之间没有真正的复用，保留了平铺结构。\n"
             "右边是我们的修改记录，前后一共五个版本，主要改动都标在上面了。")

    # ==================== 18 结束 ====================
    s = blank(prs)
    bar(s, 0, 0, SW, 0.28, fill=DARK)
    bar(s, SW / 2 - 0.43, 3.44, 0.86, 0.034, fill=GREEN)
    text_at(s, MARGIN, 2.62, CW, 0.72, "谢谢，请老师和同学指正",
            size=34, bold=True, color=DARK, align=PP_ALIGN.CENTER)
    text_at(s, MARGIN, 3.68, CW, 0.34,
            "《信息系统分析与设计》· 作业四 · 基于 UML 的图书管理系统建模",
            size=14, color=GREY, align=PP_ALIGN.CENTER)
    text_at(s, MARGIN, 4.18, CW, 0.34, "、".join(MEMBERS),
            size=13, color=GREEN, align=PP_ALIGN.CENTER)
    notes(s, "我们的汇报到这里，谢谢大家，请老师和同学指正。")

    prs.save(OUT)
    print("OK ->", len(prs.slides), "slides")


if __name__ == "__main__":
    main()
