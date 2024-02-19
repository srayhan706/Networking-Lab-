import socket


def primechek(num):

    for i in range (2,int(num/2)):
        if num%i==0:
            return False
    return True


def palchek(pal):

    l=len(pal)

    for i in range (0,int (l/2)):
        if pal[i]!=pal[-(i+1)]:
            return False

    return True


def connection():
    hostn=socket.gethostname()
    host=socket.gethostbyname(hostn)
    port=4553
    print(host)

    serv_sock=socket.socket()
    serv_sock.bind(('',port))
    serv_sock.listen(2)

    con,addr=serv_sock.accept()

    print("Connected to : "+str(addr))

    return  con


def serv_driver(c):
    while True:


        text=c.recv(1024).decode()
        print("Client wants to convert uppercase : "+str(text))
        c.send(text.upper().encode())


        #recieving option
        opt=int(c.recv(1024).decode())

        print(opt)
        if opt==1:

            numb=int(c.recv(1024).decode())
            print(f"Checking wheter {numb} is prime")
            if primechek(numb):
                c.send(bytes("Your number is a prime number",'utf-8'))
            else:
                c.send(bytes("Your number is not prime",'utf-8'))

        elif opt==2:
            pal=c.recv(1024).decode()
            print(f"Checking wheter {pal} is palindrome ")
            if palchek(pal):
                c.send(bytes("Your number is a palindrome number",'utf-8'))

            else:
                c.send(bytes("Your number is not a palindrome number",'utf-8'))
        else:
            c.close()
            break





c=connection()

serv_driver(c)

