import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8081
server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

def clienthandle(conn, addr):
    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

    operation = conn.recv(1024).decode()
    filename = conn.recv(1024).decode()

    if operation == 'download':
        print(f"[*] Client requested file: {filename}")
        send_file(conn, filename, addr)
    elif operation == 'upload':
        print(f"[*] Client uploading file: {filename}")
        receive_file(conn, filename, addr)


def receive_file(conn, filename, addr):
    buffer_size = 4096
    received_data = b''

    try:
        with open(filename, 'wb') as file:
            while True:
                data = conn.recv(buffer_size)
                if not data:
                    break
                received_data += data
                buffer_size *= 2

            file.write(received_data)
            print(f"[*] File received from {addr[0]}")
    except FileNotFoundError:
        print("[*] File not found")


def send_file(conn, filename, addr):
    try:
        with open(filename, 'rb') as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                conn.sendall(data)
            print(f"[*] File sent to {addr[0]}")
    except FileNotFoundError:
        print("[*] File not found")


def main():
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=clienthandle, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()

