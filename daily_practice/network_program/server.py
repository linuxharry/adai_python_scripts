#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, time
from threading import Thread


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 9999))
s.listen(5)
print('Waiting for connection...')


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcom!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed!' % addr)


while True:
    sock, addr = s.accept()
    t = Thread(target=tcplink, args=(sock, addr))
    t.start()


