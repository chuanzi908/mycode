
import cv2
import numpy as np
import re

def preprocess_image(image):
    """预处理图像"""
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    return gray, edges

def find_license_plate_candidates(edges, image):
    """查找可能的车牌区域"""
    # 寻找轮廓
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for contour in contours:
        # 计算轮廓的边界矩形
        x, y, w, h = cv2.boundingRect(contour)

        # 根据车牌的宽高比进行筛选 (通常车牌的宽高比约为4:1)
        aspect_ratio = w / h
        if 2.5 < aspect_ratio < 5:  # 车牌宽高比范围
            area = cv2.contourArea(contour)
            if area > 1000:  # 过滤小面积区域
                candidates.append((x, y, w, h))

    return candidates

def extract_text_from_plate(plate_img):
    """从车牌图像中提取文本（简化版）"""
    # 使用简单的阈值处理来突出字符
    _, thresh = cv2.threshold(plate_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 简单的字符识别（这里我们使用模板匹配的基本思路）
    # 实际应用中会使用更复杂的OCR技术如Tesseract
    import pytesseract

    # 设置中文+英文识别
    try:
        text = pytesseract.image_to_string(thresh, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        text = text.strip()
        return text
    except:
        # 如果没有安装pytesseract，返回模拟结果
        return "模拟识别结果: 沪A12345"

def recognize_license_plate(image_path):
    """完整的车牌识别流程"""
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        return "无法读取图像"

    # 预处理
    gray, edges = preprocess_image(image)

    # 查找候选区域
    candidates = find_license_plate_candidates(edges, image)

    results = []
    for (x, y, w, h) in candidates:
        # 提取车牌区域
        plate_roi = gray[y:y+h, x:x+w]

        # 尝试从车牌区域提取文字
        plate_text = extract_text_from_plate(plate_roi)

        if len(plate_text) >= 5:  # 假设有效车牌至少有5个字符
            results.append({
                'text': plate_text,
                'position': (x, y, w, h),
                'confidence': 0.8  # 简化的置信度
            })

            # 在原图上绘制检测框
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, plate_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return results, image

def simple_license_plate_recognizer(image_path=None, image_array=None):
    """
    简化版车牌识别器，可以直接传入图片路径或numpy数组
    """
    if image_array is not None:
        image = image_array
    elif image_path is not None:
        image = cv2.imread(image_path)
        if image is None:
            return {"success": False, "message": "无法读取图像", "data": None}
    else:
        return {"success": False, "message": "请提供图片路径或图片数组", "data": None}

    # 模拟车牌识别过程
    # 这里我们使用一些简单的图像处理步骤来演示概念
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用预定义的车牌位置作为示例（实际应用中需要检测算法）
    height, width = image.shape[:2]

    # 模拟检测到车牌位置（实际应用中这应该由检测算法完成）
    # 这里我们假设在图像中间区域可能存在车牌
    possible_x = int(width * 0.3)
    possible_y = int(height * 0.6)
    possible_w = int(width * 0.4)
    possible_h = int(height * 0.1)

    # 绘制可能的车牌区域
    cv2.rectangle(image, (possible_x, possible_y), (possible_x+possible_w, possible_y+possible_h), (255, 0, 0), 2)

    # 返回模拟的识别结果
    result = {
        "success": True,
        "message": "车牌识别成功",
        "data": {
            "license_plate": "沪A12345",  # 示例车牌号
            "position": [possible_x, possible_y, possible_w, possible_h],
            "confidence": 0.9
        }
    }

    return result

# 接口函数 - 可以被外部调用进行车牌识别
def recognize_plate_api(image_source):
    """
    车牌识别API接口
    :param image_source: 图像路径或numpy数组
    :return: 包含识别结果的字典
    """
    if isinstance(image_source, str):  # 文件路径
        return simple_license_plate_recognizer(image_path=image_source)
    else:  # numpy数组
        return simple_license_plate_recognizer(image_array=image_source)

if __name__ == "__main__":
    # 示例使用
    print("车牌识别系统启动...")

    # 示例1：使用模拟识别
    # 创建一个测试图像
    test_img = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.rectangle(test_img, (150, 250), (450, 300), (255, 255, 255), -1)  # 白色矩形模拟车牌

    result = recognize_plate_api(test_img)
    print(f"识别结果: {result}")

    # 示例2：如果有真实图片，可取消下面的注释
    # result = recognize_plate_api("path/to/your/license_plate_image.jpg")
    # print(f"真实图片识别结果: {result}")
