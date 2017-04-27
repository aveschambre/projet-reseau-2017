#!/usr/bin/python3
from game import *
from utils import *
import socket
import select
import  random
import time
from collections import namedtuple
import sys

import client

MAX_CONNECTS = 3
SERVER_NAME = '127.0.0.1'
PORT = 7777
Player = namedtuple("Player", "socket addr num")

""" generate a random valid configuration """
def randomConfiguration():
    boats = [];
    while not isValidConfiguration(boats):
        boats=[]
        for i in range(5):
            x = random.randint(1,10)
            y = random.randint(1,10)
            isHorizontal = random.randint(0,1) == 0
            boats = boats + [Boat(x,y,LENGTHS_REQUIRED[i],isHorizontal)]
    return boats



def displayConfiguration(boats, shots=[], showBoats=True):
    Matrix = [[" " for x in range(WIDTH+1)] for y in range(WIDTH+1)]
    for i  in range(1,WIDTH+1):
        Matrix[i][0] = chr(ord("A")+i-1)
        Matrix[0][i] = i

    if showBoats:
        for i in range(NB_BOATS):
            b = boats[i]
            (w,h) = boat2rec(b)
            for dx in range(w):
                for dy in range(h):
                    Matrix[b.x+dx][b.y+dy] = str(i)

    for (x,y,stike) in shots:
        if stike:
            Matrix[x][y] = "X"
        else:
            Matrix[x][y] = "O"


    for y in range(0, WIDTH+1):
        if y == 0:
            l = "  "
        else:
            l += "\n"
            l += str(y)
            if y < 10:
                l = l + " "
        for x in range(1,WIDTH+1):
            l = l + str(Matrix[x][y]) + " "
    l += "\n"
    return l

""" display the game viewer by the player"""
def displayGame(game, players, currentPlayer):
    #players = [addr, socket, 0; ...], currentPlayer = [0,1]
    otherPlayer = (currentPlayer+1)%2
    display1 = displayConfiguration(game.boats[currentPlayer], game.shots[otherPlayer], showBoats=True)
    display2 = displayConfiguration([], game.shots[otherPlayer], showBoats=False)
    sendMessage(players[currentPlayer], "Your Game:\n" + display1 + "\n")
    sendMessage(players[otherPlayer], "Your Shots:\n" + display2 + "\n")


def broadcastGame(game, observers):
    display1 = displayConfiguration(game.boats[0], game.shots[1], showBoats=True)
    display2 = displayConfiguration(game.boats[1], game.shots[0], showBoats=True)
    for observer in observers:
        sendMessage(observer, "Player 1's Game:\n" + display1 + "\n")
        sendMessage(observer, "Player 2's Game:\n" + display2 + "\n")


def sendMessage(player, mesg):
    #print(player)
    player.socket.send(mesg.encode('utf-8'))

""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)

def startGame(players) :
    boats1 = randomConfiguration()
    boats2 = randomConfiguration()
    game = Game(boats1, boats2)
    displayGame(game, players, 0)
    displayGame(game, players, 1)
    print("======================")
    return game

def waitMessage(player, players) :
    while True :
        message = player.socket.recv(2048)
        if len(message) == 0 :
            #Add code for monitor closing sockets
            #players[x].socket.close()
            #players.remove(player)
            return None
        return message.splitlines()


def main():


    if(len(sys.argv) > 1) :
        print("I am client")
        client.clientConnect(sys.argv[1], PORT)
        return

    #else I am Server, let's play the game.
    print("I am server")
    #make sockets
    sock = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))
    print(sock.getsockname())
    sock.listen(1)

    #sock = createServerSocket()
    connects = [sock]
    players = []

    print("Waiting for clients")

    #wait for clients
    while True :
        (socks,_,_) = select.select(connects, [], [])
        for x in range(0, len(socks), 1) :
            if (socks[x] == sock) & (len(connects) < 3) :
                print("New Player!")
                acpt, addr = sock.accept()
                player = Player(socket=acpt, addr = addr, num=len(socks)-1)
                connects.append(player.socket);
                players.append(player)
        if (len(connects) >= MAX_CONNECTS) :
            print("No new players :(")
            break;

    game = startGame(players)

    currPlayer = 0
    while gameOver(game) == -1:
        #print("======================") #>>>> utils shot validation
        print("currentPlayer = ", currPlayer)
        sendMessage(players[currPlayer], "quelle colonne ?")
        x_char = waitMessage(players[currPlayer], connects)
        if x_char != None :
            x = xStandardization(x_char)
            sendMessage(players[currPlayer], "quelle ligne ?")
            y = waitMessage(players[currPlayer], connects)
            if y != None :
                y = yStandardization(y)
            else:
                break; #handle client disconnect
        else:
            break; #handle handle client disconnect

        #(x,y) = randomNewShot(game.shots[currentPlayer])
        #time.sleep(1)
        addShot(game, x, y, currPlayer)
        #Select here for awaiting connections and add them
        #this also allows us to validate that the players are still here
        observers = []
        print("observer check")
        print(connects)
        (socks,_,_) = select.select(connects, [], [], 0)
        print(socks)
        for x in range(0, len(socks), 1) :
            if (socks[x] == sock) :
                print("New Observer!")
                acpt, addr = sock.accept()
                obsvr = Player(socket=acpt, addr = addr, num=len(socks)-1)
                observers.append(obsvr)
                connects.append(obsvr.socket)
            else:
                message = socks[x].recv(2048)
                if len(message) == 0 :
                    socks[x].close()
                    connects.remove(socks[x])
                    if socks[x] in players :
                        break #handle reconnections

        print("After Observers")
        displayGame(game, players, currPlayer)
        broadcastGame(game, observers);
        currPlayer = (currPlayer+1)%2


    (socks,_,_) = select.select(connects, [], [])
    for i in range(0, len(socks), 1):
        if (socks[i] != sock) :

            print("game over")
            broadcastGame(game, observers)
            broadcastGame(players)

    if gameOver(game) == J0:
        print("You win !")
    else:
        print("you loose !")

main()
