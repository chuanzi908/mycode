# -*- coding: utf-8 -*-
"""把桌面版《项目计划书》重排为商业计划书版式（内容一字不动，只改排版）。

  · 封面页 + 目录页 + 页眉页脚（绿色主题，对照 LaTeX 版商业计划书 PDF）
  · 一级/二级标题、正文、表格、图片统一排版
  · 替换“四功能闭环”“技术路线”两张配图
  · 竞品分析配图（产业链与竞争格局）转为表格行，并入上方竞品对比表
"""
import copy
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DESK = Path(r"C:\Users\35111\Desktop")
SRC = DESK / "基于AI图像识别的轻量化病虫害诊断与防治助手——项目计划书（配图版）.docx"
DST = DESK / "基于AI图像识别的轻量化病虫害诊断与防治助手——商业计划书.docx"
FIG = (DESK / "26年大创" / "病虫害AI诊断商业计划书" / "病虫害AI诊断商业计划书"
       / "figures" / "docx")

# ---------------- 配色（与配图一致） ----------------
DARK, GREEN, MINT = "1C3D2E", "2E7D32", "4A7C59"
CARD, CARD2, LINE = "F4F7F5", "EDF1EE", "DDE2E0"
WHITE, INK, GRAY = "FFFFFF", "3A4A44", "778B82"

CN_HEI, CN_SONG, EN_FONT = "黑体", "宋体", "Times New Roman"
BODY_PT, TBL_PT = 12, 10.5
CONTENT_W = 15.6          # 正文可用宽度 cm
TW = 567                  # 1cm = 567 twips

# ---------------- OOXML schema 子元素顺序 ----------------
PPR_SEQ = ["w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore",
           "w:framePr", "w:widowControl", "w:numPr", "w:suppressLineNumbers",
           "w:pBdr", "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku",
           "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE",
           "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid",
           "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
           "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
           "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle",
           "w:rPr", "w:sectPr", "w:pPrChange"]
TCPR_SEQ = ["w:cnfStyle", "w:tcW", "w:gridSpan", "w:hMerge", "w:vMerge",
            "w:tcBorders", "w:shd", "w:noWrap", "w:tcMar", "w:textDirection",
            "w:tcFitText", "w:vAlign", "w:hideMark"]
TBLPR_SEQ = ["w:tblStyle", "w:tblpPr", "w:tblOverlap", "w:bidiVisual",
             "w:tblStyleRowBandSize", "w:tblStyleColBandSize", "w:tblW", "w:jc",
             "w:tblCellSpacing", "w:tblInd", "w:tblBorders", "w:shd",
             "w:tblLayout", "w:tblCellMar", "w:tblLook", "w:tblCaption",
             "w:tblDescription"]
SECTPR_SEQ = ["w:headerReference", "w:footerReference", "w:footnotePr",
              "w:endnotePr", "w:type", "w:pgSz", "w:pgMar", "w:paperSrc",
              "w:pgBorders", "w:lnNumType", "w:pgNumType", "w:cols"]
RPR_SEQ = ["w:rFonts", "w:b", "w:bCs", "w:i", "w:iCs", "w:caps",
           "w:smallCaps", "w:strike", "w:dstrike", "w:outline", "w:shadow",
           "w:emboss", "w:imprint", "w:noProof", "w:snapToGrid", "w:vanish",
           "w:webHidden", "w:color", "w:spacing", "w:w", "w:kern",
           "w:position", "w:sz", "w:szCs", "w:highlight", "w:u", "w:effect",
           "w:bdr", "w:shd", "w:fitText", "w:vertAlign", "w:rtl", "w:cs",
           "w:em", "w:lang", "w:eastAsianLayout"]


def ins(parent, child, seq, tag):
    """按 OOXML schema 顺序把 child 插入 parent。"""
    try:
        i = seq.index(tag)
    except ValueError:
        parent.append(child)
        return child
    parent.insert_element_before(child, *seq[i + 1:])
    return child


