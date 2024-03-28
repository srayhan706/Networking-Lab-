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

cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_addr = ('127.0.0.1', 8888)
cl_socket.connect(serv_addr)

head_len = 12
rec_buf_size = 4
mss = 8
win_size = 8
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
estimated_rtt = 0.4
sample_rttinit = 0.3
alpha = 0.125
beta = 0.25
dev_rtt = 0.35
cwnd=mss
ssthresh=25
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

        if not sf:
            curr_time = time.time()
            sample_rtt = round((curr_time - start_time)*1000,4)
            estimated_rtt = alpha * sample_rtt + (1 - alpha) * estimated_rtt
            dev_rtt = beta * abs(sample_rtt - estimated_rtt) + (1 - beta) * dev_rtt
            timeout = round(estimated_rtt + 4 * dev_rtt,4)

            # Store sample RTT and timeout values
            sample_rtt_file.write(f"Packet Number: {ack_num}, Sample RTT: {sample_rtt}\n")
            timeout_file.write(f"Packet Number: {ack_num}, Timeout: {timeout}\n")

            print(f'Timing Updates : {estimated_rtt}, {sample_rtt}, {dev_rtt}, {timeout}')

        if ack_num >= data_len:
            break

        

        if ack_num == last_ack:
            dup_ack += 1
        else:
            dup_ack = 0
            #slow start phase
            if cwnd<=ssthresh:
               cwnd=cwnd*2
            else:
            # congestion avoidance phase
                cwnd=cwnd+1
            
        if dup_ack == 3:
            
            ssthres=cwnd//2
            
            # first recovery phase
            cwnd=ssthres+3
            
            print("Received Triple Duplicate Acknowledgment, go back to last_ack")
            dup_ack = 0
            seq_num = last_ack
            
        win_size = min( rec_win,cwnd)
        last_ack = ack_num

cl_socket.close()
