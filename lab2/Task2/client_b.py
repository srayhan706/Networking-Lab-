import socket
import time

cl_sock = socket.socket()
id = 0

def connection():
    host = ''
    port = 6990
    cl_sock.connect((host, port))
    user = input("Enter Your Username: ")
    cl_sock.send(user.encode())

    pasw = input("Enter Your Password: ")
    cl_sock.send(pasw.encode())

    cc = cl_sock.recv(1024).decode()

    if cc == '404':
        print("Server Error: ")
        cl_sock.close()


def clientdriver(id):
    while True:
        print('Please Select')
        print('1. Check Balance')
        print('2. Cash Withdraw')
        print('3. Cash Deposit')

        opt = input("Enter : ")
        cl_sock.send(opt.encode())

        if int(opt) == 1:
            msg = cl_sock.recv(1024).decode()
            print(msg)

        elif int(opt) == 3:
            am = input("Enter the amount to deposit: ")
            cl_sock.send(am.encode())
            msg = cl_sock.recv(1024).decode()
            print(msg)

        elif int(opt) == 2:
            withdrawhelper(id)


        print('Anything else')  # after executing one request
        print('1. YES')
        print('2. NO')
        a = input('ENTER : ')  # enter the desired option
        cl_sock.send(a.encode())
        if a == '2':
            break

def widra_req(id, wit, client_socket):
    client_socket.send(wit.encode())
    time.sleep(1)
    id=str(id)
    client_socket.send(id.encode())



def withdrawhelper(id):
    id = id + 1
    wam = input("Enter the amount of withdrawal: ")

    if int(wam) <= 0:
        print("Enter Correct Amount to withdraw")
        msg = cl_sock.recv(1024).decode()
        print(msg)

    else:
        while True:
            widra_req(id, wam, cl_sock)

            r = cl_sock.recv(1024).decode()
            print(r)

            if r == '401':
                print("Insufficient Balance")
            elif r == '555':
                print("Failed Attempt")
                print("Try Again!")
                print('1. Yes')
                print('2. No')
                trya = input('Enter : ')

                if trya == '1':
                    cl_sock.send(('2').encode())
                    time.sleep(0.5)
                    continue
                else:
                    break
            else:
                print(r)
                break

connection()

clientdriver(id)

cl_sock.close()