def E(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        key = k if k.startswith("xml:") else "w:" + k
        e.set(qn(key), str(v))
    return e


# ============================================================
# 通用格式工具
# ============================================================
def set_font(run, cn=CN_SONG, size=BODY_PT, bold=False, color=None, italic=False):
    rPr = run._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts")) or ins(rPr, E("w:rFonts"), RPR_SEQ, "w:rFonts")
    for k in ("w:ascii", "w:hAnsi", "w:cs"):
        rf.set(qn(k), EN_FONT)
    rf.set(qn("w:eastAsia"), cn)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def clear_body(p):
    """清空段落的 run / 书签等，保留 pPr。"""
    for tag in ("w:r", "w:hyperlink", "w:bookmarkStart", "w:bookmarkEnd",
                "w:proofErr", "w:ins", "w:del"):
        for e in list(p._p.findall(qn(tag))):
            p._p.remove(e)


def para_fmt(p, align=None, line=1.5, before=0, after=0, indent_chars=0,
             keep_next=False, keep_lines=False):
    pf = p.paragraph_format
    if align is not None:
        pf.alignment = align
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:ind")):
        pPr.remove(old)
    if indent_chars:
        ins(pPr, E("w:ind", firstLineChars=indent_chars * 100,
                   firstLine=int(indent_chars * BODY_PT * 20)), PPR_SEQ, "w:ind")
    if keep_next:
        ins(pPr, E("w:keepNext"), PPR_SEQ, "w:keepNext")
    if keep_lines:
        ins(pPr, E("w:keepLines"), PPR_SEQ, "w:keepLines")


def set_p_border(p, color, sz=8, edges=("bottom",), space=6):
    pPr = p._p.get_or_add_pPr()
    for old in pPr.findall(qn("w:pBdr")):
        pPr.remove(old)
    bdr = E("w:pBdr")
    for e in edges:
        bdr.append(E("w:" + e, val="single", sz=sz, space=space, color=color))
    ins(pPr, bdr, PPR_SEQ, "w:pBdr")


def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:shd")):
        tcPr.remove(old)
    ins(tcPr, E("w:shd", val="clear", color="auto", fill=fill), TCPR_SEQ, "w:shd")


def vcenter(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:vAlign")):
        tcPr.remove(old)
    ins(tcPr, E("w:vAlign", val="center"), TCPR_SEQ, "w:vAlign")


def set_tbl_borders(tbl, color=LINE, sz=4, inside_color=None):
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = E("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        c = inside_color if edge.startswith("inside") and inside_color else color
        b.append(E("w:" + edge, val="single", sz=sz, space=0, color=c))
    ins(tblPr, b, TBLPR_SEQ, "w:tblBorders")


def set_col_widths(tbl, widths):
    tbl.autofit = False
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblLayout")):
        tblPr.remove(old)
    ins(tblPr, E("w:tblLayout", type="fixed"), TBLPR_SEQ, "w:tblLayout")
    for old in tblPr.findall(qn("w:tblW")):
        tblPr.remove(old)
    ins(tblPr, E("w:tblW", w=int(sum(widths) * TW), type="dxa"), TBLPR_SEQ, "w:tblW")
    grid = tbl._tbl.find(qn("w:tblGrid"))
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * TW)))
    for row in tbl.rows:
        for c, w in zip(row.cells, widths):
            c.width = Cm(w)


def set_cell_margins(tbl, top=60, bottom=60, left=100, right=100):
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblCellMar")):
        tblPr.remove(old)
    m = E("w:tblCellMar")
    for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        m.append(E("w:" + k, w=v, type="dxa"))
    ins(tblPr, m, TBLPR_SEQ, "w:tblCellMar")


def cell_text(cell):
    return " ".join(p.text for p in cell.paragraphs).strip()


# ============================================================
# 打开文档 & 页面设置
# ============================================================
doc = Document(str(SRC))
body = doc.element.body


def setup_section(sec):
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.6)
    sec.left_margin = sec.right_margin = Cm(2.7)
    sec.header_distance, sec.footer_distance = Cm(1.4), Cm(1.4)


for s in doc.sections:
    setup_section(s)

# ============================================================
# 样式
# ============================================================
styles = doc.styles
normal = styles["Normal"]
normal.font.name = EN_FONT
normal.font.size = Pt(BODY_PT)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), CN_SONG)
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_after = Pt(0)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def make_style(name, cn, size, bold, color, align, before, after, line=1.5,
               outline_lvl=None):
    try:
        st = styles[name]
    except KeyError:
        st = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = styles["Normal"]
    st.font.name = EN_FONT
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.color.rgb = RGBColor.from_string(color)
    rPr = st.element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = ins(rPr, E("w:rFonts"), RPR_SEQ, "w:rFonts")
    rf.set(qn("w:ascii"), EN_FONT)
    rf.set(qn("w:hAnsi"), EN_FONT)
    rf.set(qn("w:eastAsia"), cn)
    pf = st.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pPr = st.element.get_or_add_pPr()
    for old in pPr.findall(qn("w:outlineLvl")):
        pPr.remove(old)
    if outline_lvl is not None:
        ins(pPr, E("w:outlineLvl", val=outline_lvl), PPR_SEQ, "w:outlineLvl")
    return st


