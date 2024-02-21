import socket
import time

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

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_addr = ('127.0.0.1', 8888)
cl_socket.connect(serv_addr)

head_len = 12
rec_buf_size = 4
mss = 20
win_size = mss
cl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rec_buf_size)

seq_num = 0
exp_acq_num = 0

filename = "send.txt"
with open(filename, "rb") as file:
    data = file.read()
data_len = len(data)
print(f"length of the file {data_len}")

timeout = 2
start_time = time.time()
rec_win = 50
sent_size = 0
dup_ack = 0
last_ack = 0

while seq_num < data_len:
    curr_sent_size = 0
    while curr_sent_size < win_size and seq_num < data_len:
        send_size = min(mss, data_len - seq_num)
        cl_socket.sendall(makeheader(seq_num, seq_num, 0, 0, 0) + data[seq_num:seq_num + send_size])
        print(f"data sent of sequence number {seq_num}")
        curr_sent_size += send_size
        sent_size += send_size
        seq_num += send_size

    exp_acq_num = seq_num
    ack_pkt = cl_socket.recv(head_len)
    print("acknowledgement packet recieved")
    seqNum, ack_num, ack, sf, rec_win = fromheader(ack_pkt)
    print(f"sequence number {seqNum},expected Ackn_Number {exp_acq_num},Ackn_Number {ack_num}")
    win_size = min(2 * rec_buf_size, rec_win)


    if ack_num == last_ack:
        dup_ack += 1
    else:
        dup_ack = 0
    if dup_ack == 3:
        print("Received Triple Duplicate Acknowledgement, go back to last_ack")
        dup_ack = 0
        seq_num = last_ack

    last_ack = ack_num

cl_socket.close()
