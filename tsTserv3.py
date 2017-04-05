"""
 Charlie Ang
 CSC 4800 Python Applications Programming
 Lab # 5
 Dr. Tindall
 February 6, 2017
 TCP ServeR
"""

#!/usr/bin/env python

from socket import *
from time import ctime
import os
import sys
import time

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)  #DATA RECEIVED FROM CLIENT
        if not data:
            break

        splitLine = data.split(maxsplit=1)      #split user input into two
        numArgs = 0                             #variable to keep track of number of args entered
        for w in splitLine:
            numArgs = numArgs + 1

        #2
        if (splitLine[0].decode('utf-8')) == 'date':
            tcpCliSock.send(bytes('%s: %s' % ('date', ctime()), 'utf-8'))
        #3
        elif (splitLine[0].decode('utf-8')) == 'os':
            tcpCliSock.send(bytes('%s: %s' % ('os', os.name), 'utf-8'))
        #1
        elif (splitLine[0].decode('utf-8')) == 'EXITSERVER':
            tcpCliSock.close()      #terminate client connection
            tcpSerSock.close()      #close server socket
            sys.exit(0)             #terminate server
        #4
        elif (splitLine[0].decode('utf-8')) == 'ls':
            #ls with no path defaults to current directory...only one arg
            if numArgs == 1:
                tcpCliSock.send(bytes('%s (%s)' % ('ls "path":', os.listdir(os.curdir)), 'utf-8'))
            if numArgs == 2:
                # ls with specified directory listing
                try:
                    #os.chdir(splitLine[1].decode('utf-8'))
                    tcpCliSock.send(bytes('%s (%s)' % ('ls "path":', os.listdir(splitLine[1])), 'utf-8'))
                except FileNotFoundError:
                    tcpCliSock.send(bytes('%s' % ('No such file or directory'), 'utf-8'))
                except PermissionError:
                    tcpCliSock.send(bytes('%s' % ('Permission Error: You do not have read permissions'), 'utf-8'))
        #5
        elif (splitLine[0].decode('utf-8')) == 'sleep':
            #sleep with no second argument defaults to 5 seconds
            if numArgs == 1:
                time.sleep(5)
                tcpCliSock.send(bytes("Slept for 5 seconds", 'utf-8'))
            if numArgs == 2:
                #server sleeps for specified number of seconds
                try:
                    time.sleep(float(splitLine[1]))
                    tcpCliSock.send(bytes("Slept for %d seconds" % float(splitLine[1]), 'utf-8'))
                except ValueError:
                    #sleep for 5 seconds if invalid sleep
                    #tcpCliSock.send(bytes('%s' % ('Please enter a number for the number of seconds'), 'utf-8'))
                    time.sleep(5)
                    tcpCliSock.send(bytes("Slept for 5 seconds", 'utf-8'))
            if numArgs >= 3:
                #sleep for 5 seconds if invalid sleep
                time.sleep(5)
                tcpCliSock.send(bytes("Slept for 5 seconds", 'utf-8'))
        # 6
        else:
            #tcpCliSock.send('[%s] %s' % (bytes(ctime(), 'utf-8'), data))
            tcpCliSock.send(bytes('[%s] %s' % (ctime(), data.decode('utf-8')), 'utf-8'))

    tcpCliSock.close()
tcpSerSock.close()
