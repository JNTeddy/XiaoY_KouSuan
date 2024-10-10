import pyautogui
import keyboard

def print_mouse_position():
    # 获取当前鼠标位置
    x, y = pyautogui.position()
    print(f"Current mouse position: ({x}, {y})")

print("按下 'p' 键以获取当前鼠标位置，或按 'q' 键退出程序。")

while True:
    # 检查是否按下 'p' 键
    if keyboard.is_pressed('p'):
        print_mouse_position()
        # 防止重复输出，等待按键释放
        keyboard.wait('p', suppress=True)
    
    # 检查是否按下 'q' 键退出程序
    if keyboard.is_pressed('q'):
        print("程序已退出。")
        break