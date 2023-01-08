#調用 selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#調用 time
import time,os,wget
user = "gamedola3"
passwords= "Tdemcodie2"
#設定關鍵字
keyword = "#game"
#開啟 chromedriver
PATH = Service(r"C:/Users/BOB/Desktop/python/chromedriver.exe")
driver = webdriver.Chrome(service = PATH)
#開啟網址
driver.get("https://www.instagram.com/")
#取得登入
#尋找 持續 10秒直到找到元素
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)
login = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div')
#清除
username.clear()
password.clear()
#輸入帳號密碼
username.send_keys(user)
password.send_keys(passwords)
#點擊登入
login.click()
time.sleep(5)
#轉跳頁面
driver.get("https://www.instagram.com/explore/")
time.sleep(3)
#取得搜尋
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/input"))
)
#輸入搜尋關鍵字
search.send_keys(keyword)
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