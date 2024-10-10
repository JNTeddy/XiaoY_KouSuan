# 数字比较游戏

这是一个基于Python的游戏，使用计算机视觉和OCR技术来识别屏幕上的数字，比较它们，并使用鼠标移动绘制比较结果。

## 环境要求

- Python 3.7+
- OpenCV (cv2)
- NumPy
- Pytesseract
- PyAutoGUI
- Pillow (PIL)
- Tkinter (通常随Python一起安装)

## 安装步骤

1. 克隆此仓库或下载源代码。

2. 安装所需的Python包：

   ```
   pip install opencv-python numpy pytesseract pyautogui pillow
   ```

3. 安装Tesseract OCR：
   - Windows：从[Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)下载并安装
   - macOS：`brew install tesseract`
   - Linux：`sudo apt-get install tesseract-ocr`

4. 更新脚本中的Tesseract路径：
   打开`number_comparison_game.py`并更新以下行，使用您的Tesseract安装路径：
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'path/to/your/tesseract.exe'
   ```

## 使用说明

1. 运行脚本：
   ```
   python number_comparison_game.py
   ```

2. 将出现一个带有"开始"和"停止"按钮的GUI窗口。

3. 点击"开始"开始游戏。程序将开始识别屏幕上的数字并绘制比较结果。

4. 点击"停止"结束游戏。

## 注意事项

本游戏设计为使用特定的屏幕坐标。您可能需要调整`NumberComparisonGame`类中的坐标值以匹配您的屏幕设置，代码中提供了getwz.py来获取坐标。

