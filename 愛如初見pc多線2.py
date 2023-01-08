from re import L
from win32com.client import Dispatch
import os,time,json,ctypes,threading
import win32gui
import requests
Path = "愛如初見"
Window_name = 'RO仙境傳說：愛如初見'
token = 'Z8NSmX4Tpz3kxW7is09KF0wVWWPUQTpLOW2hxLmKAn9' # LINE Notify 權杖
# ================= 檢查檔案是否缺少 =================
try:
    dms = ctypes.windll.LoadLibrary('C:/dm/DmReg.dll')
except Exception:
    input('缺少 C:/dm/DmReg.dll')
    exit()
dms.SetDllPathW('C:/dm/dm7.dll', 0)
if os.path.isfile('C:/dm/dm7.dll'):
    print("\tC:/dm/dm7.dll 檔案存在")
else:
    input('缺少 C:/dm/dm7.dll')
    exit()
# ================= 遍歷窗口 =================
def demo_top_windows(window):
    hWndList = []
    window_hwnd = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for h in hWndList:
        if not h:
            return
        title = win32gui.GetWindowText(h)
        if window == title:
            window_hwnd.append(h)
            clsname = win32gui.GetClassName(h)
            print ('\t窗口句柄:%s 窗口標題:%s 窗口類名:%s' %(h,title,clsname))
    return window_hwnd
# ================= 創造物件&註冊 =================
def reg_dm(註冊碼,附加碼):
    regdm = Dispatch('dm.dmsoft')
    dm_ret = regdm.Reg(註冊碼,附加碼) 
    if dm_ret == -1 :
        print('可能防火牆攔截,如果可以正常訪問大漠插件網站，那就可以肯定是被防火牆攔截' + str(dm_ret) )
    elif dm_ret == -2 :
        print('進程沒有以管理員方式運行' + str(dm_ret) )
    elif dm_ret == 0 :
        print('未知錯誤' + str(dm_ret) )
    elif dm_ret == 2 :
        print('餘額不足' + str(dm_ret) )
    elif dm_ret == 3 :
        print('綁定了本機器，但是賬戶餘額不足50元' + str(dm_ret) )
    elif dm_ret == 4 :
        print('註冊碼錯誤' + str(dm_ret) )
    elif dm_ret == 5 :
        print('你的機器或者IP在黑名單列表中或者不在白名單列表中' + str(dm_ret) )
    elif dm_ret == 6 :
        print('非法使用插件. 一般出現在定制插件時，使用了和綁定的用戶名不同的註冊碼' + str(dm_ret) )
    elif dm_ret == 7 :
        print('你的帳號因為非法使用被封禁' + str(dm_ret) )
    elif dm_ret == 8 :
        print('ver_info不在你設置的附加白名單中' + str(dm_ret) )
    elif dm_ret == 77 :
        print('機器碼或者IP因為非法使用，而被封禁' + str(dm_ret) )
    elif dm_ret == 777 :
        print('同一個機器碼註冊次數超過了服務器限制' + str(dm_ret) )
    elif dm_ret == -8 :
        print('版本附加信息長度超過了20' + str(dm_ret) )
    elif dm_ret == -9 :
        print('版本附加信息裡包含了非法字母' + str(dm_ret) )
    elif dm_ret == -10 :
        print('非法的參數ip' + str(dm_ret) )
    else:
        print('\t成功註冊,使用腳本插件需要付費,依照使用時間計價,請勿給他人使用 ^_^y')
    print("\t大漠插件版本: ",regdm.Ver())
    path = regdm.GetBasePath()+Path # 尋找dll路徑並配置文件夾
    print('\t附件路徑存放: ',path)
    print('\t=================================================================')
    return path
# ================= 大漠 =================
class Operation(threading.Thread):
    def __init__(self,hwnd,path): # 初始化Operation
        super(Operation,self).__init__()
        self.daemon = True
        self.dm = Dispatch('dm.dmsoft')
        self.path = self.dm.SetPath(path) # 配置全局路徑
        self.hwnd = hwnd
        self.dm_ret = self.dm.SetDict(0, "字典.txt") # 配置字典
        print('\t[' + str(self.hwnd) + '] 字典加載: ', str(self.dm_ret))
        self.dm_ret = self.dm.BindWindowEx(self.hwnd,"dx.graphic.3d.10plus","dx.mouse.position.lock.api|dx.mouse.clip.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor","dx.keypad.state.api|dx.keypad.api","",0)
        if self.dm_ret == 1:
            msg='\t綁定成功'
        else:
            msg=' 綁定失敗'
        window = self.dm.GetClientSize(self.hwnd)
        if window[1] != 1280 & window[2] != 720 :
            self.dm.SetClientSize(self.hwnd, 1280, 720) # 設定窗口大小
        print('\t[' + str(self.hwnd) + '] 窗口大小: ' + str(self.dm.GetClientSize(self.hwnd)) + msg) # 輸出窗口資訊

    def run(self):
        print ("啟動线程：" + self.name )
        self.script()
        print ("退出线程：" + self.name)
