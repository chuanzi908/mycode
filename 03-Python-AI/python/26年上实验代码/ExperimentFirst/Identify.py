import easyocr
from PIL import Image, ImageDraw, ImageFont

# 生成模拟车牌
img = Image.new('RGB', (400, 120), color=(0,0,128))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("simhei.ttf", 60)
draw.text((30, 20), "京A12345", fill="white", font=font)
draw.rectangle([(5,5),(395,115)], outline="white", width=2)
img.save('sim_plate.jpg')

# EasyOCR识别
reader = easyocr.Reader(['ch_sim','en'])
result = reader.readtext('sim_plate.jpg')
for det in result:
    print("文本:", det[1], "置信度:", round(det[2],2))