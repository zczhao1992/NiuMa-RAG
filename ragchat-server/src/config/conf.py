import os

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 假设 conf.py 在 src/config/ 目录下
# 那么向上跳两级就是项目根目录
PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(current_file_path)))
