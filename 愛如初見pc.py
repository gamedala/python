from win32com.client import Dispatch
import os,time,json,ctypes
import win32gui
import requests
Path = "愛如初見"
Window_name = 'RO仙境傳說：愛如初見'
token = 'Z8NSmX4Tpz3kxW7is09KF0wVWWPUQTpLOW2hxLmKAn9' # LINE Notify 權杖
try:
    dms = ctypes.windll.LoadLibrary('C:/dm/DmReg.dll')
except Exception:
    input('缺少 C:/dm/DmReg.dll')
    exit()
config = 0
def rjson(): # 讀取 JOSN
    with open("config.json", mode="r", encoding="utf-8") as file:
        config = json.load(file)
        # print("name", self.config["name"])
        # print("cup", self.config["cup"])
        # print("kg", self.config["kg"])
        # print("參數", self.config["參數"])

def wjson(): # 寫入 JOSN
    config["name"] = "中文"
    with open("test.json", mode="w") as file:
        json.dump(config,file)

class Operation:
    def __init__(self, hwnd): # 初始化Operation
        dms.SetDllPathW('C:/dm/dm7.dll', 0)
        if os.path.isfile('C:/dm/dm7.dll'):
            print("\tC:/dm/dm7.dll 檔案存在")
        else:
            input('缺少 C:/dm/dm7.dll')
            exit()
        try:
            dm = Dispatch('dm.dmsoft')
        except Exception:
            os.system(r'regsvr32 /s %s\dm.dll' % os.getcwd())
            dm = Dispatch('dm.dmsoft')
        print("\t大漠插件版本: ",dm.Ver())
        self.dm = dm
        self.hwnd = hwnd
        self.path = self.dm.GetBasePath()+Path
        self.dm.SetPath(self.path)
        print('\t附件路徑存放: ',self.path)
        dm_ret = self.dm.SetDict(0, "字典.txt")
        print('\t字典加載: ', str(dm_ret))
        dm_ret = self.dm.Reg("jv965720b239b8396b1b7df8b768c919e86e10f","jfiax8yhxfpyqy7")
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
            
    def Bind(self): # 綁定窗口模式
        dm_ret = self.dm.BindWindowEx(self.hwnd,"dx.graphic.3d.10plus","dx.mouse.position.lock.api|dx.mouse.clip.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor","dx.keypad.state.api|dx.keypad.api","",0)
        if dm_ret == 1:
            msg='\t綁定成功'
        else:
            msg=' 綁定失敗'
        self.dm.SetClientSize(self.hwnd, 1280, 720) # 設定窗口大小
        print('\t窗口大小: ' + str(self.dm.GetClientSize(self.hwnd)) + msg) # 輸出窗口資訊

# =================== 大漠註冊 ======================

    def ToLeftClick(self,pic_name,inX,inY):
        star = time.time()
        self.dm.moveto(inX,inY)
        self.dm.LeftDown()
        time.sleep(0.1)
        self.dm.LeftUp()
        sum=time.time() - star
        #print(round(sum,3))
        print(time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()) +  pic_name + ' 移動點擊左鍵 耗時: %.3f 秒' %sum)

    def FindStr(self, x1, y1, x2, y2, string, color_format, sim, Click): # 找文字
        xy = self.dm.FindStr(x1, y1, x2, y2, string, color_format, sim)
        if xy[0] != -1 :
            if Click == 1:
                obj.ToLeftClick(string,xy[1],xy[2])
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
                obj.ToLeftClick(pic_name,xy[1],xy[2])
            return True
        else:
            return False

    def Notify(self,message): # Notify訊息通知
        headers = { "Authorization": "Bearer " + token }
        data = { 'message': message }
        # image = open(r''+self.path+'/'+img, 'rb')
        # print(image)
        # files = { 'imageFile': image }
        msg=requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data)
        print(msg)

if __name__ == '__main__':
    window_id = win32gui.FindWindow(None, Window_name) # 獲取窗口句柄
    if window_id == 0:
        input("找不到窗口 " + Window_name)
        exit()
    obj = Operation( window_id) # 註冊插件
    obj.Bind() # 綁定窗口
    #rjson()
    while 1:
        statr=obj.FindStr(530,312,751,337,'您已斷線請重新登入','4f6fbc-404040',0.9,0)
        if statr == True:
            print('重新登入')
            while 1:
                obj.FindStr(612,461,666,485,'確認','fafafd-404040',0.9,1)
                time.sleep(0.2)
                obj.FindStr(576,602,704,636,'進|入|遊|戲','fafafd-404040',0.9,1)
                time.sleep(0.2)
                obj.FindStr(1064,655,1163,681,'開|始|遊|戲','fafafd-404040',0.9,1)
                time.sleep(0.2)
                obj.FindStr(1147,200,1197,217,'全|自|動','fafafd-404040',0.8,1)
                time.sleep(0.2)
                statr=obj.FindStr(954,278,1038,303,'全|部|魔|物','5e79bf-404040',0.8,1)
                if statr == True:
                    print('成功重新登入並寫點選Auto')
                    break
                time.sleep(0.2)
        else:
            obj.FindPic(751,454,777,478,"紅包.bmp","000000",0.95,0,1)
            #obj.FindPic(608,652,640,683,"對話.bmp","000000",0.9,0,1)
            #obj.FindPic(1130,15,1257,55,"點擊跳過.bmp","000000",0.8,0,1)
            obj.FindPic(587,482,709,519,"省電模式中.bmp","050505",0.8,0,1)
            obj.FindPic(534,660,821,715,"點擊任意區域關閉頁面.bmp","101010",0.8,0,1)
        time.sleep(0.2)