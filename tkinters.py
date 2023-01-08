from tkinter import *
from tkinter import messagebox
import datetime,time
class winUI:
    def __init__(self,obj):
        self.win = obj
        # 標題名
        self.win.title('Hello World')
        # icoN
        self.win.iconbitmap("C:\\Users\\BOB\\Desktop\\python\\pic\\app.ico")
        # 窗口大小
        self.win.geometry("600x400")
        # 布局
        # place(anchor=CENTER, x=300, y=380) anchor元件置中 X Y 座標
        # 固定窗口大小 0=False 1=True
        self.win.resizable(0,0)
        # 文字
        self.txt = Text(self.win, width=80, height=25)
        self.txt.pack()
        # 輸入框
        self.en = Entry(self.win)
        self.en.pack()
        # 複選框
        self.var1 = IntVar(self.win)
        self.ch = Checkbutton(self.win, text="GOOGLE", variable=self.var1, onvalue=1, offvalue=0, command = self.hello)
        self.ch.pack()
        # 建立按鈕
        self.button = Button(self.win, # 按鈕所在視窗
                        text = 'Hello', # 顯示文字
                        command = self.hello) # 按下按鈕所執行的函數
        self.button.place(anchor=CENTER, x=300, y=380)
        # 窗口關閉事件
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.gettime()
    # 自訂函數
    def on_closing(self):
        if messagebox.askokcancel("Quit", "確定要離開嗎?"):
            self.win.destroy()
    def hello(self):
        t = self.en.get()+str(self.var1.get())
        self.txt.insert(END,t+"Hello, world.\n")
    def gettime(self):
        s = str(datetime.datetime.now())+'\n'
        self.txt.insert(END,s)
        self.txt.see(END)
        self.win.after(1000,self.gettime) # 每隔1s呼叫函數 gettime 自身獲取時間

UIrend=winUI(Tk())

# for ttt in range(1,5):
#     UIrend.txt.insert(END,'\tC:/dm/dm7.dll '+str(ttt)+'檔案存在\n')
#     time.sleep(1)
UIrend.win.mainloop()