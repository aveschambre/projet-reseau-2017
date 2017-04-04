import socket
import select
import threading

sock = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 7777))
sock.listen(1)

connects = [sock]
def connector(acpt) :
    while True :
        message = acpt.recv(2048)
        if len(message) == 0 :
            acpt.close()
            break
        acpt.send(message)

while True :
    #acpt, addr = sock.accept()
    #threading.Thread(None, connector, None, (acpt,)).start()
    (socks,_,_) = select.select(connects, [], [])
    for x in range(0, len(socks), 1) :
        if socks[x] == sock :
            acpt, addr = sock.accept()
            connects.append(acpt);
        else :
            message = socks[x].recv(2048)
            #print(message)
            if len(message) == 0 :
                socks[x].close()
                connects.remove(socks[x])
                break
            for skt in connects :
                print(message)
                if (skt != socks[x]) and (skt != sock)  :
                    skt.send(message)
