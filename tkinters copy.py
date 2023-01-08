from win32com.client import Dispatch
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime,time
import numpy as np
import json

class winUI:
    def __init__(self,obj):
        self.win = obj
        # 標題名
        self.win.title('仙境傳說多窗口脫機---插件版本:'+dm.Ver())
        # icoN
        self.win.iconbitmap("C:\\Users\\BOB\\Desktop\\python\\pic\\app.ico")
        # 窗口大小
        self.win.geometry("600x400")
        # 固定窗口大小 0=False 1=True
        self.win.resizable(0,0)
        # 布局
        # place(anchor=CENTER, x=300, y=380) anchor元件置中 X Y 座標
        # 文字
        # self.txt = Text(self.win, width=80, height=25)
        # self.txt.pack()
        # 標籤
        # self.ti_1 = Label(self.win, text='窗口選擇', padx=10)
        # self.ti_1.place(anchor=W, x=5, y=10)
        self.ti_2 = Label(self.win, text='血量%', padx=10)
        self.ti_2.place(anchor=W, x=5, y=60)
        self.ti_3 = Label(self.win, text='魔量%', padx=10)
        self.ti_3.place(anchor=W, x=5, y=85)
        # 輸入框
        self.en_HP = Entry(self.win)
        self.en_HP.place(anchor=W, x=55, y=60, width= 50)
        # self.en_HP.insert(0,0)
        self.en_MP = Entry(self.win)
        self.en_MP.place(anchor=W, x=55, y=85, width= 50)
        # self.en_MP.insert(0,0)
        # 複選框
        self.var1 = IntVar(self.win)
        self.ch = Checkbutton(self.win, text="血魔保護", variable=self.var1, onvalue=1, offvalue=0, padx=10)
        self.ch.place(anchor=W, x=5, y=35)
        # 建立按鈕
        self.but_win = Button(self.win, # 按鈕所在視窗
                                text = '刷新窗口', # 顯示文字
                                command=self.getwin) # 按下按鈕所執行的函數
        self.but_win.place(anchor=W, x=5, y=10)
        self.but_toggle = Button(self.win, # 按鈕所在視窗
                                text = '切換', # 顯示文字
                                command=self.getwin) # 按下按鈕所執行的函數
        self.but_toggle.place(anchor=W, x=220, y=10)
        self.star = Button(self.win, # 按鈕所在視窗
                                text = '啟動' # 顯示文字
                                ) # 按下按鈕所執行的函數
        self.star.place(anchor=W, x=260, y=10)
        self.stop = Button(self.win, # 按鈕所在視窗
                                text = '停止' # 顯示文字
                                ) # 按下按鈕所執行的函數
        self.stop.place(anchor=W, x=300, y=10)
        self.star_all = Button(self.win, # 按鈕所在視窗
                                text = '全部啟動' # 顯示文字
                                ) # 按下按鈕所執行的函數
        self.star_all.place(anchor=W, x=340, y=10)
        self.stop_all = Button(self.win, # 按鈕所在視窗
                                text = '全部停止', # 顯示文字
                                command=self.json_r) # 按下按鈕所執行的函數
        self.stop_all.place(anchor=W, x=405, y=10)
        # 下拉選單
        self.box_窗口Text = StringVar()
        self.box_窗口 = ttk.Combobox(self.win,
                                    textvariable=self.box_窗口Text,
                                    values=[''])
        self.box_窗口.place(anchor=W, x=65, y=10, width= 150)
        # self.box_窗口.bind('<<ComboboxSelected>>', self.json_r)
        # 窗口關閉事件
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)


    # 自訂函數
    def on_closing(self):
        if messagebox.askokcancel("Quit", "確定要離開嗎?"):
            self.win.destroy()
    def getwin(self):
        hwnds = dm.EnumWindow(0, "", "Ragnarok", 2 + 4 + 8 + 16)
        if hwnds == "":
            messagebox.askokcancel("錯誤", "找不到遊戲窗口")
        else:
            arr = hwnds.split(',')
            帳號=[]
            for hwnd in arr:
                name = dm.ReadString(hwnd,"011CBFE8",0,10)
                帳號.append("帳號:"+name+",停止")
            self.box_窗口['value'] = 帳號
    def json_r(self):
        user = self.box_窗口.get()
        with open("test.json", mode="r", encoding="utf-8") as file:
            config=json.load(file)
        print("token", config["token"])
        print("窗口名", config["窗口名"])
        self.en_HP.delete(0, "end") # 清空
        self.en_HP.insert(0,config[user]["血量%"]) # 新增
        self.en_MP.delete(0, "end") # 清空
        self.en_MP.insert(0,config["123456"]["魔量%"]) # 新增

if __name__ == "__main__":
    # 主介面註冊大漠
    dm = Dispatch('dm.dmsoft')
    UIrend=winUI(Tk())
    UIrend.win.mainloop()