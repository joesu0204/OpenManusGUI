import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import sys

openmanus_path = r'C:\Users\v_zizhousu\OpenManus\main.py'

class OpenManusGUI:
    def __init__(self, master):
        self.master = master
        master.title('OpenManus Chat')
        
        # 设置初始窗口大小
        master.geometry("800x600")  # 初始尺寸800x600
        
        # 配置主窗口网格权重
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # 主框架容器
        self.main_frame = tk.Frame(master)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置主框架内部网格
        self.main_frame.grid_rowconfigure(0, weight=1)    # 聊天区域行
        self.main_frame.grid_rowconfigure(1, weight=0)    # 输入区域行
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 创建聊天显示区域
        self.chat_area = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=80,            # 缩小宽度
            height=15           # 减少高度避免过长
        )
        self.chat_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # 输入区域容器
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # 用户输入框（保留原始宽度）
        self.input_box = tk.Entry(self.input_frame, width=60)  # 调整宽度为60
        self.input_box.pack(side=tk.LEFT, padx=(0,5), pady=5)
        self.input_box.focus_set()  # 设置输入焦点
        
        # 发送按钮（显式保留）
        self.send_button = tk.Button(
            self.input_frame,
            text='Send',
            command=self.send_message,
            width=10  # 固定按钮宽度
        )
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # 绑定窗口调整事件（可选）
        master.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """限制最大宽度避免变形"""
        if event.widget == self.master:
            # 限制最大宽度为1200像素
            if event.width > 1200:
                self.master.geometry("1200x600")
            # 保持输入框和按钮布局稳定
            self.input_box.config(width=60)
            self.send_button.config(width=10)

    def send_message(self):
        user_input = self.input_box.get().strip()
        if not user_input:
            return

        # 显示用户消息
        self.chat_area.insert(tk.END, f'User: {user_input}\n')
        self.input_box.delete(0, tk.END)

        try:
            # 调用OpenManus
            result = subprocess.run(
                [
                    r"C:\Users\v_zizhousu\anaconda3\python.exe",
                    "main.py"
                ],
                input=user_input,
                text=True,
                capture_output=True,
                cwd=r'C:\Users\v_zizhousu\OpenManus'
            )
            
            # 处理错误输出
            if result.stderr:
                raise Exception(f"STDERR: {result.stderr}")
                
            response = result.stdout.strip()

        except Exception as e:
            response = f"Error: {str(e)}"

        # 显示OpenManus回复
        self.chat_area.insert(tk.END, f'OpenManus: {response}\n')
        self.chat_area.see(tk.END)  # 自动滚动到底部

if __name__ == '__main__':
    root = tk.Tk()
    app = OpenManusGUI(root)
    root.mainloop()