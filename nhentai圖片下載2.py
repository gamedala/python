import _thread
#調用 time
import time
import os,wget
from urllib import request
url = "https://gitee.com/rootentertainment/a-star-map-editor/blob/master/v5.2/A-star/resource/" # 開啟網址
Type = ("clear.png","end.png","erase.png","logo.ico","logo.png","profile.jpg","start.png","wall.png") # 開啟網址
keyword = "resource" # 設定關鍵字
#PATH = "C:/Users/BOB/Desktop/python/chromedriver.exe" # 開啟 chromedriver
#driver = webdriver.Chrome(PATH)
#設定路徑
path = os.path.join(keyword)
os.mkdir(path)

class Operation:
    def __init__(self, src,save_as):
        print(src) # 顯示下載SRC
        wget.download(src,save_as) # 下載檔案
        #request.urlretrieve(src, save_as)
    
def main():
    Down = Operation
    for i in Type:
        save_as = os.path.join(path, keyword+str(i)) # 存檔名稱 keyword+編號.jpg
        Down( url+str(i), save_as)

if __name__ == "__main__":
    main()
