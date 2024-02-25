import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8081


def receive_file(conn, filename):
    buffer_size = 4096
    received_data = b''

    try:
        with open(filename, 'wb') as file:
            while True:
                data = conn.recv(buffer_size)
               
                if not data or len(data) < buffer_size:
                   # print("break hosse na")
                    break

                
                received_data += data
           
            file.write(received_data)
            print("file is receives successfulyy")
            # Write all received data to the file
    except FileNotFoundError:
        print("[*] File not found")

def send_file(conn, filename):
    try:
        with open(filename, 'rb') as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                conn.sendall(data)
            print("[*] File sent")
    except FileNotFoundError:
        print("[*] File not found")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        operation = input("Enter 'download' to download file or 'upload' to upload file: ")
        client_socket.sendall(operation.encode())

        if operation == 'download':
           # msg= client_socket.recv(1024).decode()
           # print(msg)

            filename = input("Enter the name of the file you want to download: ")
            client_socket.sendall(filename.encode())
            print(f"[*] Requesting file: {filename}")
            receive_file(client_socket, filename)
        elif operation == 'upload':
            filename = input("Enter the name of the file you want to upload: ")
            client_socket.sendall(filename.encode())
            print(f"[*] Uploading file: {filename}")
            send_file(client_socket, filename)


if __name__ == "__main__":
    main()
