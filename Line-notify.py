import requests
path = "C:/dm"
token = 'Z8NSmX4Tpz3kxW7is09KF0wVWWPUQTpLOW2hxLmKAn9'
def Notify(message,img):
    headers = { "Authorization": "Bearer " + token }
    data = { 'message': message }
    #img_path = Path(r''+self.path+'/'+img)
    image = open(r''+path+'/'+img, 'rb')
    print(image)
    files = { 'imageFile': image }
    msg=requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data, files = files)
    print(msg)


Notify("123","未命名aaa.png")