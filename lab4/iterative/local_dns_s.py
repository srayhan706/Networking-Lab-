import socket
import threading
import os
import struct
cache = []
def load_file(filename):
    dns_record = {}
    with open(filename, "r") as file:
        for line in file:
            name, value, r_type, ttl = line.strip().split()
            name = name.lower()  # Convert domain name to lowercase
           # print(name)
            if name not in dns_record:
                dns_record[name] = []  # Initialize list if domain name doesn't exist
            dns_record[name].append((value, r_type, int(ttl)))
    return dns_record

   
def handle_dns_query_iterative(msg, c_addr, server):

    
    

    print(f'Connected to {c_addr}, and the client is querying for {msg}')
    
    print("locan dns cannot find the ip..so it start the request for root")
    
    for item in cache:
        parts = item.split()  # Splitting the string by space
        debug=parts[0]
        if parts[0] == msg.decode():
            server.sendto(item.encode(), c_addr)
     
            return  
    
    #connected with root
   # kisu=input("press enter for access root")
    client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr=(("10.33.2.203",9195))
    
    client.sendto(msg,server_addr)

    # flag,_=client.recvfrom(1024)
    # print(flag.decode())


    msg1,_=client.recvfrom(1024)

    address=msg1.decode()
    address=address.split()
    ip=address[0]
    port=int(address[1])
    #connected to tld
    
    client_tld=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr_tld=((ip,port))
    
    client_tld.sendto(msg,server_addr_tld)
    
    msg2,_=client_tld.recvfrom(1024)
    
    
    
    
    #connect to auth
    msg2=msg2.decode()
    
    print(f"ip of auth {msg2}")
    
    msg2=msg2.split()
    ip1=msg2[0]
    
    port1=int(msg2[1])
    
    client_auth=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr_auth=((ip1,port1))
    
    client_auth.sendto(msg,server_addr_auth)
    
    msg3,_=client_auth.recvfrom(1024)
    
    
    
    
    
    
    
    server.sendto(msg3, c_addr)

    






    # domain_name = msg.decode().lower()  # Decode the message from bytes to string
    # print("Lowercased domain:", domain_name)
    # if domain_name in dns_record:
    #     records = dns_record[domain_name][-1]  # Get the last record for the domain
    # # Construct the response by joining the last record's components
        
    #     result = domain_name+" ".join(map(str, records))
    # else:
    #     result = "Not found. You have to register this domain name."

      # Send the response to the client


def main():
    server=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    global dns_record
    dns_record=load_file("dns_records.txt")
    server.bind(('10.33.2.204',9993))
    
    print("local_dns server  is running")
    
    while True:
       msg,c_addr =server.recvfrom(1024)

       th=threading.Thread(target=handle_dns_query_iterative,args=(msg,c_addr,server))
       th.start()



if __name__=='__main__':
    main()    
