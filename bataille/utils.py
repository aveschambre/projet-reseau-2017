import socket
#Shot Validation

def inputStandardization(input):
	if input != None :
		output = ord(input[0].upper())-ord("A")+1
		return output



#other validations ?


def waitClientReconnect() :
    return

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
