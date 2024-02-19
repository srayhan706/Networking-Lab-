from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/list_files':
                # Get a list of all files in the server directory
                files = os.listdir('.')
                files_str = "\n".join(files)

                # Send the list of files as the response
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(files_str.encode())
            else:
                # Extracting file path from the request
                file_path = self.path.strip("/")
                if not os.path.exists(file_path):
                    raise FileNotFoundError

                # Sending the file to the client
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            # Extracting file name from the request path
            file_name = self.path.strip("/")
            if not file_name:
                raise ValueError("File name not provided in the request")
            # Reading file content from the request
            file_content = self.rfile.read(content_length)

            # Saving the received file
            with open(file_name, 'wb') as file:
                file.write(file_content)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File saved successfully')
        except Exception as e:
            self.send_error(500, str(e))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8005):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
