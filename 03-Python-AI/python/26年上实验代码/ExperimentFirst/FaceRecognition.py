# 人脸检测+质量判断+注册+考勤完整代码
from aip import AipFace
import base64
import cv2

# 替换为自己的密钥
APP_ID = '你的AppID'
API_KEY = '你的API Key'
SECRET_KEY = '你的Secret Key'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def img2base64(img_path):
    with open(img_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# 1. 人脸检测
image_path = 'test.jpg'
image = img2base64(image_path)
imageType = 'BASE64'
options = {'face_field': 'quality', 'max_face_num': 1}
result = client.detect(image, imageType, options)
print(result)

# 2. 质量判断
face = result['result']['face_list'][0]
prob = face['face_probability']
blur = face['quality']['blur']
if prob >= 0.9 and blur < 0.5:
    print("图片合格，可注册")
else:
    print("图片不合格")

# 3. 人脸注册
groupId = 'gduf202408'
userId = 'stu01'
client.addUser(image, imageType, groupId, userId)

# 4. 考勤搜索（M:N）
result = client.multiSearch(image, imageType, groupId)
print(result)