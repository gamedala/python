from tkinter import *
from tkinterie.tkinterIE import WebView

a=Tk()
a.geometry('700x500+100+100')

w=WebView(a,500,500,'www.baidu.com')
w.pack(expand=True,fill='both')

a.mainloop()
