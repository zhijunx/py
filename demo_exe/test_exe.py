# pip install pyinstaller
# pyinstaller --onefile --windowed test_exe.py
# https://docs.python.org/zh-cn/3.10/library/tkinter.html


import tkinter as tk
from tkinter import messagebox

def on_button_click():
    name = entry.get()
    if name:
        messagebox.showinfo("问候", f"你好, {name}!")
    else:
        messagebox.showwarning("警告", "请输入你的名字")

if __name__ == '__main__':
    print('MAIN_ENTRY')
    # 创建主窗口
    root = tk.Tk()
    root.title("简单应用")
    root.geometry("300x200")

    # 创建控件
    label = tk.Label(root, text="请输入你的名字:")
    label.pack(pady=10)

    entry = tk.Entry(root, width=20)
    entry.pack(pady=5)

    button = tk.Button(root, text="打招呼", command=on_button_click)
    button.pack(pady=10)

    # 启动主循环
    root.mainloop()