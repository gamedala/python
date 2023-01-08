from tkinter import *
import datetime,time
class windowUI:
    def __init__(self,obj):
        self.window = obj
        self.window.title('Hello World')
        self.window.geometry("600x400+250+150")
        self.txt=Text(self.window)
        self.txt.pack()
            # 建立按鈕
        self.button = Button(self.window,          # 按鈕所在視窗
                        text = 'Hello',  # 顯示文字
                        command = self.hello) # 按下按鈕所執行的函數

            # 以預設方式排版按鈕
        self.button.pack()
        self.gettime()
        # 自訂函數
    def hello(self):
        self.txt.insert(END,"Hello, world.\n")
    def gettime(self):
        s=str(datetime.datetime.now())+'\n'
        self.txt.insert(END,s)
        self.window.after(1000,self.gettime)  # 每隔1s呼叫函數 gettime 自身獲取時間

UI=Tk()
UIrend=windowUI(UI)

print('貓貓叫')
for ttt in range(1,5):
    UIrend.txt.insert(END,'\tC:/dm/dm7.dll '+str(ttt)+'檔案存在\n')
    time.sleep(1)
UIrend.window.mainloop()