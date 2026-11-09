# -*- coding: utf-8 -*-
"""PPT 排版工具库：统一的配色、字体、卡片与文本控件。"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn, nsdecls

# ---------- 配色 ----------
DARK   = RGBColor(0x1C, 0x3D, 0x2E)   # 深墨绿：标题
GREEN  = RGBColor(0x2E, 0x7D, 0x32)   # 主绿：强调
LIGHT  = RGBColor(0xF4, 0xF7, 0xF5)   # 浅绿底：卡片
LIGHT2 = RGBColor(0xED, 0xF1, 0xEE)   # 稍深一档的浅绿底
LINE   = RGBColor(0xDD, 0xE2, 0xE0)   # 描边
GREY   = RGBColor(0x77, 0x8B, 0x82)   # 辅助灰
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BODY   = RGBColor(0x33, 0x3D, 0x38)   # 正文

FONT = "微软雅黑"

SW, SH = 13.3333, 7.5   # 16:9 画布尺寸（英寸）
MARGIN = 0.78           # 左右页边距
CW = SW - 2 * MARGIN    # 内容区宽度


# ---------- 底层工具 ----------
def _set_ea(run, typeface=FONT):
    """python-pptx 只设 latin 字体，中文需要额外写入 a:ea。"""
    rPr = run._r.get_or_add_rPr()
    for e in rPr.findall(qn('a:ea')):
        rPr.remove(e)
    ea = parse_xml('<a:ea %s typeface="%s"/>' % (nsdecls('a'), typeface))
    latin = rPr.find(qn('a:latin'))
    if latin is not None:
        latin.addnext(ea)
    else:
        rPr.append(ea)


def style_run(run, size=14, bold=False, color=BODY, italic=False, font=FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    _set_ea(run, font)
    return run


def tb(slide, l, t, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
    """建一个无内边距的文本框，返回 text_frame。"""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    return tf


def para(tf, text, size=14, bold=False, color=BODY, align=PP_ALIGN.LEFT,
         before=0, after=0, line=None, first=False, italic=False,
         indent=None, font=FONT):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if before:
        p.space_before = Pt(before)
    if after:
        p.space_after = Pt(after)
    if line:
        p.line_spacing = line
    if indent is not None:
        p.paragraph_format.left_indent = Inches(indent) if hasattr(p, 'paragraph_format') else None
    if text:
        style_run(p.add_run(), size, bold, color, italic, font).text = text
    return p


def rich(tf, chunks, size=14, align=PP_ALIGN.LEFT, before=0, after=0,
         line=None, first=False):
    """一段里混排多种样式：chunks = [(文本, {样式}), ...]"""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if before:
        p.space_before = Pt(before)
    if after:
        p.space_after = Pt(after)
    if line:
        p.line_spacing = line
    for text, kw in chunks:
        opts = dict(size=size, color=BODY)
        opts.update(kw)
        style_run(p.add_run(), **opts).text = text
    return p


def text_at(slide, l, t, w, h, text, **kw):
    """一次性写入单个文本框。"""
    anchor = kw.pop('anchor', MSO_ANCHOR.TOP)
    align = kw.pop('align', PP_ALIGN.LEFT)
    line = kw.pop('line', None)
    tf = tb(slide, l, t, w, h, anchor=anchor)
    para(tf, text, align=align, line=line, first=True, **kw)
    return tf


# ---------- 形状 ----------
def card(slide, l, t, w, h, fill=LIGHT, line=None, radius=None,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, line_w=0.75):
    s = slide.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.text_frame.word_wrap = True
    tf = s.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return s


def bar(slide, l, t, w, h, fill=GREEN):
    """纯色矩形，用于分隔线、装饰条。"""
    return card(slide, l, t, w, h, fill=fill, line=None,
                shape=MSO_SHAPE.RECTANGLE)


def hline(slide, l, t, w, color=LINE, h=0.012):
    return bar(slide, l, t, w, h, fill=color)


def picture(slide, path, l, t, w=None, h=None, border=LINE):
    pic = slide.shapes.add_picture(path, Inches(l), Inches(t),
                                   Inches(w) if w else None,
                                   Inches(h) if h else None)
    if border is not None:
        pic.line.color.rgb = border
        pic.line.width = Pt(0.75)
    return pic


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ---------- 版式骨架 ----------
def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def page(prs, kicker, title, speaker=None, subtitle=None, page_no=None):
    """标准内容页：小标签 + 标题 + 绿色短线 + 右下页码 + 右上主讲人。"""
    s = blank(prs)
    text_at(s, MARGIN, 0.40, 9.5, 0.28, kicker,
            size=11.5, bold=True, color=GREEN)
    text_at(s, MARGIN, 0.70, 10.6, 0.60, title, size=26, bold=True, color=DARK)
    bar(s, MARGIN + 0.02, 1.36, 0.86, 0.034, fill=GREEN)
    if speaker:
        text_at(s, SW - MARGIN - 2.2, 0.44, 2.2, 0.28, speaker,
                size=11, color=GREY, align=PP_ALIGN.RIGHT)
    if subtitle:
        text_at(s, MARGIN, 1.52, CW, 0.34, subtitle, size=13, color=GREY)
    if page_no:
        text_at(s, SW - MARGIN - 1.0, 7.02, 1.0, 0.26, str(page_no),
                size=10.5, color=GREY, align=PP_ALIGN.RIGHT)
    return s


def bullet_list(tf, items, size=13, gap=7, line=1.28, marker="·",
                marker_color=GREEN, color=BODY, first=True):
    """带圆点标记的条目列表。items 里每项可以是 str 或 (加粗前缀, 正文)。"""
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            head, rest = it
            rich(tf, [(marker + "  ", dict(size=size, bold=True, color=marker_color)),
                      (head, dict(size=size, bold=True, color=DARK)),
                      (rest, dict(size=size, color=color))],
                 size=size, line=line, before=0 if (first and i == 0) else gap,
                 first=(first and i == 0))
        else:
            rich(tf, [(marker + "  ", dict(size=size, bold=True, color=marker_color)),
                      (it, dict(size=size, color=color))],
                 size=size, line=line, before=0 if (first and i == 0) else gap,
                 first=(first and i == 0))
