import  socket
import time
import random

usa='rayhan'
pasa='1234'
bala=120000

usb='sakib'
pasb='123'
balb=50000

d={}
serv_sock=socket.socket()
def connection():

    hostn = socket.gethostname()
    host = socket.gethostbyname(hostn)
    port = 6990

    print(host)

    serv_sock.bind(('', port))
    serv_sock.listen(5)
    c, addr = serv_sock.accept()

    print("Connected to: " + str(addr))
    return c


def servertransiction(bala):
    while True:
        opt = c.recv(1024).decode()
        print('choice ', opt)

        if int(opt) == 1:
            print("Holder wants to know balance")
            c.send(("Your current balance is : " + str(bala)).encode())

        elif int(opt) == 3:
            am = int(c.recv(1024).decode())
            bala = bala + am
            c.send(("After deposing current balance is: " + str(bala)).encode())

        elif int(opt)==2:
            am = int(c.recv(1024).decode())
            print(am)

            if am <= 0:
                continue

            id = c.recv(1024).decode()

            if d.get(id) is not None:
                print('Error')
                c.send(('555').encode())

            else:
                print("Wtihdrawn amnt: ", am)

                if bala < am:
                    c.send(('401').encode())
                    continue
                else:
                    d[id] = {usa, am}

                    ra = random.randint(0, 50)
                    print(ra)

                    if ra > 50:
                        c.send(('401').encode())
                        continue
                    bala = bala - am
                    c.send(("Withdraw successful!After withdraw your balance is: " + str(bala)).encode())
                    print(d)
            any=c.recv(1024).decode()

            if any=='1':
                continue
            else:
                break


            


def serverdriver(c,bala):
    while True:
        user = c.recv(1024).decode()
        if not user:
            break

        if user == usa:
            pas = c.recv(1024).decode()
            if pas == pasa:
                c.send('40'.encode())

                servertransiction(bala)

            else:
                print("Invalid Password")
                c.send(('404').encode())
                c.close()
        else:
            print('Invalid User')
            c.send(('404').encode())
            c.close()



c=connection()

serverdriver(c,bala)













