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

def calculate_timeout(sample_rtt, alpha=0.125):
    return (1 - alpha) * timeout + alpha * sample_rtt

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_addr = ('127.0.0.1', 8888)
cl_socket.connect(serv_addr)

head_len = 12
rec_buf_size = 4
mss = 20
win_size = 20
cl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rec_buf_size)

seq_num = 0
exp_acq_num = 0

filename = "send.txt"
with open(filename, "rb") as file:
    data = file.read()
data_len = len(data)
print(f"Length of the file {data_len}")

rec_win = 50
sent_size = 0
dup_ack = 0
last_ack = 0
sample_rtt = []
timeout = 1

with open("sample_rtt.txt", "w") as sample_rtt_file, open("timeout.txt", "w") as timeout_file:
    while seq_num < data_len:
        start_time = time.time()
        curr_sent_size = 0
        while curr_sent_size < win_size and seq_num < data_len:
            send_size = min(mss, data_len - seq_num)
            cl_socket.sendall(makeheader(seq_num, seq_num, 0, 0, rec_win) + data[seq_num:seq_num + send_size])
            print(f"Data sent of sequence number {seq_num}")
            curr_sent_size += send_size
            sent_size += send_size
            seq_num += send_size

        exp_acq_num = seq_num
        ack_pkt = cl_socket.recv(head_len)
        print("Acknowledgment packet received")
        seqNum, ack_num, ack, sf, rec_win = fromheader(ack_pkt)
        print(f"Sequence number {seqNum}, expected Ackn_Number {exp_acq_num}, Ackn_Number {ack_num}")
        sample_rtt_value = time.time() - start_time
        sample_rtt.append(sample_rtt_value)
        sample_rtt_file.write(str(sample_rtt_value) + "\n")

        timeout = calculate_timeout(sample_rtt_value)
        timeout_file.write(str(timeout) + "\n")

        win_size = min(2 * rec_buf_size, rec_win)

        if ack_num == last_ack:
            dup_ack += 1
        else:
            dup_ack = 0
        if dup_ack == 3:
            print("Received Triple Duplicate Acknowledgment, go back to last_ack")
            dup_ack = 0
            seq_num = last_ack

        last_ack = ack_num

cl_socket.close()
