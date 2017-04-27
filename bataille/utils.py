import socket
import select
from collections import namedtuple


Player = namedtuple("Player", "socket addr num")


def xStandardization(input):
	if input != None :
		if len(input[0]) > 1:
			first = input[0]
			first = first[:1]
			output = ord(first.upper())-ord("A")+1
			return output
		return ord(input[0].upper())-ord("A")+1

def yStandardization(input):
	if input != None :
		try:
			ret = int(input[0])
			return ret
		except ValueError:
			return -1
	else :
		return -1

#other validations ?

#player
def waitClientReconnect(players, connects, observers) :
    while True :
        (socks,_,_) = select.select(connects, [], [])
        for x in range(0, len(socks), 1) :
            if (socks[x] == connects[0]) :
                acpt, addr = connects[0].accept()
                for play in players :
                    print(addr, " ", play.addr)
                    if addr[0] == play.addr[0] :
                        print("Player Reconnect!")
                        playerReconn = Player(socket=acpt, addr = addr, num=play.num)
                        players[players.index(play)] = playerReconn
                        return

                #Someone else wants to watch the game? OK
                print("New Observer!")
                observer = Player(socket=acpt, addr = addr, num=len(connects))
                connects.append(observer.socket)
                observers.append(observer)

            else :
                print("help")
                message = socks[x].recv(2048)
                if len(message) == 0 :
                    socks[x].close()
                    connects.remove(socks[x])
                    print("Removing Connection")

def createServerSocket() :
    HOST = None
    PORT = 7777
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):

        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
            try:
                s.bind(sa)
                s.listen(1)
            except OSError as msg:
                s.close()
                s = None
                continue
                break
    if s is None:
        print('could not open socket')
        sys.exit(1)

    print("My address is: " , sa)
    return s
