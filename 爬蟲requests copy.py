import requests,logging
from bs4 import BeautifulSoup
logging.captureWarnings(True)
title = ['IRB/REC案號','計畫主持人','','']
login_url="https://vghtc.cims.tw/wiPtms/index.jsp"
home_url="https://vghtc.cims.tw/wiPtms/newHome.do?ctab=all&mode=notag&debug=AU"
payload={
    "user":"U578",
    "domain":"duty821028"
}
#構造Session
#在session中傳送登入請求，此後這個session裡就儲存了cookie
#可以用print(session.cookies.get_dict())檢視
session = requests.Session()
print('開始登入頁面:'+login_url)
登入狀態 = session.post(login_url, params=payload, timeout=5, verify=False)
if 登入狀態.status_code == 200:
    print('登入完成開始獲取頁面資料:'+home_url)
    web = session.get(home_url, timeout=5, verify=False)
    soup = BeautifulSoup(web.text, "html.parser") # 指定 lxml 作為解析器
    # print(soup.prettify())
    titles = soup.find_all('td',class_="listCell")
    print(titles)
    for title in titles:
        print(title.select_one("th").getText())
else:
    print('登入失敗')