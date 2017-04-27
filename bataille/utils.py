import socket
#Shot Validation

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
		if len(input[0]) > 1:
			first = input[0]
			first = first[:1]
			return int(first)
		return (int(input[0]))

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
