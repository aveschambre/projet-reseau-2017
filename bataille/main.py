#!/usr/bin/python3

from game import *
import  random
import time



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
            l = str(y)
            if y < 10:
                l = l + " "
        for x in range(1,WIDTH+1):
            l = l + str(Matrix[x][y]) + " "
        print(l)

""" display the game viewer by the player"""
def displayGame(game, player, ):
    otherPlayer = (player+1)%2
    displayConfiguration(game.boats[player], game.shots[otherPlayer], showBoats=True)
    displayConfiguration([], game.shots[player], showBoats=False)


""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)

def main():

    boats1 = randomConfiguration()
    boats2 = randomConfiguration()
    game = Game(boats1, boats2)
    displayGame(game, 0)
    print("======================")


""" Find Clients (2)
    start game
    (how to avoid disconnections ?)
    while game
        for players
            message player
            validate input
            make move
            send game state to players
        check game over

fonction de changer -
    displayGame
    main

"""

    currentPlayer = 0
    displayGame(game, currentPlayer)
    while gameOver(game) == -1:
        print("======================")
        if currentPlayer == J0:
            x_char = input ("quelle colonne ? ")
            x_char.capitalize()
            x = ord(x_char)-ord("A")+1
            y = int(input ("quelle ligne ? "))
        else:
            (x,y) = randomNewShot(game.shots[currentPlayer])
            time.sleep(1)
        addShot(game, x, y, currentPlayer)
        displayGame(game, 0)
        currentPlayer = (currentPlayer+1)%2
    print("game over")
    print("your grid :")
    displayGame(game, J0)
    print("the other grid :")
    displayGame(game, J1)

    if gameOver(game) == J0:
        print("You win !")
    else:
        print("you loose !")

main()
