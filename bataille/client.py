#!/usr/bin/python3
from game import *
import socket
import select
import  random
import time
#from collections import namedtuple

def clientConnect(servername, port) :

    client = socket.create_connection((servername, port))
    
    print(client)

    clientGame(client);


def clientGame(client) :
    while True:
        data = client.recv(2048)
        if len(data) == 0 :
            client.close()
            break;
        elif data.endswith(b'? ') :
            #print("Waiting for response")
            response = input(data.decode("utf-8"))
            client.send(response.encode("utf-8"))
        else:
            print(data.decode("utf-8"))
    return

def clientObserve(client) :
    return

#clientConnect('localhost', 7777)
