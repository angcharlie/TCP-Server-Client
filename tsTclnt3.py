"""
 Charlie Ang
 CSC 4800 Python Applications Programming
 Lab # 5
 Dr. Tindall
 February 6, 2017
 TCP Client
"""

#!/usr/bin/env python

from socket import *
import sys

HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    tcpCliSock.send(bytes(data, 'utf-8'))

    #1 after sending 'exitserver' message to the server
    if data == 'EXITSERVER':
        tcpCliSock.close()      #close client socket
        sys.exit(0)             #terminate client

    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))

tcpCliSock.close()
