#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File		:	 AutoClick.py
@Time		:	 2021/10/09 15:10:01
@Author	:	 Yaadon 
'''

# here put the import lib
import win32con
import win32gui
import win32ui
import time
# import threading
import numpy as np
import os
from PIL import Image
from PIL import ImageOps
import aircv as ac
import pytesseract
from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT
import string
from win32gui import FindWindow#界面
# import sys
# import cv2
# from memory_pic import *
# import win32api
# import autopy
# from PIL import ImageGrab


class AutoClick():
	"""
	@description	:自動點擊類，包含後台截圖、圖像匹配
	---------
	@param	:
	-------
	@Returns	:
	-------
	"""
	
	PostMessageW = windll.user32.PostMessageW
	SendMessageW = windll.user32.SendMessageW
	MapVirtualKeyW = windll.user32.MapVirtualKeyW
	VkKeyScanA = windll.user32.VkKeyScanA
	ClientToScreen = windll.user32.ClientToScreen

	WM_KEYDOWN = 0x100
	WM_KEYUP = 0x101
	WM_MOUSEMOVE = 0x0200
	WM_LBUTTONDOWN = 0x0201
	WM_LBUTTONUP = 0x202
	WM_MOUSEWHEEL = 0x020A
	WHEEL_DELTA = 120
	WM_SETCURSOR = 0x20
	WM_MOUSEACTIVATE = 0x21

	HTCLIENT = 1
	MA_ACTIVATE = 1

	VkCode = {
		"back":	0x08,
		"tab":	0x09,
		"return":	0x0D,
		"shift":	0x10,
		"control":	0x11,
		"menu":	0x12,
		"pause":	0x13,
		"capital":	0x14,
		"escape":	0x1B,
		"space":	0x20,
		"end":	0x23,
		"home":	0x24,
		"left":	0x25,
		"up":	0x26,
		"right":	0x27,
		"down":	0x28,
		"print":	0x2A,
		"snapshot":	0x2C,
		"insert":	0x2D,
		"delete":	0x2E,
		"lwin":	0x5B,
		"rwin":	0x5C,
		"numpad0":	0x60,
		"numpad1":	0x61,
		"numpad2":	0x62,
		"numpad3":	0x63,
		"numpad4":	0x64,
		"numpad5":	0x65,
		"numpad6":	0x66,
		"numpad7":	0x67,
		"numpad8":	0x68,
		"numpad9":	0x69,
		"multiply":	0x6A,
		"add":	0x6B,
		"separator":	0x6C,
		"subtract":	0x6D,
		"decimal":	0x6E,
		"divide":	0x6F,
		"f1":	0x70,
		"f2":	0x71,
		"f3":	0x72,
		"f4":	0x73,
		"f5":	0x74,
		"f6":	0x75,
		"f7":	0x76,
		"f8":	0x77,
		"f9":	0x78,
		"f10":	0x79,
		"f11":	0x7A,
		"f12":	0x7B,
		"numlock":	0x90,
		"scroll":	0x91,
		"lshift":	0xA0,
		"rshift":	0xA1,
		"lcontrol":	0xA2,
		"rcontrol":	0xA3,
		"lmenu":	0xA4,
		"rmenu":	0XA5
	}
	
	def move_to(self, handle: HWND, x: int, y: int):
		"""移動鼠標到坐標（x, y)

		Args:
				handle (HWND): 窗口句柄
				x (int): 橫坐標
				y (int): 縱坐標
		"""
		# https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
		wparam = 0
		lparam = y << 16 | x
		self.PostMessageW(handle, self.WM_MOUSEMOVE, wparam, lparam)


	def left_down(self, handle: HWND, x: int, y: int):
		"""在坐標(x, y)按下鼠標左鍵

		Args:
				handle (HWND): 窗口句柄
				x (int): 橫坐標
				y (int): 縱坐標
		"""
		# https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
		wparam = 0x001 # MK_LBUTTON
		lparam = y << 16 | x
		self.PostMessageW(handle, self.WM_LBUTTONDOWN, wparam, lparam)


	def left_up(self, handle: HWND, x: int, y: int):
		"""在坐標(x, y)放開鼠標左鍵

		Args:
				handle (HWND): 窗口句柄
				x (int): 橫坐標
				y (int): 縱坐標
		"""
		# https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
		wparam = 0
		lparam = y << 16 | x
		self.PostMessageW(handle, self.WM_LBUTTONUP, wparam, lparam)


if __name__ == '__main__':
	PostMessageW = windll.user32.PostMessageA
	SendMessageW = windll.user32.SendMessageA
	hwnd = FindWindow(None, "Ragnarok") # 获取窗口句柄
	lparam = 611 << 16 | 889
	while 1 :
		time.sleep(1)
		# lparam = (0x21 << 16) | 1
		# print(SendMessageW(hwnd, 0x20, hwnd, lparam))
		# # SendMessageW(hwnd, win32con.WM_SETCURSOR, HTCLIENT, win32con.WM_MOUSEMOVE)
		# # PostMessageW(hwnd, win32con.WM_MOUSEMOVE, 0, lparam)
		# #print(SendMessageW(hwnd, 0x20, hwnd, (0x0200 << 16) | 1))
        # # print(PostMessageW(hwnd, win32con.WM_MOUSEACTIVATE, hwnd, (0x0200<< 16) | 1))
        # # print(PostMessageW(hwnd, win32con.WM_MOUSEACTIVATE, hwnd, (0x0201<< 16) | 1))
        # # print(PostMessageW(hwnd, win32con.WM_MOUSEACTIVATE, hwnd, (0x0202<< 16) | 1))
		# time.sleep(0.1)
		lparam = (win32con.MA_ACTIVATEANDEAT << 16) | 1
		print(PostMessageW(hwnd, win32con.WM_USER+1201, 1, 1))
		print(PostMessageW(hwnd, win32con.WM_USER+1288, 1, 1))
		# print(PostMessageW(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, 611 << 16 | 889))
		# time.sleep(0.1)
		# print(PostMessageW(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 611 << 16 | 889))
		# time.sleep(0.1)
		# print(PostMessageW(hwnd, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, 611 << 16 | 889))
		# time.sleep(0.1)
		# print(PostMessageW(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 611 << 16 | 889))