make_style("BP Title", CN_HEI, 26, True, DARK, WD_ALIGN_PARAGRAPH.CENTER, 0, 0)
make_style("BP H1", CN_HEI, 16, True, DARK, WD_ALIGN_PARAGRAPH.CENTER, 24, 16,
           outline_lvl=0)
make_style("BP H2", CN_HEI, 14, True, GREEN, WD_ALIGN_PARAGRAPH.LEFT, 16, 8,
           outline_lvl=1)
make_style("BP Body", CN_SONG, BODY_PT, False, INK, WD_ALIGN_PARAGRAPH.JUSTIFY, 0, 6)
make_style("BP Table", CN_SONG, TBL_PT, False, INK, WD_ALIGN_PARAGRAPH.LEFT, 2, 2)
make_style("BP Caption", CN_SONG, 9.5, False, GRAY, WD_ALIGN_PARAGRAPH.CENTER, 4, 12)
make_style("BP Cover", CN_SONG, BODY_PT, False, INK, WD_ALIGN_PARAGRAPH.CENTER, 0, 6)

# ============================================================
# 1) 正文段落排版
# ============================================================
H1_RE = re.compile(r"^([一二三四五六七八九十]+、|附录)")
H2_RE = re.compile(r"^（[一二三四五六七八九十]+）")
IMG_RID = {}          # 段落序号 -> 图片 rId


def para_kind(t):
    t = t.strip()
    if not t:
        return "blank"
    if H1_RE.match(t):
        return "h1"
    if H2_RE.match(t):
        return "h2"
    return "body"


def has_drawing(p):
    return p._p.find(".//" + qn("w:drawing")) is not None


def blip_rid(p):
    b = p._p.find(".//" + qn("a:blip"))
    return b.get(qn("r:embed")) if b is not None else None


from docx.text.paragraph import Paragraph          # noqa: E402
from docx.table import Table                       # noqa: E402

paras = [Paragraph(e, doc) for e in body.iterchildren() if e.tag == qn("w:p")]
tables = [Table(e, doc) for e in body.iterchildren() if e.tag == qn("w:tbl")]

doc_title_p = paras[0]                             # 原文档标题 → 移到封面
removed_paras = []

for p in paras:
    if p is doc_title_p:
        removed_paras.append(p)
        continue
    txt = p.text.strip()
    if has_drawing(p):
        para_fmt(p, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.0, before=8, after=10,
                 keep_next=True)
        IMG_RID[blip_rid(p)] = p
        continue
    kind = para_kind(txt)
    if kind == "blank":
        removed_paras.append(p)
        continue
    if kind == "h1":
        p.style = styles["BP H1"]
        clear_body(p)
        set_font(p.add_run(txt), cn=CN_HEI, size=16, bold=True, color=DARK)
        para_fmt(p, align=WD_ALIGN_PARAGRAPH.CENTER, before=24, after=16,
                 keep_next=True)
        ins(p._p.get_or_add_pPr(), E("w:outlineLvl", val=0), PPR_SEQ, "w:outlineLvl")
    elif kind == "h2":
        p.style = styles["BP H2"]
        clear_body(p)
        set_font(p.add_run(txt), cn=CN_HEI, size=14, bold=True, color=GREEN)
        para_fmt(p, before=16, after=8, keep_next=True)
        ins(p._p.get_or_add_pPr(), E("w:outlineLvl", val=1), PPR_SEQ, "w:outlineLvl")
    else:
        p.style = styles["BP Body"]
        clear_body(p)
        set_font(p.add_run(txt), cn=CN_SONG, size=BODY_PT, color=INK)
        # 含长 URL 的段落（附录来源）：左对齐并允许西文断行，避免两端对齐拉出大空隙
        has_url = "http" in txt
        para_fmt(p, align=(WD_ALIGN_PARAGRAPH.LEFT if has_url
                           else WD_ALIGN_PARAGRAPH.JUSTIFY),
                 line=1.5, after=6, indent_chars=2)
        if has_url:
            ins(p._p.get_or_add_pPr(), E("w:wordWrap", val="0"),
                PPR_SEQ, "w:wordWrap")

