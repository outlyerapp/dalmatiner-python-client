#!/usr/bin/env python
import socket
import binascii

TCP_IP = '127.0.0.1'
TCP_PORT = 5555
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    try:
        conn, addr = s.accept()
        packet = conn.recv(BUFFER_SIZE)
        if not packet:
            continue
        print "received data:", binascii.hexlify(packet)
        conn.send("hello")
    except Exception as e:
        print e
        break

s.close()
