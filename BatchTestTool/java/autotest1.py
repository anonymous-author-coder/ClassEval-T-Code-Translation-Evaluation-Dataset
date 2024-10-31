import pyautogui
import time
import cv2
import numpy as np
import pytesseract
import os
from datetime import datetime

# 设置 Tesseract-OCR 可执行文件的路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'  # 根据你的安装路径调整

# 定义要检查红色像素的区域
red_pixel_region = (149, 1201, 2,2)  # 替换为检测红色像素的固定区域坐标 (x, y, width, height)

# 定义用于判断是否有文字的区域
text_detection_region = (120,1160,800,200)  # 用于判断有无文字的区域坐标 (x, y, width, height)

# 定义用于记录文本的区域
text_record_region = (590,153,1500,500)  # 用于记录文本的区域坐标，替换为实际的坐标

# 创建保存截图和文本的文件夹
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 红色阈值 - 调整为 RGB(158, 41, 39) 附近的范围
red_lower_bound = np.array([128, 11, 9])    # 红色的低阈值
red_upper_bound = np.array([188, 71, 69])   # 红色的高阈值

# 定义合并输出的文本文件路径
merged_output_file = os.path.join(output_folder, "output.txt")

# 循环操作10次
for i in range(100):
    print(f"正在处理第 {i+1} 次操作")

    # 等待软件启动
    time.sleep(1)

    try:
        # 获取当前时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_screenshot_path = os.path.join(output_folder, f'screenshot_{i+1}_{timestamp}.png')

        # --- 1. 检测固定位置的红色像素 ---
        # 获取指定检测区域的截图
        red_pixel_screenshot = pyautogui.screenshot(region=red_pixel_region)
        red_pixel_screenshot_np = cv2.cvtColor(np.array(red_pixel_screenshot), cv2.COLOR_RGB2BGR)

        # 检查目标区域中的红色像素
        mask = cv2.inRange(red_pixel_screenshot_np, red_lower_bound, red_upper_bound)
        red_pixels = np.sum(mask > 0)

        # --- 2. 在 text_detection_region 区域判断有无文字 ---
        text_detection_screenshot = pyautogui.screenshot(region=text_detection_region)
        text_detection_screenshot_np = np.array(text_detection_screenshot)

        # 识别判断区域的文本
        detection_text = pytesseract.image_to_string(text_detection_screenshot_np)

        # 判断条件：红色像素存在 或 判断区域无文字
        if red_pixels > 0 or not detection_text.strip():
            print(f"第 {i+1} 次操作 - 红色像素存在 或 无文字，记录文本")

            # --- 3. 从 text_record_region 提取并记录文本 ---
            text_record_screenshot = pyautogui.screenshot(region=text_record_region)
            text_record_screenshot_np = np.array(text_record_screenshot)

            # 识别记录区域的文本
            record_text = pytesseract.image_to_string(text_record_screenshot_np)

            # 将无文字或有红色像素的操作信息以及提取的文本追加到合并的文本文件中
            with open(merged_output_file, 'a', encoding='utf-8') as f:
                f.write(f"第 {i+1} 次操作:\n")
                if red_pixels > 0:
                    f.write("检测到红色像素\n")
                if not detection_text.strip():
                    f.write("判断区域无文字\n")
                f.write(f"记录区域提取的文本:\n{record_text}\n\n")

        else:
            print(f"第 {i+1} 次操作 - 区域内有文字且无红色像素，保存全屏截图")
            # 保存全屏截图
            full_screenshot = pyautogui.screenshot()
            full_screenshot.save(full_screenshot_path)
            print(f"截图已保存: {full_screenshot_path}")

    except Exception as e:
        print(f"发生错误: {e}")

    # 执行 Ctrl+F4 操作
    pyautogui.hotkey('ctrl', 'f4')

print("操作完成")