# 删掉标题段与空段（内容已迁到封面）
for p in removed_paras:
    p._p.getparent().remove(p._p)

# ============================================================
# 2) 表格排版
# ============================================================
# 每张表的列宽比例（cm，合计 15.6）
TBL_WIDTHS = {
    0:  [15.6],                                   # 项目基本信息
    1:  [3.4, 5.2, 7.0],                          # 技术指标
    2:  [2.8, 6.6, 6.2],                          # 创新点
    3:  [2.8, 5.6, 7.2],                          # 用户分层
    4:  [2.8, 5.8, 7.0],                          # 盈利模式
    5:  [3.4, 5.8, 6.4],                          # 竞品分析（将扩展）
    6:  [1.9, 6.85, 6.85],                        # SWOT
    7:  [2.7, 3.3, 2.9, 6.7],                     # 团队
    8:  [3.2, 2.6, 9.8],                          # 预算
    9:  [4.4, 3.7, 3.7, 3.8],                     # 营收预测
    10: [1.6, 5.0, 9.0],                          # 里程碑
    11: [2.8, 1.4, 11.4],                         # 风险
}


def fill_cell(cell, text, size=TBL_PT, bold=False, color=INK, align=None,
              cn=CN_SONG):
    ps = cell.paragraphs
    for extra in ps[1:]:
        extra._p.getparent().remove(extra._p)
    p = ps[0]
    clear_body(p)
    set_font(p.add_run(text), cn=cn, size=size, bold=bold, color=color)
    para_fmt(p, align=align or WD_ALIGN_PARAGRAPH.LEFT, line=1.25, before=1.5,
             after=1.5, indent_chars=0)


def style_table(tbl, idx):
    widths = TBL_WIDTHS[idx]
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_col_widths(tbl, widths)
    set_cell_margins(tbl)
    set_tbl_borders(tbl)
    rows = tbl.rows
    ncol = len(rows[0].cells)
    # 信息卡（单格表）
    if ncol == 1:
        c = rows[0].cells[0]
        shade_cell(c, CARD2)
        vcenter(c)
        for p in c.paragraphs:
            txt = p.text.strip()
            clear_body(p)
            set_font(p.add_run(txt), cn=CN_SONG, size=TBL_PT, color=DARK)
            para_fmt(p, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.4, before=2, after=2)
        # 左侧绿色粗边
        tcPr = c._tc.get_or_add_tcPr()
        for old in tcPr.findall(qn("w:tcBorders")):
            tcPr.remove(old)
        b = E("w:tcBorders")
        b.append(E("w:left", val="single", sz=24, space=0, color=GREEN))
        ins(tcPr, b, TCPR_SEQ, "w:tcBorders")
        return
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row.cells):
            txt = cell_text(cell)
            vcenter(cell)
            if ri == 0:
                shade_cell(cell, DARK)
                fill_cell(cell, txt, bold=True, color=WHITE,
                          align=WD_ALIGN_PARAGRAPH.CENTER, cn=CN_SONG)
            else:
                shade_cell(cell, CARD if ri % 2 == 1 else WHITE)
                if ci == 0:
                    fill_cell(cell, txt, bold=True, color=DARK)
                else:
                    fill_cell(cell, txt, color=INK)
    # 表头下方加粗分隔线
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = E("w:tblBorders")
    b.append(E("w:top", val="single", sz=8, space=0, color=DARK))
    b.append(E("w:bottom", val="single", sz=8, space=0, color=DARK))
    b.append(E("w:left", val="none", sz=0, space=0, color="auto"))
    b.append(E("w:right", val="none", sz=0, space=0, color="auto"))
    b.append(E("w:insideH", val="single", sz=4, space=0, color=LINE))
    b.append(E("w:insideV", val="none", sz=0, space=0, color="auto"))
    ins(tblPr, b, TBLPR_SEQ, "w:tblBorders")


# ============================================================
# 3) 替换配图
# ============================================================
NEW_FIGS = {
    "rId8":  FIG / "func_loop.png",        # 四功能闭环
    "rId14": FIG / "tech_roadmap.png",     # 技术路线总览
}
for rid, path in NEW_FIGS.items():
    p = IMG_RID.get(rid)
    if p is None:
        print("!! 未找到图片段落:", rid)
        continue
    clear_body(p)
    p.add_run().add_picture(str(path), width=Cm(15.6))
    para_fmt(p, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.0, before=8, after=10,
             keep_next=True)

