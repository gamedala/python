# -*- coding: utf-8 -*-
import win32process#进程模块
import win32con,win32gui
from win32con import PROCESS_ALL_ACCESS #Opencress 权限
from ctypes.wintypes import HWND
import win32api#调用系统模块
import ctypes #C语言类型
from ctypes import windll
from win32gui import FindWindow#界面
from time import *
import time

VkCode = {
    "back":  0x08,
    "tab":  0x09,
    "return":  0x0D,
    "shift":  0x10,
    "control":  0x11,
    "menu":  0x12,
    "pause":  0x13,
    "capital":  0x14,
    "escape":  0x1B,
    "space":  0x20,
    "end":  0x23,
    "home":  0x24,
    "left":  0x25,
    "up":  0x26,
    "right":  0x27,
    "down":  0x28,
    "print":  0x2A,
    "snapshot":  0x2C,
    "insert":  0x2D,
    "delete":  0x2E,
    "lwin":  0x5B,
    "rwin":  0x5C,
    "numpad0":  0x60,
    "numpad1":  0x61,
    "numpad2":  0x62,
    "numpad3":  0x63,
    "numpad4":  0x64,
    "numpad5":  0x65,
    "numpad6":  0x66,
    "numpad7":  0x67,
    "numpad8":  0x68,
    "numpad9":  0x69,
    "multiply":  0x6A,
    "add":  0x6B,
    "separator":  0x6C,
    "subtract":  0x6D,
    "decimal":  0x6E,
    "divide":  0x6F,
    "f1":  0x70,
    "f2":  0x71,
    "f3":  0x72,
    "f4":  0x73,
    "f5":  0x74,
    "f6":  0x75,
    "f7":  0x76,
    "f8":  0x77,
    "f9":  0x78,
    "f10":  0x79,
    "f11":  0x7A,
    "f12":  0x7B,
    "numlock":  0x90,
    "scroll":  0x91,
    "lshift":  0xA0,
    "rshift":  0xA1,
    "lcontrol":  0xA2,
    "rcontrol":  0xA3,
    "lmenu":  0xA4,
    "rmenu":  0XA5
}
mouse_event = windll.user32.mouse_event 
PostMessageW = windll.user32.PostMessageA
ClientToScreen = windll.user32.ClientToScreen
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
WM_KEYDOWN = 0x100
WM_KEYUP = 0x101
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120
WM_SETCURSOR = 0x20
WM_MOUSEACTIVATE = 0x21
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VkCode[key]

def key_down(handle: HWND, key: str):
    """按下指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)
    sleep(0.001)
    PostMessageW(handle, WM_KEYUP, wparam, lparam)

def doClick(handle: HWND, x: int, y: int):
    move_to(handle,x,y)
    #win32api.SetCursorPos(cx,cy)
    long_position = win32api.MAKELONG(x, y)#模拟鼠标指针 传送到指定坐标
    PostMessageW(handle, WM_MOUSEMOVE, win32con.MK_LBUTTON, long_position)
    PostMessageW(handle, WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
    time.sleep(0.1)
    PostMessageW(handle, WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起

def move_to( handle: HWND, x: int, y: int):
      """移动鼠标到坐标（x, y)

      Args:
          handle (HWND): 窗口句柄
          x (int): 横坐标
          y (int): 纵坐标
      """
      # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
      wparam = 0
      lparam = y << 16 | x
      PostMessageW(handle, WM_MOUSEMOVE, wparam, lparam)

def GetProcssID(address,bufflength):
    pid = ctypes.c_ulong() # 设置 pid 为 无符号单精度类型
    kernel32 = ctypes.windll.LoadLibrary("kernel32.dll") # 加载动态链接库
    hwnd = FindWindow(None, "Ragnarok") # 获取窗口句柄
    ReadProcessMemory = kernel32.ReadProcessMemory
    hpid, pid = win32process.GetWindowThreadProcessId(hwnd) # 获取窗口ID
    hProcess = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid) # 获取进程句柄
    addr = ctypes.c_ulong()
    ReadProcessMemory(int(hProcess), address, ctypes.byref(addr), bufflength, None) # 读内存
    win32api.CloseHandle(hProcess) # 关闭句柄
    return addr.value
    
def main():
    hwnd = FindWindow(None, "Ragnarok") # 获取窗口句柄
    remote_thread, pid = win32process.GetWindowThreadProcessId(hwnd)
    #win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
    win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    #win32gui.SetFocus(hwnd)
    while(True):
        # MHP = GetProcssID(0x011D0A18, 4)
        # NHP = GetProcssID(0x011D0A14, 4)
        # sun = NHP/MHP*100
        # sleep(0.001)
        # if sun < 99:
        #     star=time.time()
        #     key_down(hwnd,"f1")
        #     print (str(star)+"補血hp:%d" % sun)
        time.sleep(1)
        doClick(hwnd,891,611)

        

if __name__ == '__main__':
    main()

