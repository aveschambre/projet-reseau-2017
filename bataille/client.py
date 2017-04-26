#!/usr/bin/python3
from game import *
import socket
import select
import  random
import time
from collections import namedtuple

def clientConnect(servername, port) :

    client = socket.create_connection((servername, port))
    print(client)

    clientGame(client);


def clientGame(client) :
    while True:
        data = client.recv(1024)
        if data == 0 :
            client_socket.close()
            break;
        else:
            print ("RECIEVED:" , data)
            response = input(prompt=data)
            client.send(response)
    return

def clientObserve(client) :
    return

clientConnect('localhost', 7777)