# 竞品分析配图（产业链与竞争格局）不再用图，内容并入下方竞品对比表
comp_img = IMG_RID.get("rId15")
if comp_img is not None:
    comp_img._p.getparent().remove(comp_img._p)

# ============================================================
# 4) 竞品表：并入“产业链与竞争格局”内容
# ============================================================
COMP_ROWS = [
    ("国际代表厂商",
     "覆盖产业链上中下游：上游核心部件与数据（多光谱/高光谱相机传感器、AI 芯片与算力、"
     "云计算平台、标注数据集服务）→ 中游系统集成与算法（可见光图像视觉检测、多光谱/高光谱"
     "生理检测、多模态融合检测）→ 下游应用与服务机构（精准植保服务商、无人机与智能农机厂商、"
     "农资企业、农业保险机构）。代表厂商：Taranis、Sentera、Cropin、Fermata、Agrio、ClimateAi、"
     "FlyPix、TMA Innovation、AgroScout、BioScout、Kindwise",
     "主战场在北美·欧洲（技术成熟、大规模农场多、付费意愿高），面向规模化农场，付费门槛高、"
     "本地化不足；亚太（中国/印度/日本/澳大利亚）增长最快、潜力最大，但本地化供给不足；"
     "拉美·非洲仍处于早期探索阶段"),
    ("国内代表厂商",
     "河南云飞、北京依科曼、河南兆迪、山东祥辰、北京爱格瑞；以智能病虫害监测设备与硬件为主，"
     "服务植保站、示范基地与大型园区",
     "硬件重资产、项目制交付，依赖政府与基地采购；面向小农户的轻量化软件方案仍属空白"),
]

tbl5 = tables[5]
target = next((i for i, r in enumerate(tbl5.rows)
               if cell_text(r.cells[0]) == "本方案"), None)
if target is None:
    print("!! 竞品表未找到“本方案”行")
else:
    ref_tr = tbl5.rows[target]._tr
    for _ in COMP_ROWS:
        ref_tr.addprevious(copy.deepcopy(ref_tr))
    t_new = Table(tbl5._tbl, doc)
    for k, data in enumerate(COMP_ROWS):
        for c, txt in zip(t_new.rows[target + k].cells, data):
            fill_cell(c, txt)
    print(f"竞品表已并入 {len(COMP_ROWS)} 行产业链/厂商信息")

# 表格样式统一（在插行之后执行）
for i, t in enumerate(tables):
    style_table(t, i)

# ============================================================
# 5) 封面 + 目录 + 分节
# ============================================================
from docx.text.paragraph import Paragraph as _P     # noqa: E402


def new_p(anchor, text="", cn=CN_SONG, size=BODY_PT, bold=False, color=None,
          align=WD_ALIGN_PARAGRAPH.CENTER, line=1.5, before=0, after=0):
    p_el = OxmlElement("w:p")
    anchor.addprevious(p_el)
    p = _P(p_el, doc)
    if text:
        set_font(p.add_run(text), cn=cn, size=size, bold=bold, color=color)
    para_fmt(p, align=align, line=line, before=before, after=after)
    return p


def new_rule(anchor, color, sz, before=0, after=0):
    p = _P(OxmlElement("w:p"), doc)
    anchor.addprevious(p._p)
    para_fmt(p, line=1.0, before=before, after=after)
    set_p_border(p, color, sz=sz)
    return p


def make_sect_pr(base, strip_refs=True):
    sp = copy.deepcopy(base)
    if strip_refs:
        for tag in ("w:headerReference", "w:footerReference"):
            for e in sp.findall(qn(tag)):
                sp.remove(e)
    return sp


def sect_break(anchor, base):
    """插入分节符（该段落之前的全部内容属于新的一节）。"""
    p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    pPr.append(make_sect_pr(base))
    p.append(pPr)
    anchor.addprevious(p)
    return p


first = next(body.iterchildren())
main_sect = doc.sections[-1]._sectPr

# ---- 封面 ----
for _ in range(5):
    new_p(first, line=1.0, after=6)
new_rule(first, DARK, 24, after=2)
new_p(first, line=1.0, after=10)
new_p(first, "商 业 计 划 书", cn=CN_HEI, size=20, bold=True, color=DARK,
      line=1.4, after=4)
new_p(first, line=1.0, after=14)
new_p(first, "基于 AI 图像识别的", cn=CN_HEI, size=25, bold=True, color=GREEN,
      line=1.5, after=2)
