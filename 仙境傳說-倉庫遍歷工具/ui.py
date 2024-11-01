"""
UI介面
"""
import random
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.style = Style()
        self.tk_label_m2w2u49l = self.__tk_label_m2w2u49l(self)
        self.tk_label_m2mfu49l = self.__tk_label_m2mfu49l(self)
        self.tk_select_box_m2w2v0f5 = self.__tk_select_box_m2w2v0f5(self)
        self.tk_select_box_m2mfv0f5 = self.__tk_select_box_m2mfv0f5(self)
        self.tk_button_m2w31jpw = self.__tk_button_m2w31jpw(self)
        self.tk_button_m2w323m4 = self.__tk_button_m2w323m4(self)
        self.tk_label_frame_m2w37dcv = self.__tk_label_frame_m2w37dcv(self)
        self.tk_check_button_m2xrfg5x = self.__tk_check_button_m2xrfg5x(self)
        self.tk_label_m2w39jda = self.__tk_label_m2w39jda( self.tk_label_frame_m2w37dcv) 
        self.tk_input_m2w3agz9 = self.__tk_input_m2w3agz9( self.tk_label_frame_m2w37dcv)
        self.tk_label_m2w3d4cd = self.__tk_label_m2w3d4cd( self.tk_label_frame_m2w37dcv) 
        self.tk_input_m2w3d4ce = self.__tk_input_m2w3d4ce( self.tk_label_frame_m2w37dcv) 
        self.tk_label_m2w3ivod = self.__tk_label_m2w3ivod( self.tk_label_frame_m2w37dcv) 
        self.tk_input_m2w3ivoe = self.__tk_input_m2w3ivoe( self.tk_label_frame_m2w37dcv) 
        self.tk_button_m2w4ykm7 = self.__tk_button_m2w4ykm7( self.tk_label_frame_m2w37dcv)
        self.tk_button_m2xggfy1 = self.__tk_button_m2xggfy1( self.tk_label_frame_m2w37dcv)
        self.tk_table_m2w3rgpm = self.__tk_table_m2w3rgpm(self)
        self.tk_button_m2w6ba1e = self.__tk_button_m2w6ba1e(self)
        self.tk_selection_box = self.__tk_selection_box( self) 
    def __win(self):
        self.title("裝備管理工具")
        # 設置窗口大小、居中
        width = 1200
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.minsize(width=width, height=height)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自動隱藏滾動條"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_label_m2w2u49l(self,parent):
        label = Label(parent,text="選擇遍歷類型：",anchor="center", )
        label.place(x=0, y=0, width=100, height=30)
        return label
    def __tk_select_box_m2w2v0f5(self,parent):
        type_var = StringVar(value="個人")
        type_options = ["","倉庫", "個人"]
        type_menu = OptionMenu(parent, type_var, *type_options)
        # cb = Combobox(parent, state="readonly", )
        # cb['values'] = ("個人","倉庫")
        type_menu.place(x=100, y=2, width=80, height=30)
        return type_var
    def __tk_button_m2w31jpw(self,parent):
        btn = Button(parent, text="遍歷個人", takefocus=False,)
        btn.place(x=195, y=0, width=70, height=30)
        return btn
    def __tk_check_button_m2xrfg5x(self,parent):
        self.tk_check_button_m2xrfg6x = IntVar(value=0)
        cb = Checkbutton(parent,text="定時掃描(5s)",variable=self.tk_check_button_m2xrfg6x)
        cb.place(x=280, y=0, width=90, height=30)
        return cb
    def __tk_button_m2w323m4(self,parent):
        btn = Button(parent, text="輸出data.json", takefocus=False,)
        btn.place(x=380, y=0, width=105, height=30)
        return btn
    def __tk_label_frame_m2w37dcv(self,parent):
        frame = LabelFrame(parent,text="篩選",)
        frame.place(x=0, y=29, relwidth=1.0000, relheight=0.8380)
        return frame
    def __tk_label_m2w39jda(self,parent):
        label = Label(parent,text="請輸入要搜索的ID(用逗號分隔,例如: 145,147,158):",anchor="center", )
        label.place(x=0, y=0, width=285, height=30)
        return label
    def __tk_input_m2w3agz9(self,parent):
        ipt = Entry(parent, validate="key", validatecommand=(parent.register(self.only_numeric_and_comma), '%P'))
        ipt.place(x=285, y=0, width=200, height=30)
        return ipt
    def __tk_label_m2mfu49l(self,parent):
        label = Label(parent,text="複製類型：",anchor="center", )
        label.place(x=520, y=0, width=100, height=30)
        return label
    def __tk_select_box_m2mfv0f5(self,parent):
        type_var = StringVar(value="全部")
        type_options = ["","全部", "ID", "名稱", "詞墜", "卡槽"]
        type_menu = OptionMenu(parent, type_var, *type_options)
        type_menu.place(x=600, y=2, width=80, height=30)
        return type_var
    def __tk_label_m2w3d4cd(self,parent):
        label = Label(parent,text="精煉值大於:",anchor="center", )
        label.place(x=675, y=0, width=85, height=30)
        return label
    def __tk_input_m2w3d4ce(self,parent):
        ipt = Entry(parent, validate="key", validatecommand=(parent.register(self.only_numeric), '%P'))
        ipt.place(x=755, y=0, width=100, height=30)
        ipt.insert(0, "0")  # 初始值设为0
        return ipt
    def __tk_label_m2w3ivod(self,parent):
        label = Label(parent,text="強化值大於:",anchor="center", )
        label.place(x=485, y=0, width=85, height=30)
        return label
    def __tk_input_m2w3ivoe(self,parent):
        ipt = Entry(parent, validate="key", validatecommand=(parent.register(self.only_numeric), '%P'))
        ipt.place(x=570, y=0, width=100, height=30)
        ipt.insert(0, "0")  # 初始值设为0
        return ipt
    def __tk_button_m2w4ykm7(self,parent):
        btn = Button(parent, text="更新", takefocus=False,)
        btn.place(x=875, y=0, width=50, height=30)
        return btn
    def __tk_button_m2xggfy1(self,parent):
        btn = Button(parent, text="重複裝備", takefocus=False,)
        btn.place(x=935, y=0, width=70, height=30)
        return btn
    def __tk_button_m2w6ba1e(self,parent):
        btn = Button(parent, text="窗口重設", takefocus=False,)
        btn.place(x=895, y=0, width=105, height=30)
        return btn
    def __tk_table_m2w3rgpm(self,parent):
        # 设置样式
        self.style.configure("Custom.Treeview", font=(10))

        # 表头字段和宽度设置
        columns = {"排序": 49, "精煉": 49, "ID": 79, "名稱": 149, "詞綴": 999, "卡槽": 399}
        # 创建一个框架来容纳 Treeview 和滚动条
        frame = Frame(parent)
        frame.place(x=0, y=80, relwidth=1, relheight=1)
        # 创建 Treeview
        tk_table = Treeview(frame, show="headings", columns=list(columns), style="Custom.Treeview")
        for text, width in columns.items():
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='w', width=width, stretch=False)
        tk_table.grid(row=0, column=0, sticky="nsew")  # 使用 grid 布局
        # 创建垂直滚动条
        vsb = Scrollbar(parent, orient="vertical", command=tk_table.yview)
        tk_table.configure(yscrollcommand=vsb.set)
        # 创建水平滚动条
        hsb = Scrollbar(parent, orient="horizontal", command=tk_table.xview)
        tk_table.configure(xscrollcommand=hsb.set)
        # 使用 pack 或 grid 进行布局
        tk_table.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y",pady=(80, 0))
        hsb.pack(side="bottom", fill="x")
        return tk_table
    def __tk_selection_box(self,parent):
        selection_box = Listbox(parent, selectmode=SINGLE)
        selection_box.config(font=("Helvetica", 10))  # 12 为字体大小，可自行调整
        selection_box.place_forget()  # 初始隐藏
        return selection_box
    def only_numeric(self, value):
        return value.isdigit() or value == ""  # 允许空输入或纯数字
    def only_numeric_and_comma(self, value):
        return all(char.isdigit() or char == ',' for char in value) or value == "" # 允许数字、逗号或空字符串

class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_m2w31jpw.bind('<Button-1>',self.ctl.search)
        self.tk_check_button_m2xrfg5x.bind('<Button-1>',self.ctl.research)
        self.tk_button_m2w323m4.bind('<Button-1>',self.ctl.outputJson)
        self.tk_input_m2w3agz9.bind("<Double-Button-1>", self.ctl.show_selection_box)
        self.tk_button_m2w4ykm7.bind('<Button-1>',self.ctl.refresh)
        self.tk_button_m2xggfy1.bind('<Button-1>',self.ctl.equipment)
        self.tk_button_m2w6ba1e.bind('<Button-1>',self.ctl.hwnd_binding)
        self.tk_table_m2w3rgpm.bind("<Double-Button-1>", self.ctl.on_double_click)
        self.tk_select_box_m2w2v0f5.trace("w", self.ctl.update_button_text)
        pass
    def __style_config(self):
        self.title(f'裝備管理工具 目前尋找 {self.ctl.read_string("01572430" )} 的倉庫')
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()