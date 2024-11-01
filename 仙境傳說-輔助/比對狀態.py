#coding=utf-8

import tkinter as tk
from tkinter import messagebox, scrolledtext
from  win32com.client import Dispatch
import win32gui
import sys
import os
import ctypes
current_path = os.path.dirname(sys.argv[0])
# 設置 DLL 的路徑
dll_path = os.path.join(current_path, 'DmReg.dll')
# 加載 DLL
dms = ctypes.windll.LoadLibrary(dll_path)
# 定義全局變量
buff_temp = []
class Operation:
    def __init__(self,hwnd):
        dms.SetDllPathW(current_path+"/dm.dll", 0)
        self.dm = Dispatch('dm.dmsoft')
# 執行按鈕點擊事件
def on_button_click():
    global buff_temp
    address = int("01505E5C", 16) # 起始
    
    if hWnd == 0:
        messagebox.showerror("Error", "未找到窗口")
        return
    
    buff = []
    print(f"hWnd {hWnd}")
    for i in range(60):
        buffs = job.dm.ReadInt(hWnd, hex(address),0)
        if buffs > 0 and buffs != -1:
            buff.append(buffs)
            address += 4
        elif buffs == -1 or buffs == 0:
            break
    
    
    differences = []
    
    for b in buff:
        if b not in buff_temp and b != -1:
            differences.append(b)
    
    result_text.delete('1.0', tk.END)
    for diff in differences:
        result_text.insert(tk.END, f"{diff}\n")
    
    
    buff_temp = buff.copy()

# 創建UI
root = tk.Tk()
root.title("Memory Compare Tool")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

button = tk.Button(frame, text="執行", command=on_button_click)
button.pack(pady=5)

result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
result_text.pack(pady=5)
hWnd = win32gui.FindWindow(None, "Ragnarok")
job = Operation(hWnd) # 註冊插件
root.mainloop()
