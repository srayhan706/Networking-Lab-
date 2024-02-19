import  socket
def connection():
    host=''
    port=4553

    client_sock=socket.socket()

    client_sock.connect((host,port))

    return client_sock


def client_driver(c):
    while True:
        #sending text
        text=input("Enter a line of text : ")
        c.send(text.encode())

        #recieving uppercase
        msg = c.recv(1024).decode()
        print(msg)

        #recieving option printing things
        print("Choice Your Option ")
        print("1. Prime Check")
        print("2. Palindrome Check")
        print("3. No more ")

        opt=input("Enter : ")
        c.send(opt.encode())

        num=input("Enter your number: ")
        c.send(num.encode())

        msg=c.recv(1024).decode()
        print(msg)

        if opt=="3":
            c.close()
            break


c=connection()

client_driver(c)