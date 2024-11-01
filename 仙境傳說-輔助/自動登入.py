from win32com.client import Dispatch
from win32gui import GetWindowText,GetClassName,EnumWindows
from win32api import ShellExecute
from time import sleep, time
import os
import ctypes
import json
import sys
if getattr(sys, 'frozen', False):
    # 當程式被打包為 exe 時，使用此路徑
    current_dir = os.path.dirname(sys.executable)  # 獲取可執行文件所在的目錄
else:
    # 開發環境下使用 __file__ 獲取路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
dmreg_path = os.path.join(current_dir, 'DmReg.dll')
dm_path = os.path.join(current_dir, 'dm.dll')

def 找字(位置,文字,顏色,偏移,type):
    xy = dm.FindStrWithFont(位置[0],位置[1],位置[2],位置[3],文字,顏色, 1.0, "細明體", 9, 0)
    if xy[1] > -1 :
        if type == True:
            dm.MoveTo(xy[1]+偏移[0],xy[2]+偏移[1])
            dm.LeftClick()
        else:
            return xy
        return True
    else:
        return False
    
def zmRunApp(path):
    p = path.rfind("/")
    dir_path = path[:p]
    ShellExecute(0, 'open', path, '', dir_path,5)

def read_section(section_name):
    if section_name in data:
        return data[section_name]
    else:
        return ''

def 拆分輸入(number_string):
    for digit in number_string:
        dm.KeyPressChar(digit)

class DM:
    def __init__(self):
        try:
            # 加载DmReg.dll库
            dms = ctypes.windll.LoadLibrary(dmreg_path)
            dms.SetDllPathW(dm_path, 0)
            print(f'加载DmReg: {dmreg_path}')
        except Exception as e:
            print(f"加载DLL失败: {e}")
            os._exit(1)

        try:
            # 创建大漠COM对象
            self.dm = Dispatch('dm.dmsoft')
            print("\t大漠插件版本: ", self.dm.Ver())
        except Exception as e:
            print(f"初始化大漠插件失败: {e}")
            os._exit(1)

if __name__ == '__main__':
    dm = DM().dm
    數量 = 0
    # 讀取帳號設定
    with open(current_dir+r'\user.json', 'r', encoding='utf-8') as file: # 讀取 json
        data = json.load(file)
        user_points = read_section('user')
        Setup_points = read_section('Setup')
    # 開始登入帳號
    for 帳號, (密碼, 人物位置) in user_points.items():
        登入開始 = time()
        登入時間 = hwnd = dm_ret = None
        數量 += 1
        print(f'\r數量: {數量} 帳號: {帳號} 密碼: {密碼} 人物位置: {人物位置}',end="")
        # 啟動遊戲路徑
        # print(Setup_points["路徑"])
        zmRunApp(Setup_points["路徑"])
        while not hwnd and not dm_ret:
            hwnd = dm.EnumWindow(0, "DragonRo", "", 1 + 4 + 8 + 16)
            # hwnd = find_windows(window_info) # 獲取窗口控制句柄
            if hwnd:
                dm_ret = dm.SetWindowState(hwnd,12) # 恢復並激活指定窗口
            sleep(0.2)
        sleep(1)
        dm_ret = dm.SetWindowText(hwnd, f'帳號: {帳號} 句柄: {hwnd}') 
        dm_ret = dm.BindWindow(hwnd, 'gdi', 'dx2', 'dx', 4)
        dm.WriteString(hwnd, "011F5374",0 ,帳號)
        dm.WriteInt(hwnd, "011F5384",0,len(帳號))
        # 拆分輸入(帳號)
        dm.KeyPress(9)
        dm.WriteString(hwnd, "011F5374",0 ,密碼)
        dm.WriteInt(hwnd, "011F5384",0,len(密碼))
        #拆分輸入(密碼)
        for _ in range(2):
            dm.KeyPress(13)
            sleep(0.5)
        now位置 = dm.ReadInt(hwnd, "[<啟動-龍氏仙境.exe>+00BC4B74]+100", 0)
        移動 = 人物位置 - now位置
        # print(f'移動 {移動}')
        for _ in range(abs(移動)):
            if 移動 > 0:
                dm.KeyPress(39)
            elif 移動 < 0:
                dm.KeyPress(37)
        dm.KeyPress(13)
        # 創腳色
        # dm.WriteString(hwnd, "011F5374",0 ,f"龍龍{i}")
        # dm.WriteInt(hwnd, "011F5384",0,20)
        # dm.KeyPress(13)
        # sleep(0.5)
        # dm.KeyPress(13)
        sleep(1)
        找字([230,296,721,800], "火之湖" , "9cbdff-000000" ,(45,40), True )
        dm.UnBindWindow()
        登入時間 = time() - 登入開始
        print(f'\r數量: {數量} 帳號: {帳號} 密碼: {密碼} 人物位置: {人物位置} 登入時間: {登入時間:.2f}')
        #sleep(5)