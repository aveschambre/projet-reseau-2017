import  random 


WIDTH = 10 # width of the grid

NB_BOATS = 5 # nb boats in the game
LENGTHS_REQUIRED =[2,3,3,4,5] # list of size of different boats
LENGTH_CARDINALITIES_REQUIRED = [0,0,1,2,1,1] # number of boats of different sizes
TOTAL_LENGTH = 17 #sum of boat sizes

J0 = 0 #Player 0
J1 = 1 #Player 1

""" position and size of a boat """
class Boat:
    def __init__(self, x = 1,y = 1, length = 1, isHorizontal=True):
        self.x = x
        self.y = y
        self.length = length
        self.isHorizontal = isHorizontal


""" State of a game. It is given by the position of the boats of each players and
the list of shots made by each player."""
class Game:
    shots = [[],[]] #shots of each players. A shot is a triple (x,y, strike),
      # where strike is True if there is an opponent boat at (x,y)
    def __init__(self, boats1, boats2):
        self.boats = [boats1, boats2]

""" Play a shot by the player. Return True if this shot strike a a boat, False if not and None
   if this shot has already been played by the player."""
def addShot(game, x,y, player):
    otherPlayer = (player+1)%2
    if not isANewShot(x,y, game.shots[player]):
        return
    game.shots[player].append((x,y, isAStrike(game.boats[otherPlayer], x, y)))
    return isAStrike(game.boats[otherPlayer], x, y)


""" Return the state of the game: -1 if the game is not over,
    J0 if player J0 wins and J1 if player J1 wins.  """
def gameOver(game):
    for player in range(2):
        nbStrikes = 0
        for (x,y,strike) in game.shots[player]:
            if strike:
                nbStrikes += 1
        print(player, nbStrikes)    
        if nbStrikes == 17: 
            return player
    return -1;




""" check if a list of boat is valid : has the appropriate length and sizes, fit in the grid and do not overlap """
def isValidConfiguration(boats):
    if len(boats) != 5:
        return False
    lengthCardinalities=[0,0,0,0,0,0]
    for b in boats:
        (w,h) = boat2rec(b)
        if b.length<2 or b.length>5:
            return False
        if b.x<1 or b.y <1:
            return False
        if (b.x+ w> WIDTH) or (b.y+h> WIDTH):
            return False
        lengthCardinalities[b.length] += 1
    if lengthCardinalities != LENGTH_CARDINALITIES_REQUIRED:
        return False
    for i in range(5):
        for j in range(i):
            b1 = boats[i]
            b2 = boats[j]
            if intersect(b1,b2):
                return False
    return True


#########################################

""" return the width and height of a boat """
def boat2rec(b):
    if b.isHorizontal:
        return (b.length, 1)
    else:
        return (1, b.length)
    
""" check if 2 boats overlap """
def intersect(b1, b2):  
    (w1,h1) = boat2rec(b1)
    (w2,h2) = boat2rec(b2)
    h_inter = (b1.x <=b2.x and b2.x < b1.x + w1) or \
        (b2.x <=b1.x and b1.x < b2.x + w2);
    v_inter = (b1.y <=b2.y and b2.y < b1.y + h1) or \
        (b2.y <=b1.y and b1.y < b2.y + h2);
    return h_inter and v_inter;

def isAStrike(boats, x, y):
    for b in boats:
        (w,h) = boat2rec(b)
        if b.x <=x and x <b.x+w and b.y <= y and y < b.y+h:
            return True
    return False

def isANewShot(x,y, shots):
    for (xx,yy,s) in shots:
        if (xx,yy) == (x,y):
            return False
    return True



