import socket
import  time


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (("10.33.2.204", 9993))
    t1=time.time()
    domain = "cse.du.ac.bd.com"
    client.sendto(domain.encode(), server_addr)

    # msg, _ = client.recvfrom(1024)
    # print(msg.decode())
    #

    msg, _ = client.recvfrom(1024)
    print(msg.decode())
    t2=time.time()

    print(t2-t1)


if __name__ == "__main__":
    main()
