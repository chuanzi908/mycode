import cv2
from aip import AipFace
import base64
import numpy as np


def face_detection_image(image_path):
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 读取图片
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 在检测到的人脸周围画矩形
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # 显示结果
    cv2.imshow('Detected Faces', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img


def face_detection_camera():
    """
    使用摄像头进行实时人脸检测
    """
    # 加载预训练的人脸检测分类器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    print("按 'q' 键退出程序")

    while True:
        # 读取帧
        ret, frame = cap.read()

        if not ret:
            print("无法接收帧（可能是摄像头断开连接）")
            break

        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 在检测到的人脸周围画矩形
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # 显示结果
        cv2.imshow('Real-time Face Detection', frame)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("选择人脸识别模式:")
    print("1. 图片人脸识别")
    print("2. 摄像头实时人脸识别")

    choice = input("请输入选项 (1 或 2): ")

    if choice == "1":
        image_path = input("请输入图片路径: ")
        try:
            result_img = face_detection_image(image_path)
            print("人脸识别完成！")
        except Exception as e:
            print(f"处理图片时出错: {e}")
    elif choice == "2":
        print("启动摄像头实时人脸识别...")
        face_detection_camera()
    else:
        print("无效选项")

