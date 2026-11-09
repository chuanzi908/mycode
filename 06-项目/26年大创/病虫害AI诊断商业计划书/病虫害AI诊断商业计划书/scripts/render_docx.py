# -*- coding: utf-8 -*-
"""用本机 Word 打开生成的 docx：更新目录域 → 另存为 PDF，便于检查版式。"""
import sys
import win32com.client as win32
from pathlib import Path

DESK = Path(r"C:\Users\35111\Desktop")
DOCX = DESK / "基于AI图像识别的轻量化病虫害诊断与防治助手——商业计划书.docx"
PDF = DESK / "_preview.pdf"

word = win32.gencache.EnsureDispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
try:
    d = word.Documents.Open(str(DOCX))
    # 更新所有域（生成目录）
    for i in range(1, d.TablesOfContents.Count + 1):
        d.TablesOfContents(i).Update()
    d.Fields.Update()
    d.Repaginate()
    d.Save()
    d.ExportAsFixedFormat(str(PDF), 17)      # 17 = wdExportFormatPDF
    print("页数:", d.ComputeStatistics(2))    # 2 = wdStatisticPages
    d.Close(SaveChanges=0)
finally:
    word.Quit()
print("PDF:", PDF)
