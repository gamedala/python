"""
邏輯處理
"""
import win32api
import win32gui
import win32con
import win32process
import ctypes
from collections import defaultdict
from colorama import Fore, Style, init
from win32con import PROCESS_ALL_ACCESS # Opencress 權限
import sys
import re
import os
from json import loads, dump, load
from os import path
from ui import Win
from tkinter import messagebox,END
from wmi import WMI
from hashlib import sha256

class Controller:
    # 導入UI類後，替換以下的 object 類型，將獲得 IDE 屬性提示功能
    ui: Win
    def __init__(self):
        self.check_machine =self.check_machine_code()
        # if not self.check_machine_code() :
        #     messagebox.showerror("錯誤", "機器碼不匹配，無法啟動應用程序。")
        #     exit()
        # 初始化 colorama
        init(autoreset=True)
        self.itemss = []
        self.kernel32 = ctypes.windll.LoadLibrary("kernel32.dll") # 加載動態鏈接庫
        self.psapi = ctypes.windll.psapi
        self.QueryFullProcessImageName = self.kernel32.QueryFullProcessImageNameW
        self.QueryFullProcessImageName.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.LPWSTR, ctypes.POINTER(ctypes.wintypes.DWORD)]
        self.QueryFullProcessImageName.restype = ctypes.wintypes.BOOL
        if getattr(sys, 'frozen', False):
            # 當程式被打包為 exe 時，使用此路徑
            self.current_dir = path.dirname(sys.executable)  # 獲取可執行文件所在的目錄
        else:
            # 開發環境下使用 __file__ 獲取路徑
            self.current_dir = path.dirname(path.abspath(__file__))
        self.window_id = win32gui.FindWindow('Fairy_RO', None) # 窗口 類名, 標題
        if not self.window_id:
            messagebox.showerror('錯誤','找不到遊戲窗口, 請開啟遊戲後再開啟程序!')
            quit()
        self.process_handle, self.temp_link = self.get_process_handle_from_hwnd(self.window_id) # 打開進程 進程,路徑
        suffixs_lates = self.json讀取(self.current_dir+r'\詞墬.json', 'r')
        self.suffixs_lates = loads(suffixs_lates) # 詞墜中文列表
        self.found_names, self.found_scripts = self.find_cards_with_series(self.temp_link+r'\system\itemInfo_true.lub') # 讀取文本並存入 名稱 說明
        pass

    def init(self, ui):
        """
        得到UI實例，對組件進行初始化配置
        """
        self.ui = ui

    def show_selection_box(self, evt):
        print("<selection-1>事件未處理:",evt)
        # 顯示選擇框
        # 設置位置
        if not self.ui.tk_selection_box.winfo_viewable():
            self.ui.tk_selection_box.place(x=285, y=80, width=350, height=300)
            # 綁定選擇事件
            self.ui.tk_selection_box.bind("<ButtonRelease-1>", self.on_select)
        else:
            self.ui.tk_selection_box.place_forget()  # 隱藏選擇框
            

    def on_select(self, evt):
        print("<selection-2>事件未處理:",evt)
        # 檢查選擇框是否可見
        if not self.ui.tk_selection_box.winfo_viewable():
            self.ui.tk_selection_box.place_forget()  # 隱藏選擇框
        else:
            # 獲取選中值並提取數值部分
            selected_value = self.ui.tk_selection_box.get(self.ui.tk_selection_box.curselection())
            number_part = re.findall(r'\d+', selected_value.split(":")[0])  # 提取前面的數字
            if number_part:
                current_text = self.ui.tk_input_m2w3agz9.get()
                if number_part[0] not in current_text.split(","):
                    self.ui.tk_input_m2w3agz9.insert(END, ("," if current_text else "") + number_part[0])  # 插入數值部分到輸入框
            self.ui.tk_selection_box.place_forget()  # 隱藏選擇框

    def check_machine_code(self):
        cpu_serial_number = self.get_CPU_info()
        mainboard_serial_number = self.get_mainboard_info()
        machine_code = self.generate_machine_code(cpu_serial_number, mainboard_serial_number)
        
        # 這裡假設你有一個預定義的機器碼進行比較b3adfd3e84f1d6cc
        predefined_machine_code = [ '14c5673dada288ca','10428ccc3c8db2dd',
                                    'b3adfd3e84f1d6cc','8d11da0eeba50eb8','d73df39c1d230cd8','e4295f9ae9ab14a7','06b9cd415d477f16',
                                    '51aca331282774d5','11d99052b4fc8cf7','b634dd465c11fb32','08790ce26e7b144a','490e4ee2df8629c9',
                                    'a166c5089d9ec1a9']
 
        return machine_code in predefined_machine_code

    def generate_machine_code(self, cpu_serial_number, mainboard_serial_number, length=16):
        """
        獲取機器碼
        """
        # 混合 CPU 和主板序列號
        combined_string = cpu_serial_number + mainboard_serial_number
        
        # 計算 SHA-256 哈希
        sha256_hash = sha256(combined_string.encode()).hexdigest()
        
        # 截取前 length 位作為機器碼
        machine_code = sha256_hash[:length]
        print(f'machine {machine_code}')
        return machine_code

    def get_CPU_info(self):
        s = WMI()
        cpu_serial_number = ""
        for Processor in s.Win32_Processor():
            cpu_serial_number = Processor.ProcessorId.strip()
        return cpu_serial_number

    def get_mainboard_info(self):
        s = WMI()
        mainboard_serial_number = ""
        for board_id in s.Win32_BaseBoard():
            mainboard_serial_number = board_id.SerialNumber.strip().strip('.')
        return mainboard_serial_number

    def open_process(self,pid):
        """
        打開進程
        """
        PROCESS_ALL_ACCESS = (win32con.PROCESS_QUERY_INFORMATION |
                            win32con.PROCESS_VM_OPERATION |
                            win32con.PROCESS_VM_READ |
                            win32con.PROCESS_VM_WRITE)
        return win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    def get_module_base(self, module_name):
        """
        獲取模塊基址 進程,模塊名稱
        """
        hModules = (ctypes.c_void_p * 1024)()
        cb_needed = ctypes.c_ulong()
        # 使用原始句柄而不是 PyHANDLE 對像
        self.psapi.EnumProcessModulesEx(self.process_handle.handle, ctypes.byref(hModules), ctypes.sizeof(hModules), ctypes.byref(cb_needed), 0x03)
        module_count = cb_needed.value // ctypes.sizeof(ctypes.c_void_p)
        # 遍歷模塊，找到匹配的模塊名
        for i in range(module_count):
            module_handle = hModules[i]
            # 獲取模塊名
            module_filename = ctypes.create_unicode_buffer(260)
            self.psapi.GetModuleBaseNameW(self.process_handle.handle, module_handle, ctypes.byref(module_filename), 260)
            if module_name.lower() in module_filename.value.lower():
                return module_handle  # 返回模塊基址
        return None

    def read_memory(self, address, size=4, data_type='int'):
        """
        讀取進程內存數值，根據地址、大小和數據類型返回相應的數值或字串。
        """
        # 將地址從16進制字符串轉換為整數
        mem_address = int(address, 16)
        ReadProcessMemory = self.kernel32.ReadProcessMemory
        # 根據數據類型選擇合適的 ctypes 類型
        if data_type == 'int':
            addr = ctypes.c_int32()
        elif data_type == 'uint':
            addr = ctypes.c_uint32()
        elif data_type == 'short':
            addr = ctypes.c_int16()
            size = 2
        elif data_type == 'ushort':
            addr = ctypes.c_uint16()
            size = 2 if size == 4 else size
        elif data_type == 'float':
            addr = ctypes.c_float()
        elif data_type == 'double':
            addr = ctypes.c_double()
            size = 8
        elif data_type == 'Big5':  # 處理 Big5 編碼的字符串
            buffer = ctypes.create_string_buffer(size)
            addr = ctypes.c_size_t()  # 占位符
        else:
            addr = ctypes.c_ulong()
        try:
            # Big5 字符串類型的內存讀取
            if data_type == 'Big5':
                success = ReadProcessMemory(
                    int(self.process_handle), ctypes.c_void_p(mem_address), buffer, size, ctypes.byref(addr)
                )
                if not success:
                    print(f"讀取 Big5 字符串失敗，地址：{address}")
                    return None
                return buffer.raw  # 返回字節數據
            # 其他數據類型的內存讀取
            success = ReadProcessMemory(
                int(self.process_handle), mem_address, ctypes.byref(addr), size, None
            )
            if not success:
                print(f"讀取失敗，地址：{address}")
                return None
            return addr.value  # 成功返回讀取到的值
        except Exception as e:
            print(f"內存讀取異常: {e}，地址：{address}")
            return None

    def read_string(self, address, offsets=[], max_length=100, encoding='Big5'):
        """
        讀取進程內存字串 進程,記憶體位置,偏移量[0xa5,0xa],大小,類型
        """
        address = int(address, 16)  # 起始地址
        if offsets:
            for offset in offsets:
                # 讀取指針的值（地址）
                pointer_value = self.read_memory(hex(address), data_type='ulong')
                # 當指針為 None 時返回錯誤
                if pointer_value is None:
                    print(f"無法讀取內存地址 {hex(address)}，偏移量 {offset} 無效")
                    return None
                # 更新地址為指針值加上偏移量
                address = pointer_value + offset
                
        byte_data = self.read_memory( hex(address), max_length,'Big5')
        try:
            string_data = byte_data.split(b'\x00', 1)[0]  # 以空字符為終止符分割字符串
            return string_data.decode(encoding)  # 解碼成字符串，指定 Big5 編碼
        except UnicodeDecodeError:
            return None  # 解碼失敗返回 None

    def get_process_handle_from_hwnd(self,hwnd):
        """
        通過窗口句柄獲取進程ID，並打開進程
        """
        # 獲取進程ID
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]  # 獲取進程ID
        # 打開進程
        process_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
        try:
            # 定義緩衝區來存儲文件路徑
            buffer_size = ctypes.wintypes.DWORD(260)  # 假設路徑長度不超過 260 個字符
            buffer = ctypes.create_unicode_buffer(buffer_size.value)
            
            # 獲取進程可執行文件路徑
            if self.QueryFullProcessImageName(process_handle.handle, 0, buffer, ctypes.byref(buffer_size)):
                folder_path = "\\".join(buffer.value.split("\\")[:-1]) + "\\"
                print(f"窗口頂層句柄: {hwnd} 窗口進程ID: {pid} 進程路徑: {folder_path}")
                return self.open_process(pid), folder_path  # 返回完整路徑
            else:
                raise ctypes.WinError(ctypes.get_last_error())  # 拋出異常
        finally:
            win32api.CloseHandle(process_handle)

    def find_cards_with_series(self,filename):
        """
        讀取lub輸出 名稱[ID],說明[ID]
        """
        current_id = None  # 當前處理的卡片ID
        found_name = {}    # 存儲符合條件的卡片名
        found_script = {}  # 存儲符合條件的卡片描述
        inside_description = False  # 用來判斷是否在 identifiedDescriptionName 內
        # 打開文件逐行讀取
        with open(filename, 'r', encoding='big5', errors='replace') as file:
            matcha = ""  # 放在外部，只在 identifiedDescriptionName 塊中拼接
            for line in file:
                line = line.strip()  # 去除兩端的空格或換行符
                # 檢查是否是ID行，例如：[30046] = {
                if line.startswith('[') and '= {' in line:
                    current_id = int(line.split(']')[0][1:])
                    inside_description = False  # 遇到新卡片，重置描述塊標記
                # 檢查是否有 identifiedDisplayName
                if current_id and 'identifiedDisplayName' in line:
                    match = re.search(r'identifiedDisplayName\s*=\s*"(.*?)",', line)
                    if match:
                        item_name = match.group(1)
                        found_name[current_id] = item_name  # 保存卡片名稱
                # 檢查是否結束 identifiedDescriptionName 塊
                if inside_description and '},' in line:
                    inside_description = False  # 退出描述部分
                    found_script[current_id] = self.format_description(matcha.strip(),1)  # 保存卡片描述
                    matcha = ""  # 重置 matcha
                # 當位於 identifiedDescriptionName 塊內部時，繼續拼接描述
                if inside_description:
                    match = re.sub(r'<INFO>.*?</INFO>', '', line)
                    if match :
                        matcha += match  # 拼接每一行描述
                # 檢查是否進入 identifiedDescriptionName 塊
                if line.strip() == 'identifiedDescriptionName = {' and current_id is not None:
                    inside_description = True  # 完整匹配才進入描述部分
        return found_name, found_script
    
    def format_description(self,description,type=0):
        """
        去除多餘字符
        """
        # 分割字符串並去除每行的引號和多餘字符
        description_list = [line.strip('", ') for line in description.split(",") if line.strip('", ')]
        # 去除每行開頭的 \t\t 以及其他空白字符
        description_list = [line.lstrip("\t\n\r ") for line in description_list]
        # 如果某一行以引號開頭，去除引號
        description_list = [line[1:] if line.startswith('"') else line for line in description_list]
        # 拼接並加入 <br> 換行標籤
        formatted_description = "<br>".join(description_list)
        # 轉換色碼
        if type == 0:
            formatted_description = self.convert_color_codes(formatted_description)
        return formatted_description
    
    def convert_color_codes(self,text,type=0):
        """
        將 `^xxxxxx` 的色碼轉換為 HTML 的顏色標記，^000000 被視為重置顏色。
        """
        # 匹配顏色代碼的正則表達式
        color_code_pattern = re.compile(r"\^([0-9a-fA-F]{6})")
        # 定義一個堆棧來管理顏色的嵌套
        color_stack = []
        result = ""
        last_pos = 0
        # 遍歷匹配到的色碼
        for match in color_code_pattern.finditer(text):
            # 提取匹配到的色碼及其位置
            color_code = match.group(1)
            start, end = match.span()
            # 把匹配之前的內容加到結果中
            result += text[last_pos:start]
            if color_code == '000000':
                # 遇到 ^000000 認為是重置顏色，關閉最後的 <span>
                if color_stack:
                    if type == 0:
                        result += f'<font style="color: #{color_code}">'
                    else:
                        result += f''
                    color_stack.pop()
            else:
                # 添加顏色標記
                if type == 0:
                    result += f'<font style="color: #{color_code}">'
                else:
                    result += f''
                color_stack.append(color_code)
            last_pos = end
        # 添加最後剩下的內容
        result += text[last_pos:]
        # 關閉所有打開的 <span> 標籤
        if color_stack:
            result += "</font>"
            color_stack.pop()
        return result

    def json讀取(self, temp, type, encodings="utf-8", errorss='replace'):
        """
        JSON讀取
        """
        with open(temp, type, encoding=encodings, errors=errorss) as file: # 讀取 json
            return file.read()

    def 物品掃瞄(self,exe_addint):
        """
        物品記憶體掃瞄  洞槽, 詞墜名, 詞墜數值
        """
        洞1 = int(self.read_memory(hex(exe_addint-16)))
        洞2 = int(self.read_memory(hex(exe_addint-12)))
        洞3 = int(self.read_memory(hex(exe_addint-8)))
        洞4 = int(self.read_memory(hex(exe_addint-4)))
        洞 = [洞1, 洞2, 洞3, 洞4]
        詞墜1 = int(self.read_memory(hex(exe_addint+112), data_type="ushort" ))
        詞墜1_1 = int(self.read_memory(hex(exe_addint+114), data_type="ushort" ))
        詞墜1_2 = int(self.read_memory(hex(exe_addint+116), 1, data_type="ushort" ))
        詞墜2 = int(self.read_memory(hex(exe_addint+117), data_type="ushort" ))
        詞墜2_1 = int(self.read_memory(hex(exe_addint+119), data_type="ushort" ))
        詞墜2_2 = int(self.read_memory(hex(exe_addint+121), 1, data_type="ushort" ))
        詞墜3 = int(self.read_memory(hex(exe_addint+122), data_type="ushort" ))
        詞墜3_1 = int(self.read_memory(hex(exe_addint+124), data_type="ushort" ))
        詞墜3_2 = int(self.read_memory(hex(exe_addint+126), 1, data_type="ushort" ))
        詞墜4 = int(self.read_memory(hex(exe_addint+127), data_type="ushort" ))
        詞墜4_1 = int(self.read_memory(hex(exe_addint+129), data_type="ushort" ))
        詞墜4_2 = int(self.read_memory(hex(exe_addint+131), 1, data_type="ushort" ))
        詞墜5 = int(self.read_memory(hex(exe_addint+132), data_type="ushort" ))
        詞墜5_1 = int(self.read_memory(hex(exe_addint+134), data_type="ushort" ))
        詞墜5_2 = int(self.read_memory(hex(exe_addint+136), 1, data_type="ushort" ))
        詞墜_1 = [詞墜1,詞墜2,詞墜3,詞墜4,詞墜5]
        詞墜_2 = [詞墜1_1,詞墜2_1,詞墜3_1,詞墜4_1,詞墜5_1]
        詞墜_3 = [詞墜1_2,詞墜2_2,詞墜3_2,詞墜4_2,詞墜5_2]
        suffix1 = self.generate_string(詞墜1)
        suffix2 = self.generate_string(詞墜2)
        suffix3 = self.generate_string(詞墜3)
        suffix4 = self.generate_string(詞墜4)
        suffix5 = self.generate_string(詞墜5)
        return 洞,詞墜_1,詞墜_2,詞墜_3,[suffix1,suffix2,suffix3,suffix4,suffix5]

    def generate_string(self,template_id):
        """
        定義生成字符串的函數
        """
        template_id_str = str(template_id)
        # 檢查模板 ID 是否在字典中，如果不存在則返回空字符串
        if template_id != 0 and template_id_str in self.suffixs_lates:
            suffix_template = self.suffixs_lates[template_id_str]
            if '%d' in suffix_template:
                return suffix_template
            return suffix_template
        return ''

    def generate_string2(self,temp, value1, value2=0):
        if '%d' in temp:
            return temp % (value1, value2)
        return temp

    def 自動換行(self,suffix1='',suffix2='',suffix3='',suffix4='',suffix5=''):
        suffix = ''
        if suffix1:
            suffix += '槽1: ' + suffix1
        if suffix2:
            suffix += ' 槽2: ' + suffix2
        if suffix3:
            suffix += ' 槽3: ' + suffix3
        if suffix4:
            suffix += ' 槽4: ' + suffix4
        if suffix5:
            suffix += ' 槽5: ' + suffix5
        return suffix

    def insert_to_table(self, name, values):
        """插入數據到表格中"""
        self.ui.tk_table_m2w3rgpm.insert("", index="end", text=name, values=values)
    def search_data(self):
        windowsinfo = win32gui.IsWindow(self.window_id)
        if windowsinfo:
            for row in self.ui.tk_table_m2w3rgpm.get_children():
                self.ui.tk_table_m2w3rgpm.delete(row)
            ii = 0
            self.itemss = []
            typelisst = ['防具','武器']
            search_type = self.ui.tk_select_box_m2w2v0f5.get() # 類型
            exe_address = self.get_module_base("RO_Fairy.exe") # RO_Fairy.exe 模塊位置
            base_offsets = [0x34]
            add = base_offsets[:]
            if "倉庫" == search_type:
                self.倉庫名稱 = self.read_string(hex(exe_address+int("00E8F620",16)), [0x13C, 0xC0])
                ITEM_add = exe_address + int("0116B920", 16)
                倉庫最大 = hex(exe_address + int("116B924", 16))
            elif "露天" == search_type:
                ITEM_add = exe_address + int("00E8F698", 16)
                倉庫最大 = hex(exe_address + int("116B934", 16))
                base_offsets = [0xc8, 0x34]
                add = base_offsets[:]
            else:
                ITEM_add = exe_address + int("0116B8F8", 16)
                倉庫最大 = hex(exe_address + int("116B8FC", 16))
            倉庫 = self.read_memory(倉庫最大)
            # print(倉庫)
            if 倉庫 < 1 and "露天" != search_type :
                messagebox.showerror("錯誤", '未開啟倉庫... 或檢測不到數量 ')
            else:
                for i in range(1,倉庫+1):
                    if "露天" == search_type:
                        add.insert(1, 0x0)  # 在最後一個 0x34 前插入 0x0
                    else:
                        add.insert(-1, 0x0)  # 在最後一個 0x34 前插入 0x0
                    exe_addint = ITEM_add
                    for offset in add: # 計算偏移位置
                        pointer_value = self.read_memory(hex(exe_addint), data_type='ulong')
                        exe_addint = pointer_value + offset # 指針+偏移量
                    item = self.read_string(hex(exe_addint) ) # 物品ID
                    if item.isdigit():
                        item = int(item)
                    if item : # 有物品ID 且 搜尋ID也有
                        output =''
                        洞槽, suffix_ID, suffix_veal1, suffix_veal2, suffix_name = self.物品掃瞄(exe_addint) # 獲取物品資訊
                        types = int(self.read_memory(hex(exe_addint-44), data_type="ushort"  )) # 類型
                        精煉 = int(self.read_memory(hex(exe_addint+52), data_type="ushort"  )) # 精煉值
                        個人 = None
                        if search_type == '個人':
                            個人 = int(self.read_memory(hex(exe_addint+72), data_type="ushort"  )) # 精煉值
                            # print(個人)
                        if (types == 4 or types == 5) and 個人!=1:
                            ii += 1
                            item_name,item_說明 = self.found_names.get(item, '未知'), self.convert_color_codes(self.found_scripts.get(item, '未知'))
                            洞_id = [] # 賦予空值
                            for 洞數 in 洞槽: # 迴圈洞槽
                                if 洞數 > 0: # 如果有物品
                                    match = self.found_names.get(洞數, None)  # 使用 .get() 避免 KeyError
                                    match2 = self.found_scripts.get(洞數, None)  # 使用 .get() 避免 KeyError
                                    if match:
                                        洞名 = match  # 獲取正則匹配的值
                                    else:
                                        洞名 = "未知"  # 若匹配失敗，設置一個默認值
                                    if match2:
                                        說明 = match2  # 獲取正則匹配的值
                                        說明 = self.convert_color_codes(說明,1)
                                    else:
                                        說明 = "未知"  # 若匹配失敗，設置一個默認值
                                    洞_id.append([洞名,說明])  # 使用 append 方法添加元素到列表中
                                else:
                                    洞_id.append(["",""])  # 當洞數為 0 時，直接添加空值
                            if not self.check_machine:
                                item_說明 = ''
                            # print(f'{ii} {item_name}')
                            self.itemss.append({
                                    'list_id': ii,
                                    'type': typelisst[types-4],
                                    'refine': 精煉,
                                    'name': item_name,
                                    'id': item,
                                    'suffix_ID1': suffix_ID[0],
                                    'suffix_ID2': suffix_ID[1],
                                    'suffix_ID3': suffix_ID[2],
                                    'suffix_ID4': suffix_ID[3],
                                    'suffix_ID5': suffix_ID[4],
                                    'suffix_veal11': suffix_veal1[0],
                                    'suffix_veal12': suffix_veal1[1],
                                    'suffix_veal13': suffix_veal1[2],
                                    'suffix_veal14': suffix_veal1[3],
                                    'suffix_veal15': suffix_veal1[4],
                                    'suffix_veal21': suffix_veal2[0],
                                    'suffix_veal22': suffix_veal2[1],
                                    'suffix_veal23': suffix_veal2[2],
                                    'suffix_veal24': suffix_veal2[3],
                                    'suffix_veal25': suffix_veal2[4],
                                    'suffix_name1': suffix_name[0],
                                    'suffix_name2': suffix_name[1],
                                    'suffix_name3': suffix_name[2],
                                    'suffix_name4': suffix_name[3],
                                    'suffix_name5': suffix_name[4],
                                    'description': item_說明,
                                    's_id1': 洞槽[0],
                                    's_id2': 洞槽[1],
                                    's_id3': 洞槽[2],
                                    's_id4': 洞槽[3],
                                    's_name1': 洞_id[0][0],
                                    's_name2': 洞_id[1][0],
                                    's_name3': 洞_id[2][0],
                                    's_name4': 洞_id[3][0],
                                    's_scripts1': 洞_id[0][1],
                                    's_scripts2': 洞_id[1][1],
                                    's_scripts3': 洞_id[2][1],
                                    's_scripts4': 洞_id[3][1]
                            })
                self.refresh()
        else:
            messagebox.showerror('錯誤','窗口已關閉請重新設定窗口!')
    def search(self,evt):
        """
        搜尋按鈕
        """
        print("<Button-1>事件未處理:",evt)
        self.search_data()
    def research(self,evt=''):
        """
        自動遍歷
        """
        print("<Button-1>事件未處理:",evt)
        if evt:
            checked = not bool(self.ui.tk_check_button_m2xrfg6x.get()) 
        else:
            checked = bool(self.ui.tk_check_button_m2xrfg6x.get()) 
        if checked:  # 检查复选框是否被选中
            print(checked)
            self.search_data()
            self.ui.after(1000, self.research)  # 每5秒再次调用 start_timer
    def outputJson(self, evt):
        """
        輸出json
        """
        selected_type = self.ui.tk_select_box_m2w2v0f5.get()
        if selected_type != '露天':
            print("<Button-1>事件未處理:", evt)
            # 检查 JSON 文件是否存在
            json_file_path = self.current_dir + r'\data.json'
            # 如果文件不存在，创建一个新的 JSON 文件
            if not path.exists(json_file_path):
                # 创建一个初始的空字典结构
                initial_data = {
                    "個人": {},
                    "個人倉庫": {},
                    "武器倉庫": {},
                    "防具倉庫": {},
                    "時裝倉庫": {},
                    "卡片倉庫": {},
                    "影裝倉庫": {},
                    "Guild Storage":{}
                }
                # 将初始数据写入 JSON 文件
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    dump(initial_data, f, ensure_ascii=False, indent=4)
                print("創建新的 JSON 檔案：data.json")
            if self.itemss :
                search_value = self.ui.tk_input_m2w3agz9.get() # 搜尋詞墜編號
                list1 = [int(x) for x in search_value.split(",") if x.strip().isdigit()]  # 轉換成整數列表
                list1 = [0] if not list1 else list1
                refine_value = int(self.ui.tk_input_m2w3d4ce.get() or 0) # 精煉值 表示如果 get() 的結果為空字符串或 None，將返回 0
                suffix_veal2 = int(self.ui.tk_input_m2w3ivoe.get() or 0) # 強化值 表示如果 get() 的結果為空字符串或 None，將返回 0
                
                # 匹配
                self.itemss2 = [
                    val for val in self.itemss 
                    if any(suffix in [val['suffix_ID1'], val['suffix_ID2'], val['suffix_ID3'], val['suffix_ID4'], val['suffix_ID5']] for suffix in list1)
                    and val['refine'] >= refine_value
                    and any(veal2 >= suffix_veal2 for veal2 in [val['suffix_veal21'], val['suffix_veal22'], val['suffix_veal23'], val['suffix_veal24'], val['suffix_veal25']])
                ]
                # 读取 JSON 文件
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data = load(f)
                # 更新 "倉庫" 的内容
                if selected_type == "倉庫":
                    data[self.倉庫名稱] = self.itemss2 if self.itemss2 else []  # 直接赋值给字典
                    print(self.倉庫名稱)
                elif selected_type == "個人":
                    data["個人"] = self.itemss2 if self.itemss2 else []  # 直接赋值给字典
                # 将更新后的数据写回 JSON 文件
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    dump(data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo('^_^y運行成功','成功保存檔案data.json')
                print("成功更新倉庫內容！")
        else:
            messagebox.showerror('錯誤','露天無法保存!')
    def refresh(self,evt=''):
        """
        更新清單
        """
        print("<Button-1>事件未處理:",evt)
        if self.itemss :
            search_value = self.ui.tk_input_m2w3agz9.get() # 搜尋詞墜編號
            list1 = [int(x) for x in search_value.split(",") if x.strip().isdigit()]  # 轉換成整數列表
            list1 = [0] if not list1 else list1
            refine_value = int(self.ui.tk_input_m2w3d4ce.get() or 0) # 精煉值 表示如果 get() 的結果為空字符串或 None，將返回 0
            suffix_veal2 = int(self.ui.tk_input_m2w3ivoe.get() or 0) # 強化值 表示如果 get() 的結果為空字符串或 None，將返回 0
            # print(f'list1 {list1} refine_value {self.ui.tk_input_m2w3d4ce.get()}')
            
            # 刷新
            for row in self.ui.tk_table_m2w3rgpm.get_children():
                self.ui.tk_table_m2w3rgpm.delete(row)
            # 匹配
            for val in self.itemss:
                # print(f'\n{valuess}')
                suffix_匹配 = True if list1 == [0] else any(suffix in [val['suffix_ID1'], val['suffix_ID2'], val['suffix_ID3'], val['suffix_ID4'], val['suffix_ID5']] for suffix in list1)
                refine_匹配 = True if val['refine'] >= refine_value else False
                suffix2_匹配 = any(veal2 >= suffix_veal2 for veal2 in [val['suffix_veal21'], val['suffix_veal22'], val['suffix_veal23'], val['suffix_veal24'], val['suffix_veal25']])
                
                # print(f'val[name] {val["name"]} suffix_匹配 {suffix_匹配} refine_匹配{refine_匹配} suffix_veal2_匹配 {suffix2_匹配}')
                if suffix_匹配 and refine_匹配 and suffix2_匹配:
                    suffixlist = self.自動換行(  self.generate_string2(val['suffix_name1'],val['suffix_veal11'],val['suffix_veal21']), 
                                                self.generate_string2(val['suffix_name2'],val['suffix_veal12'],val['suffix_veal22']),
                                                self.generate_string2(val['suffix_name3'],val['suffix_veal13'],val['suffix_veal23']),
                                                self.generate_string2(val['suffix_name4'],val['suffix_veal14'],val['suffix_veal24']),
                                                self.generate_string2(val['suffix_name5'],val['suffix_veal15'],val['suffix_veal25']))
                    slist = self.自動換行(val['s_name1'], val['s_name2'], val['s_name3'], val['s_name4'])
                    lists = [val['list_id'],val['refine'],val['id'],val['name'],suffixlist,slist]
                    # print(val['list_id'],val['name'])
                    self.insert_to_table( val['list_id'], lists)
    def hwnd_binding(self,evt):
        """
        綁定窗口
        """
        print("<Button-1>事件未處理:",evt)
        self.window_id = win32gui.FindWindow('Fairy_RO', None) # 窗口 類名, 標題
        if not self.window_id:
            messagebox.showerror('錯誤','找不到遊戲窗口請重新嘗試!')
        else:
            self.process_handle, self.temp_link = self.get_process_handle_from_hwnd(self.window_id) # 打開進程 進程,路徑
            char_name = self.read_string("01572430" )
            star = "授權版" if self.ctl.check_machine else "免費版"
            self.ui.title(f'裝備管理工具 目前尋找 {char_name} 的倉庫 - {star}')
    def write_iteminfo(self,evt):
        """
        修改iteminfo_true.lub
        """
        print("<Button-1>事件未處理:",evt)
        write_iteminfo = None
        input_file = self.temp_link+r'\system\itemInfo_true.lub'
        pattern = r", DESC.identifiedDisplayName,"  # 匹配模式
        # 使用临时文件保存修改内容
        output_file = input_file + ".tmp"  # 创建一个临时文件
        with open(input_file, 'r', encoding='ANSI', errors='replace') as f_in, \
            open(output_file, 'w', encoding='ANSI', errors='replace') as f_out:
            for line in f_in:
                # 判断是否符合匹配模式
                if re.search(pattern, line):
                    # 进行替换，将 identifiedDisplayName 后面加上 ItemID
                    modified_line = line.replace(", DESC.identifiedDisplayName,", ', DESC.identifiedDisplayName .. "(" .. ItemID ..")",')
                    f_out.write(modified_line)
                    write_iteminfo = 1
                else:
                    # 直接写入未修改的行
                    f_out.write(line)
        self.ui.tk_button_m212ba1e.config(state='normal')  # 禁用按钮
        if write_iteminfo:
            # 覆盖原始文件
            os.replace(output_file, input_file)
            ret = messagebox.showinfo('^_^y運行成功','修改成功 iteminfo_true.lub 顯示ID')
            print('ret:{}'.format(ret))
        # else:
        #     ret = messagebox.showerror('錯誤','修改失敗或已經修改完成,請在遊戲確認物品名稱!')
    def update_button_text(self, *args):
        """
        修改按鈕名稱
        """
        # 根据选择的类型更新按钮文本
        selected_type = self.ui.tk_select_box_m2w2v0f5.get()
        if selected_type == "倉庫":
            self.ui.tk_button_m2w31jpw.config(text="遍歷倉庫")
        elif selected_type == "個人":
            self.ui.tk_button_m2w31jpw.config(text="遍歷個人")
        elif selected_type == "露天":
            self.ui.tk_button_m2w31jpw.config(text="遍歷露天")
        else:
            self.ui.tk_button_m2w31jpw.config(text="遍歷")  # 默认文本
    def equipment(self,evt):
        """
        重複裝備
        """
        print("<Button-1>事件未處理:",evt)
        item_count = defaultdict(int)
        # 計算每個 id 的數量
        if self.itemss:
            for val in self.itemss:
                item_count[val['id']] += 1

            new_item_info = {}
            for item_id, count in item_count.items():
                # 假設我們要將其他值與數量一起存儲，例如 item 名稱
                item_name = next((val['name'] for val in self.itemss if val['id'] == item_id), None)
                new_item_info[item_id] = {'count': count, 'name': item_name}
            # 刷新
            for row in self.ui.tk_table_m2w3rgpm.get_children():
                self.ui.tk_table_m2w3rgpm.delete(row)
            # 輸出每個項目的 id、數量和名稱
            i = 0
            for item_id, info in new_item_info.items():
                if info['count'] > 1:
                    i += 1
                    self.insert_to_table( val['list_id'], [i,0,item_id,info['name'],'裝備重複數量: '+str(info['count']),""])
    def on_double_click(self, evt):
        """
        複製內容
        """
        print("<Button-1>事件未處理:",evt)
        # 獲取選中的行
        if self.check_machine :
            selected_item = self.ui.tk_table_m2w3rgpm.selection()
            if selected_item:
                type = self.ui.tk_select_box_m2mfv0f5.get()
                # 獲取行內容
                item_values = self.ui.tk_table_m2w3rgpm.item(selected_item, 'values')
                # 假設列順序是 "排序", "精煉", "ID", "名稱", "卡槽", "詞綴"
                # 剃除「排序」值，添加「+」到「精煉」值
                refined_value = f"+{item_values[1]}"  # 獲取「精煉」值並添加「+」
                if type == "全部":
                    filtered_values = [refined_value] + list(item_values[2:])  # 組合「精煉」值和後面的值
                    filtered_values = "\t".join(filtered_values)
                elif type == "ID":
                    filtered_values = item_values[2]
                elif type == "名稱":
                    filtered_values = item_values[3]
                elif type == "詞墜":
                    filtered_values = item_values[4]
                elif type == "卡槽":
                    filtered_values = item_values[5]
                # 在每個值前不添加 "+"，只添加到「精煉」值
                print("複製的內容:", filtered_values)  # 這裡可以替換為複製到剪貼板的邏輯
                # 複製到剪貼板（可選）
                self.ui.clipboard_clear()  # 清空剪貼板
                self.ui.clipboard_append(filtered_values)  # 追加內容到剪貼板abxdd
