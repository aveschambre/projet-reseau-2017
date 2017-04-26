#!/usr/bin/python3
from game import *
import socket
import select
import  random
import time
from collections import namedtuple

def clientConnect(servername, port) :

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = client.create_connection((servername, port))
    print(sock)

    clientGame(client);

# while 1:
#     data = client_socket.recv(512)
#     if ( data == 'q' or data == 'Q'):
#         client_socket.close()
#         break;
#     else:
#         print "RECIEVED:" , data
#         data = raw_input ( "SEND( TYPE q or Q to Quit):" )
#         if (data <> 'Q' and data <> 'q'):
#             client_socket.send(data)
#         else:
#             client_socket.send(data)
#             client_socket.close()
#             break;

def clientGame(client) :
    return

def clientObserve(client) :
    return

clientConnect('localhost', 7777)
