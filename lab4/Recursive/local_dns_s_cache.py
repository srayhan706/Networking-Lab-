import socket
import threading
import os
import struct

cache = []

def handle_dns_query_iterative(msg, c_addr, server):
    flag = "true..local dns process to find your data from root"
    server.sendto(flag.encode(), c_addr)
    print(f'Connected to {c_addr}, and the client is querying for {msg}')
    #print("local dns cannot find the ip, so it starts the request for root")
    debug="debug"
    for item in cache:
        parts = item.split()  # Splitting the string by space
        debug=parts[0]
        if parts[0] == msg.decode():
            server.sendto(item.encode(), c_addr)
     
            return
    print(debug)     
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = ("10.33.2.203", 9195)

    client.sendto(msg, server_addr)

    flag, _ = client.recvfrom(1024)
    print(flag.decode())

    msg, _ = client.recvfrom(1024)
    server.sendto(msg, c_addr)

    cache.append(msg.decode())
    
    cache.append(msg.decode())


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global dns_record
    
    server.bind(('10.33.2.204', 9993))
    print("local_dns server is running")
    
    while True:
        msg, c_addr = server.recvfrom(1024)
        th = threading.Thread(target=handle_dns_query_iterative, args=(msg, c_addr, server))
        th.start()

if __name__ == '__main__':
    main()
