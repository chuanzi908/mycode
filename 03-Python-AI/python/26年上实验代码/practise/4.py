# id_ocr.py身份证识别
import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog

# 图像预处理
def preprocess(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,bin_img = cv2.threshold(gray,120,255,cv2.THRESH_BINARY)
    return bin_img

# OCR识别
def ocr_recognize(path):
    pic = preprocess(path)
    txt = pytesseract.image_to_string(pic,lang="chi_sim+eng")
    return txt

# 打开文件识别
def select_file():
    path = filedialog.askopenfilename()
    res = ocr_recognize(path)
    show_text.delete(1.0,tk.END)
    show_text.insert(tk.END,res)

# GUI
win = tk.Tk()
win.title("身份证识别系统")
tk.Button(win,text="选择身份证图片",command=select_file).pack()
show_text = tk.Text(win,width=65,height=18)
show_text.pack()
win.mainloop()