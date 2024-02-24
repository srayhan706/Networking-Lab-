import socket
import time

# Function to create TCP segment header
def makeheader(seqNum=0, ackNum=0, ack=0, sf=0, rwnd=0):
    header = seqNum.to_bytes(4, byteorder="little")
    header += ackNum.to_bytes(4, byteorder="little")
    header += ack.to_bytes(1, byteorder="little")
    header += sf.to_bytes(1, byteorder="little")
    header += rwnd.to_bytes(2, byteorder="little")
    return header

# Function to parse TCP segment header
def fromheader(segment):
    seqNum = int.from_bytes(segment[:4], byteorder="little")
    ackNum = int.from_bytes(segment[4:8], byteorder="little")
    ack = int.from_bytes(segment[8:9], byteorder="little")
    sf = int.from_bytes(segment[9:10], byteorder="little")
    rwnd = int.from_bytes(segment[10:12], byteorder="little")
    return seqNum, ackNum, ack, sf, rwnd

# Function to calculate SampleRTT using EWMA
def calculate_sample_rtt(sample_rtt, alpha, new_rtt):
    return alpha * sample_rtt + (1 - alpha) * new_rtt

# Function to calculate Timeout using EWMA
def calculate_timeout(sample_rtt, estimated_rtt, alpha):
    return alpha * estimated_rtt + (1 - alpha) * sample_rtt

# Function to send data packets and handle acknowledgments
def send_data_packets(cl_socket, data, data_len, mss, rec_buf_size, alpha):
    head_len = 12
    win_size = mss
    seq_num = 0
    exp_ack_num = 0
    rec_win = 50
    sent_size = 0
    dup_ack = 0
    last_ack = 0
    sample_rtt = 0
    estimated_rtt = 0
    timeout = 1  # Initial timeout value
    start_time = time.time()

    # Open files to store SampleRTT and timeout
    sample_rtt_file = open("sample_rtt.txt", "w")
    timeout_file = open("timeout.txt", "w")

    while seq_num < data_len:
        curr_sent_size = 0
        while curr_sent_size < win_size and seq_num < data_len:
            send_size = min(mss, data_len - seq_num)
            send_time = time.time()  # Start timer
            cl_socket.sendall(makeheader(seq_num, seq_num, 0, 0, 0) + data[seq_num:seq_num + send_size])
            print(f"Data sent with sequence number {seq_num}")
            curr_sent_size += send_size
            sent_size += send_size
            seq_num += send_size

            # Receive ACK and calculate SampleRTT
            ack_pkt = cl_socket.recv(head_len)
            recv_time = time.time()  # Stop timer
            sample_rtt = recv_time - send_time
            estimated_rtt = calculate_sample_rtt(sample_rtt, alpha, estimated_rtt)
            timeout = calculate_timeout(sample_rtt, estimated_rtt, alpha)

            # Write SampleRTT and timeout to files
            sample_rtt_file.write(f"{sample_rtt}\n")
            timeout_file.write(f"{timeout}\n")

            print("Acknowledgement packet received")
            seqNum, ack_num, ack, sf, rec_win = fromheader(ack_pkt)
            print(f"Sequence number {seqNum}, expected Ackn_Number {exp_ack_num}, Ackn_Number {ack_num}")
            win_size = min(2 * rec_buf_size, rec_win)

            # Implement Cumulative ACK
            if ack_num == last_ack:
                dup_ack += 1
            else:
                dup_ack = 0
            if dup_ack == 3:
                print("Received Triple Duplicate Acknowledgement, go back to last_ack")
                dup_ack = 0
                seq_num = last_ack

            last_ack = ack_num

    # Close files
    sample_rtt_file.close()
    timeout_file.close()

    print("Data transmission completed.")

# Main function to initiate the client
def main():
    cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_addr = ('127.0.0.1', 8888)
    cl_socket.connect(serv_addr)

    rec_buf_size = 4
    mss = 20
    alpha = 0.125  # Alpha value for EWMA

    filename = "send.txt"
    with open(filename, "rb") as file:
        data = file.read()
    data_len = len(data)
    print(f"Length of the file: {data_len}")

    send_data_packets(cl_socket, data, data_len, mss, rec_buf_size, alpha)

    cl_socket.close()

if __name__ == "__main__":
    main()
