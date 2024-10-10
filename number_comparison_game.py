import cv2
import numpy as np
import pytesseract
import pyautogui
import tkinter as tk
from PIL import Image, ImageGrab
import time
import threading
import os
from datetime import datetime


# 设置Tesseract OCR的路径（根据您的安装位置进行调整）
pytesseract.pytesseract.tesseract_cmd = r'E:\tesseract\tesseract.exe'

class NumberComparisonGame:
    def __init__(self):
        self.running = False
        self.thread = None
        # 修改所有坐标定义为 (left, top, right, bottom)
        self.left_number_area = (1280, 285, 1215 + 180, 285 + 125)  # 左侧数字区域
        self.right_number_area = (1480, 315, 1480 + 120, 315 + 100)  # 右侧数字区域
        self.result_area = (1250, 640, 1250 + 360, 640 + 230)  # 结果绘制区域
        self.draw_speed = 0.02  # 减少绘制速度
        self.last_left = None
        self.last_right = None
        self.last_result = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
            print("游戏已开始")

    def stop(self):
        if self.running:
            self.running = False
            print("游戏已停止")

    def run(self):
        consecutive_failures = 0
        max_consecutive_failures = 3  # 连续失败的最大次数

        while self.running:
            left_number = self.recognize_number(self.left_number_area, "left")
            right_number = self.recognize_number(self.right_number_area, "right")
            
            print(f"识别到的数字: 左侧 = {left_number}, 右侧 = {right_number}")
            
            if left_number is None and right_number is None:
                consecutive_failures += 1
                print(f"连续无法识别两个数字: {consecutive_failures}/{max_consecutive_failures}")
                if consecutive_failures >= max_consecutive_failures:
                    print("连续多次无法识别两个数字，停止程序")
                    self.running = False
                    break
            else:
                consecutive_failures = 0  # 重置连续失败计数
                result = self.compare_and_draw(left_number, right_number)
                print(f"比较结果: {result}")
            
            time.sleep(0.3)  # 减少等待时间到0.3秒

    def recognize_number(self, area, side):
        print(f"正在捕获区域: {area}")
        screenshot = ImageGrab.grab(bbox=area)
        
        # 转换为灰度图像
        gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        
        # 应用高斯模糊以减少噪声
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 应用自适应阈值处理
        threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # 应用形态学操作以进一步清理图像
        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # 使用更严格的配置进行OCR
        number = pytesseract.image_to_string(opening, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789 -c tessedit_min_confidence=80')
        print(f"OCR 结果: {number}")
        try:
            return int(number.strip())
        except ValueError:
            print(f"无法识别数字: {number}")
            return None

    def compare_and_draw(self, left, right):
        x1, y1, x2, y2 = self.result_area
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        size = min(x2 - x1, y2 - y1) // 4

        # 处理一边为 None 的情况
        if left is None and right is not None:
            left = right  # 假设左边应该等于右边
        elif right is None and left is not None:
            right = left  # 假设右边应该等于左边

        # 初始化 result 为默认值
        result = '>'  # 默认为等于

        # 检查是否与上次结果相同
        if left == self.last_left and right == self.last_right and (left is not None or right is not None):
            time.sleep(0.1)
            # 如果相同且不全为空，则输出相反的结果
            if self.last_result == '>':
                result = '<'
            elif self.last_result == '<':
                result = '>'
        else:
            # 正常比较
            if left > right:
                result = '>'
            elif left < right:
                result = '<'
            

        # 更新上次的结果
        self.last_left = left
        self.last_right = right
        self.last_result = result

        # 移动到中心点并绘制
        pyautogui.moveTo(center_x, center_y)
        if result == '>':
            self.draw_greater_than(center_x, center_y, size)
        elif result == '<':
            self.draw_less_than(center_x, center_y, size)
        
        
        print(f"在区域 {self.result_area} 绘制了 '{result}'")
        return result

    def draw_greater_than(self, x, y, size):
        pyautogui.mouseDown()
        pyautogui.move(size, size/2, duration=self.draw_speed)  # 右下
        pyautogui.move(-size, size/2, duration=self.draw_speed)  # 左下
        pyautogui.mouseUp()

    def draw_less_than(self, x, y, size):
        pyautogui.mouseDown()
        pyautogui.move(-size, size/2, duration=self.draw_speed)  # 左下
        pyautogui.move(size, size/2, duration=self.draw_speed)  # 右下
        pyautogui.mouseUp()

    
    
class GameGUI:
    def __init__(self, master):
        self.master = master
        self.game = NumberComparisonGame()

        self.master.title("数字比较游戏")

        self.start_button = tk.Button(self.master, text="开始", command=self.start_game)
        self.start_button.pack()

        self.stop_button = tk.Button(self.master, text="停止", command=self.stop_game, state=tk.DISABLED)
        self.stop_button.pack()

    def start_game(self):
        self.game.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_game(self):
        self.game.stop()
        if self.game.thread:
            self.game.thread.join()  # 在 GUI 线程中等待游戏线程结束
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

def create_gui():
    root = tk.Tk()
    GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()