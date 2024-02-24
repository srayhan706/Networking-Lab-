import socket
import threading
import os
import struct
cache = []
def handlelocaldns(msg, c_addr, server):
    print(f'Connected to {c_addr}, and the client is querying for {msg}')
    
    
    for item in cache:
        parts = item.split()  # Splitting the string by space
        debug=parts[0]
        if parts[0] == msg.decode():
            server.sendto(item.encode(), c_addr)
     
            return
    msgs=msg.decode()
    dom=msgs.split('.')
    kisu=dom[-1]
    print(kisu)
    #aaa=input("please enter to open tld server")
    client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_addr=(("10.33.2.204",9996))

    client.sendto(msg,server_addr)
    msg,_=client.recvfrom(1024)
    print(msg.decode())

    msg,_=client.recvfrom(1024)
    server.sendto(msg,c_addr)
    
    
def main():
    server=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server.bind(('10.33.2.203',9195))

    print("root server  is running")

    while True:
       msg,c_addr =server.recvfrom(1024)
       flag="Root server working"
       server.sendto(flag.encode(),c_addr)
       handlelocaldns(msg,c_addr,server)


if __name__=='__main__':
    main()
