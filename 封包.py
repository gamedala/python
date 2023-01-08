import socket

from struct import * #struct模块用来自定义封包格式!如发送'7061636b6574'等...

#'7061636b6574'.decode('hex')得出"packet"    'packet'.encode('hex')得出'7061636b6574'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('114.33.114.145',5121))

packet=pack("6B",0x33,0x12,0,0,0,0x01)

s.send(packet)

#这样就发送了一个封包,用WPE截来看是这样的:33 12 00 00 00 01 61 62 63

#pack()用来构造封包的结构,后面可加字符串等...0x33是代表以十六进制格式发,不可直接写成33

#当然这样乱发封包,google服务器是不会有响应的.

s.close() #关闭连接
