# -*- coding: utf-8 -*-
"""用 PowerPoint COM 把生成的 pptx 导出成 PNG 预览，方便检查排版。"""

import os
import sys
import glob
import win32com.client

HERE = os.path.dirname(os.path.abspath(__file__))
PPTX = os.path.join(HERE, "业务场景信息系统建模实践_图书管理系统.pptx")
OUTDIR = os.path.join(HERE, "preview")


def main():
    if not os.path.exists(PPTX):
        print("ERR: pptx not found")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    for f in glob.glob(os.path.join(OUTDIR, "*.PNG")):
        os.remove(f)

    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = None
    try:
        pres = app.Presentations.Open(PPTX, ReadOnly=True, WithWindow=False)
        pres.Export(OUTDIR, "PNG", 1600, 900)
    finally:
        if pres is not None:
            pres.Close()
        app.Quit()

    files = sorted(glob.glob(os.path.join(OUTDIR, "*.PNG")))
    print("exported:", len(files))


if __name__ == "__main__":
    main()
