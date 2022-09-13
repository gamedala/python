from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
user = ""
passwords= ""
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
username.send_keys(user)
password.send_keys(passwords)
#點擊登入
login.click()
time.sleep(3)
#轉跳追蹤網址
driver.get("https://www.instagram.com/explore/people/")
time.sleep(5)
#獲取追蹤button
follows = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[2]/div/div/div[*]/div[3]/button')
print(follows)
for follow in follows:
    follow.click()
    time.sleep(random.randint(1,3))
