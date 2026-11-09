# 1､创建结构
import os
project_dir = "output/legal_consultation_model_cpu"
# 创建目录
for subdir in ["data", "models"]:
    os.makedirs(f"{project_dir}/{subdir}", exist_ok=True)
print(f"创建CPU 简化版项目目录: {project_dir}")