# =================== 大漠註冊 ======================
    def 切換(self,index):
        self.dm = self.dm_all[index]

    def rjson(self): # 讀取 JOSN
        with open("test.json", mode="r", encoding="utf-8") as file:
            self.config=json.load(file)
            print("name", self.config["name"])

    def ToLeftClick(self,pic_name,inX,inY):
        star = time.time()
        self.dm.moveto(inX,inY)
        self.dm.LeftDown()
        time.sleep(0.1)
        self.dm.LeftUp()
        sum=time.time() - star
        #print(round(sum,3))
        print(time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()) + ' [' + str(self.hwnd) + '] ' + pic_name + ' 移動點擊左鍵 耗時: %.3f 秒' %sum)

    def FindStr(self, x1, y1, x2, y2, string, color_format, sim, Click): # 找文字
        xy = self.dm.FindStr(x1, y1, x2, y2, string, color_format, sim)
        if xy[0] != -1 :
            if Click == 1:
                self.ToLeftClick(string,xy[1],xy[2])
            return True
        else:
            return False

    def Ocr(self,x1,y1,x2,y2,color_format,sim): # 文字識別
        xy = self.dm.Ocr(self,x1,y1,x2,y2,color_format,sim)
        if xy[0] != -1:
            return [xy]

    def FindPic(self,x1, y1, x2, y2, pic_name, delta_color,sim, dir, Click): # 找圖
        xy = self.dm.FindPic(x1, y1, x2, y2, pic_name, delta_color,sim, dir)
        if xy[0] != -1 :
            if Click == 1:
                self.ToLeftClick(pic_name,xy[1],xy[2])
            return True
        else:
            return False

    def Notify(self,message,img):
        headers = { "Authorization": "Bearer " + token }
        data = { 'message': message }
        #img_path = Path(r''+self.path+'/'+img)
        image = open(r''+self.path+'/'+img, 'rb')
        print(image)
        files = { 'imageFile': image }
        msg=requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data, files = files)
        print(msg)
        
    def script(self):
        print ( self.daemon )
        print(self.hwnd)
        while 1:
            self.statr=self.FindStr(530,312,751,337,'您已斷線請重新登入','4f6fbc-404040',0.9,0)
            if self.statr == True:
                print('[' + str(self.hwnd) + '] 重新登入')
                while 1:
                    self.FindStr(612,461,666,485,'確認','fafafd-404040',0.9,1)
                    time.sleep(0.2)
                    self.FindStr(576,602,704,636,'進|入|遊|戲','fafafd-404040',0.9,1)
                    time.sleep(0.2)
                    self.FindStr(1064,655,1163,681,'開|始|遊|戲','fafafd-404040',0.9,1)
                    time.sleep(0.2)
                    self.FindStr(1147,200,1197,217,'全|自|動','fafafd-404040',0.6,1)
                    time.sleep(0.2)
                    self.statr=self.FindStr(954,278,1038,303,'全|部|魔|物','5e79bf-404040',0.8,1)
                    if self.statr == True:
                        print('[' + str(self.hwnd) + '] 成功重新登入並寫點選Auto')
                        break
                    time.sleep(1)
            else:
                self.FindPic(751,454,777,478,"紅包.bmp","000000",0.95,0,1)
                #self.FindPic(608,652,640,683,"對話.bmp","000000",0.9,0,1)
                #self.FindPic(1130,15,1257,55,"點擊跳過.bmp","000000",0.8,0,1)
                self.FindPic(587,482,709,519,"省電模式中.bmp","101010",0.8,0,1)
                self.FindPic(534,660,821,715,"點擊任意區域關閉頁面.bmp","101010",0.8,0,1)
            time.sleep(0.2)
            if stop_threads: 
                break

# ================= 主程序 =================
if __name__ == '__main__':
    path = reg_dm("jv965720b239b8396b1b7df8b768c919e86e10f","jfiax8yhxfpyqy7")
    hWndList = demo_top_windows(Window_name)

    threads = []
    for hWnd in hWndList:
        threads.append(Operation(hWnd,path)) # 註冊插件
    for t in threads:
        t.start()
        stop_threads = True
    while 1:
        pass
    for t in threads:
        t.kill()