# -*- coding: utf-8 -*-
"""核对新旧文档内容是否一字未丢。"""
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

DESK = Path(r"C:\Users\35111\Desktop")
SRC = DESK / "基于AI图像识别的轻量化病虫害诊断与防治助手——项目计划书（配图版）.docx"
DST = DESK / "基于AI图像识别的轻量化病虫害诊断与防治助手——商业计划书.docx"


def norm(s):
    """规范化：去掉所有空白与全角空格，便于逐字比对。"""
    s = s.replace("\u3000", "").replace("\xa0", "")
    return re.sub(r"\s+", "", s)


def dump(path):
    d = Document(str(path))
    out = []
    for child in d.element.body.iterchildren():
        if child.tag == qn("w:p"):
            p = Paragraph(child, d)
            out.append(norm(p.text))
        elif child.tag == qn("w:tbl"):
            t = Table(child, d)
            for r in t.rows:
                for c in r.cells:
                    out.append(norm(c.text))
    return [x for x in out if x]


src, dst = dump(SRC), dump(DST)
src_join, dst_join = "".join(src), "".join(dst)

print(f"源文档文本块: {len(src)}   新文档文本块: {len(dst)}")
print(f"源文档字符数: {len(src_join)}   新文档字符数: {len(dst_join)}")

# 1) 源文档里每个文本块，是否都能在新文档中找到
missing = []
for t in src:
    if t not in dst_join:
        missing.append(t)

print("\n=== 原文档中未能完整出现在新文档的文本块 ===")
if not missing:
    print("（无）—— 所有原文内容均已保留")
for t in missing:
    print(f"  [{len(t)}字] {t[:160]}")

# 2) 逐段落级比对：源有多少块没进新文档
print("\n=== 新文档比源文档多出的文本块（封面/目录/新增行） ===")
extra = [t for t in dst if t not in src_join]
for t in extra[:40]:
    print(f"  [{len(t)}字] {t[:120]}")
print(f"  共 {len(extra)} 块")
