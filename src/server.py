import socket
import threading
# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)
#
# print(f'Hostname : {hostname}')
# print(f'IP: {ip}')

class HTTPServer:
    
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Reusable addr
        self.server_socket.bind((self.host, self.port))

        self.server_socket.listen(5)
        print(f"Server listens on https://{self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from: {client_address}")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))

        except KeyboardInterrupt:
            print("\nShutting down the server")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        pass

# Run server
if __name__ == '__main__':
    server = HTTPServer(host='127.0.0.1', port=8080)
    server.start_server()
        
