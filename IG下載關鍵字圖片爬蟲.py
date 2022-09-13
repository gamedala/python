#調用 selenium webdriver
from selenium import webdriver
#應用 selenium Keys
#from selenium.webdriver.common.keys import Keys
#應用 selenium By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#調用 time
import time
import os
import wget
#設定關鍵字
keyword = "#game"
#開啟 chromedriver
PATH = "C:/Users/BOB/Desktop/pytjon爬蟲/chromedriver.exe"
driver = webdriver.Chrome(PATH)
#開啟網址
driver.get("https://www.instagram.com/")
time.sleep(1)
#取得登入
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)
login = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button')
#清除
username.clear()
password.clear()
#輸入帳號密碼
username.send_keys("")
password.send_keys("")
#點擊登入
login.click()
time.sleep(3)
#轉跳頁面
driver.get("https://www.instagram.com/explore/")
time.sleep(3)
#取得搜尋
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/input"))
)
#輸入搜尋關鍵字
search.send_keys("#game")
time.sleep(1)
search.send_keys(Keys.RETURN)
time.sleep(1)
search.send_keys(Keys.RETURN)
time.sleep(3)
#取得照片連結
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "_aagt"))
)
#向下滾動
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
#取得照片連結
imgs = driver.find_elements(By.CLASS_NAME, "_aagt")
#設定路徑
path = os.path.join(keyword)
os.mkdir(path)

count = 0
for img in imgs:
    #存檔名稱 keyword+編號.jpg
    save_as = os.path.join(path, keyword+str(count)+'.jpg')
    #取得元素SRC
    src = img.get_attribute('src')
    #下載檔案
    wget.download(src,save_as)
    #顯示下載SRC
    print(src)
    count += 1
time.sleep(10)