import socket
import time
import random

def makeheader(seqNum=0, ackNum=0, ack=0, sf=0, rwnd=0):
    header = seqNum.to_bytes(4, byteorder="little")
    header += ackNum.to_bytes(4, byteorder="little")
    header += ack.to_bytes(1, byteorder="little")
    header += sf.to_bytes(1, byteorder="little")
    header += rwnd.to_bytes(2, byteorder="little")
    return header

def fromheader(segment):
    seqNum = int.from_bytes(segment[:4], byteorder="little")
    ackNum = int.from_bytes(segment[4:8], byteorder="little")
    ack = int.from_bytes(segment[8:9], byteorder="little")
    sf = int.from_bytes(segment[9:10], byteorder="little")
    rwnd = int.from_bytes(segment[10:12], byteorder="little")
    return seqNum, ackNum, ack, sf, rwnd

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_addr = ('', 8888)
serv_sock.bind(serv_addr)
serv_sock.listen(1)

cl_socket, client_address = serv_sock.accept()
print(f"Accepted connection from {client_address}")

rec_buf_size = 16
win_size = 20
mss = 10
cl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rec_buf_size)

expected_seq_num = 0
ack_num = 0
start_time = time.time()
cl_socket.settimeout(1)
timeout = 1
received_data = b''
buffer_data = b''

while True:
    try:
        header = cl_socket.recv(12)
        seq_num, ack_num, ack, sf, rwnd = fromheader(header)
        print(f"sequence number from client {seq_num},acknowledgement from client {ack_num}")
        data = cl_socket.recv(mss)
        print(data)
        print("header & data asche")

    except:
        print("except block a asce")
        rwind = rec_buf_size - (len(buffer_data) + mss - 1) // mss
        to_send_ack = makeheader(expected_seq_num, ack_num, 1, 0, rwind)
        print(f"seq_number {seq_num},acknowledgement_num {ack_num}")
        cl_socket.sendall(to_send_ack)
        start_time = time.time()
        continue

    if not data:
        print("No data received")
        break

    seq_num = ack_num

    if seq_num == expected_seq_num and random.randint(0, 2) != 0:
        buffer_data += data
        ack_num += len(data)
        expected_seq_num += len(data)
        to_send_ack = makeheader(seq_num, ack_num, 1, 0, 8)
        if(len(buffer_data) >= rec_buf_size):
            received_data += buffer_data
            buffer_data = b''
            try:
                cl_socket.sendall(to_send_ack)
                print(f"seq_number {seq_num},acknowledgement_num {ack_num}")
            except:
                print("Client closed")
    else:
        to_send_ack = makeheader(expected_seq_num, expected_seq_num, 1, 0, 0)
        cl_socket.sendall(to_send_ack)
        cl_socket.sendall(to_send_ack)
        cl_socket.sendall(to_send_ack)
        print(f"seq_number {seq_num},acknowledgement_num {ack_num}")

# Write received data to a file
with open("received_data.txt", "wb") as file:
    file.write(received_data)

cl_socket.close()
serv_sock.close()
