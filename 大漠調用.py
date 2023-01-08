from win32com.client import Dispatch
import os,time,json,ctypes
import win32gui
import requests
Path = "愛如初見"
token = 'Z8NSmX4Tpz3kxW7is09KF0wVWWPUQTpLOW2hxLmKAn9' # LINE Notify 權杖
dms = ctypes.windll.LoadLibrary('./DmReg.dll')
class Operation:
    def __init__(self, hwnd): # 初始化Operation
        dms.SetDllPathW('C:/dm/dm7.dll', 0)
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
        #dm_ret = self.dm.RegEx("jv965720b239b8396b1b7df8b768c919e86e10f","jfiax8yhxfpyqy7","121.204.252.143|121.204.253.161|125.77.165.62|125.77.165.131|123.129.231.44|123.129.231.45|123.129.231.85|123.129.231.86")
        #dm_ret = self.dm.Reg("jv965720b239b8396b1b7df8b768c919e86e10f","jfiax8yhxfpyqy7")
        # if dm_ret != 1 :
        #     print('\t注册失败,只能使用免费功能')
        # else:
        #     print('\t成功註冊,使用腳本插件需要付費,依照使用時間計價,請勿給他人使用 ^_^y')
            
    def Bind(self): # 綁定窗口模式
        dm_ret = self.dm.BindWindowEx(self.hwnd,"dx.graphic.3d.10plus","dx.mouse.position.lock.api|dx.mouse.clip.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor","dx.keypad.state.api|dx.keypad.api","",0)
        if dm_ret == 1:
            msg='\t綁定成功'
        else:
            msg=' 綁定失敗'
        self.dm.SetClientSize(self.hwnd, 1280, 720) # 設定窗口大小
        print('\t窗口大小: ' + str(self.dm.GetClientSize(self.hwnd)) + msg) # 輸出窗口資訊

    def rjson(self): # 讀取 JOSN
        with open("test.json", mode="r", encoding="utf-8") as file:
            self.config=json.load(file)
            print("name", self.config["name"])
            print("cup", self.config["cup"])
            print("kg", self.config["kg"])
            print("參數", self.config["參數"])

    def wjson(self): # 寫入 JOSN
        self.config["name"] = "中文"
        with open("test.json", mode="w") as file:
            json.dump(self.config,file)
# =================== 大漠註冊 ======================

    def ToLeftClick(self,pic_name,inX,inY):
        star = time.time()
        self.dm.moveto(inX,inY)
        self.dm.LeftDown()
        time.sleep(0.1)
        self.dm.LeftUp()
        sum=time.time() - star
        #print(round(sum,3))
        print(pic_name+' 移動點擊左鍵 耗時: %.3f 秒' %sum)

    def FindStr(self,x1,y1,x2,y2,string,color_format,sim):
        xy = self.dm.FindStr(x1,y1,x2,y2,string,color_format,sim)
        if xy[0] != -1:
            return [xy]
        else:
            return [xy]

    def Ocr(self,x1,y1,x2,y2,color_format,sim):
        xy = self.dm.Ocr(self,x1,y1,x2,y2,color_format,sim)
        if xy[0] != -1:
            return [xy]
        else:
            return [xy]

    def FindPic(self,x1, y1, x2, y2, pic_name, delta_color,sim, dir):
        xy = self.dm.FindPic(x1, y1, x2, y2, pic_name, delta_color,sim, dir)
        if xy[0] == 0:
            return obj.ToLeftClick(pic_name,xy[1],xy[2])

    def Notify(self,message,img):
        headers = { "Authorization": "Bearer " + token }
        data = { 'message': message }
        #img_path = Path(r''+self.path+'/'+img)
        image = open(r''+self.path+'/'+img, 'rb')
        print(image)
        files = { 'imageFile': image }
        msg=requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data, files = files)
        print(msg)

window_id = win32gui.FindWindow(None, 'RO仙境傳說：愛如初見') # 獲取窗口句柄

obj = Operation( window_id) # 註冊插件