new_p(first, "轻量化病虫害诊断与防治助手", cn=CN_HEI, size=25, bold=True,
      color=GREEN, line=1.5, after=10)
new_p(first, "—— 拍照即诊断 · 诊断即给方案 · 精准即防治 ——", size=12,
      color=GRAY, line=1.5, after=24)
new_p(first, "中国国际大学生创新大赛版", cn=CN_HEI, size=13, bold=True,
      color=MINT, line=1.5, after=22)
new_rule(first, GREEN, 12, after=2)
new_p(first, line=1.0, after=16)
new_p(first, "编制时间：2026 年 9 月", size=12, color=INK, line=1.6, after=2)
new_p(first, "版本号：V1.0　　密级：商业机密", size=10.5, color=GRAY,
      line=1.6, after=40)
new_p(first, "本文件包含商业敏感信息，未经授权请勿外传", size=9, color=GRAY,
      line=1.5, after=0)
sect_break(first, main_sect)          # 封面节结束

# ---- 目录 ----
new_p(first, line=1.0, after=8)
new_p(first, "目　录", cn=CN_HEI, size=18, bold=True, color=DARK, line=1.5,
      after=16)
toc_p = new_p(first, line=1.45, after=0)
toc_run = toc_p.add_run()
_r = toc_run._r
_r.append(E("w:fldChar", fldCharType="begin"))
_instr = OxmlElement("w:instrText")
_instr.set(qn("xml:space"), "preserve")
_instr.text = ' TOC \\o "1-2" \\h \\z \\u '
_r.append(_instr)
_r.append(E("w:fldChar", fldCharType="separate"))
_hint = OxmlElement("w:t")
_hint.text = "（打开文档后按 Ctrl+A、F9 更新目录）"
_r.append(_hint)
_r.append(E("w:fldChar", fldCharType="end"))
set_font(toc_run, size=BODY_PT, color=GRAY)
sect_break(first, main_sect)          # 目录节结束

# ============================================================
# 6) 页眉页脚
# ============================================================
secs = doc.sections
cover_sec, toc_sec, main_sec = secs[0], secs[1], secs[2]

for s in (cover_sec, toc_sec):
    s.header.is_linked_to_previous = False
    s.footer.is_linked_to_previous = False
    for p in list(s.header.paragraphs):
        clear_body(p)
        para_fmt(p, line=1.0)
    for p in list(s.footer.paragraphs):
        clear_body(p)
        para_fmt(p, line=1.0)

from docx.enum.text import WD_TAB_ALIGNMENT     # noqa: E402

hp = main_sec.header.paragraphs[0]
clear_body(hp)
set_font(hp.add_run("基于 AI 图像识别的轻量化病虫害诊断与防治助手"),
         cn=CN_SONG, size=9, color=GRAY)
set_font(hp.add_run("\t商业计划书"), cn=CN_SONG, size=9, color=GRAY)
hp.paragraph_format.tab_stops.add_tab_stop(Cm(15.6), WD_TAB_ALIGNMENT.RIGHT)
para_fmt(hp, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.0, after=3)
set_p_border(hp, GREEN, sz=6, space=2)

fp = main_sec.footer.paragraphs[0]
clear_body(fp)
fr = fp.add_run()
fr._r.append(E("w:fldChar", fldCharType="begin"))
_i = OxmlElement("w:instrText")
_i.set(qn("xml:space"), "preserve")
_i.text = " PAGE "
fr._r.append(_i)
fr._r.append(E("w:fldChar", fldCharType="end"))
set_font(fr, cn=CN_SONG, size=10, color=GRAY)
para_fmt(fp, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.0)

# 正文页码从 1 开始
sp = main_sec._sectPr
for e in sp.findall(qn("w:pgNumType")):
    sp.remove(e)
ins(sp, E("w:pgNumType", start=1), SECTPR_SEQ, "w:pgNumType")

# 打开文档时提示更新域（生成目录）
st = doc.settings.element
for e in st.findall(qn("w:updateFields")):
    st.remove(e)
st.append(E("w:updateFields", val="true"))

print("封面 / 目录 / 页眉页脚 完成")

# 文档属性
cp = doc.core_properties
cp.title = "基于 AI 图像识别的轻量化病虫害诊断与防治助手——商业计划书"
cp.subject = "中国国际大学生创新大赛 项目计划书"
cp.comments = ""

doc.save(str(DST))
print("已保存:", DST.name)
