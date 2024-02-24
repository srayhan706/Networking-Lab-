import socket
import threading
import os
import struct


def load_file(filename):
    dns_record = {}
    with open(filename, "r") as file:
        for line in file:
            name, value, r_type, ttl = line.strip().split()
            name = name.lower()  # Convert domain name to lowercase
            print(name)
            if name not in dns_record:
                dns_record[name] = []  # Initialize list if domain name doesn't exist
            dns_record[name].append((value, r_type, int(ttl)))
    return dns_record


def handle_dns_query_iterative(msg, c_addr, server):
    #flag="Auth server is working"
   # server.sendto(flag.encode(),c_addr)
    print(f'Connected to {c_addr}, and the client is querying for {msg}')

    domain_name = msg.decode().lower()
    my_string =domain_name
    modified_string = my_string[:-3]
    print(modified_string)
    domain_name=modified_string


    # Decode the message from bytes to string
    print("Lowercased domain:", domain_name)
    if domain_name in dns_record:
        records = dns_record[domain_name][-1]  # Get the last record for the domain
        # Construct the response by joining the last record's components

        result = domain_name+"com"+" " + " ".join(map(str, records))
    else:
        result = "Not found. You have to register this domain name."

    server.sendto(result.encode(), c_addr)  # Send the response to the client


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    global dns_record
    dns_record = load_file("dns_records.txt")
    server.bind(('10.33.2.203', 9997))

    print("dns server  is running")

    while True:
        msg, c_addr = server.recvfrom(1024)
        th = threading.Thread(target=handle_dns_query_iterative, args=(msg, c_addr, server))
        th.start()


if __name__ == '__main__':
    main()