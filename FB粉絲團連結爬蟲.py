#調用 selenium webdriver
from selenium import webdriver
#應用 selenium Keys
#from selenium.webdriver.common.keys import Keys
#應用 selenium By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#調用 time
import time
#開啟 chromedriver
s = Service(r"C:/Users/BOB/Desktop/python/chromedriver.exe")
driver = webdriver.Chrome(service = s)
#開啟網址
driver.get("https://www.facebook.com/")
#取得登入
email = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "email"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "pass"))
)
login = driver.find_element(By.XPATH, '//*[@name="login"]')
#清除
email.clear()
password.clear()
#輸入帳號密碼
email.send_keys("")
password.send_keys("")
#點擊登入
login.click()
#轉跳頁面
driver.get("https://m.facebook.com/groups_browse/your_groups")
#延遲
time.sleep(2)
#titles = driver.find_elements(By.CLASS_NAME, "_7hkg")
#取得粉絲團連結
titles = driver.find_elements(By.XPATH, '//*[@id="root"]/div[1]/div/div/div[2]/div/div[2]/div[*]/a')
#迴圈 titles
for title in titles:
#取得 title 'href' = url
    url = title.get_attribute('href')
#url不等於空白 輸出文本
    if url != "":
        print(url)
time.sleep(10)