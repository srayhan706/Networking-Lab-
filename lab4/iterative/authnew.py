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
    flag = "Auth server is working"
    server.sendto(flag.encode(), c_addr)
    print(f'Connected to {c_addr}, and the client is querying for {msg}')

    domain_name = msg.decode().lower()
    modified_domain = domain_name[:-3]
    print(modified_domain)

    # Decode the message from bytes to string
    print("Lowercased domain:", modified_domain)

    if modified_domain in dns_record:
        # Fetch all records for the domain
        records = dns_record[modified_domain]

        # Find the record with the minimum TTL
        min_ttl = float('inf')  # Initialize with infinity
        min_ttl_record = None

        for record in records:
            if record[2] < min_ttl:
                min_ttl = record[2]
                min_ttl_record = record

        # Construct the response by joining the components of the record with minimum TTL
        result = modified_domain + ".com" + " " + " ".join(map(str, min_ttl_record))

        # Update text file by removing records with TTL greater than min_ttl
        dns_record[modified_domain] = [min_ttl_record]  # Keep only the record with minimum TTL
        with open("ndns_records.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                parts = line.strip().split()
                if parts[0].lower() == modified_domain and int(parts[-1]) > min_ttl:
                    continue  # Skip writing this line if TTL is greater than min_ttl
                file.write(line)
            file.truncate()  # Remove any extra lines at the end of the file
    else:
        result = "Not found. You have to register this domain name."

    server.sendto(result.encode(), c_addr)  # Send the response to the client


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    global dns_record
    dns_record = load_file("ndns_records.txt")
    server.bind(('10.33.2.203', 9997))

    print("dns server  is running")

    while True:
        msg, c_addr = server.recvfrom(1024)
        th = threading.Thread(target=handle_dns_query_iterative, args=(msg, c_addr, server))
        th.start()


if __name__ == '__main__':
    main()