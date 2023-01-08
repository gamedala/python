import win32com.client
import time
dm = win32com.client.Dispatch('dm.dmsoft')

print('插件版本:'+dm.ver()) # 顯是插件版本
base_path = dm.GetBasePath() + '愛如初見' # 取得插件路徑
dm_ret = dm.SetPath(base_path) # 設定全局路徑
print('路徑:' + base_path + ' 返回:'+ str(dm_ret)) # dm_ret類型轉換str