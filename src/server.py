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
        print(f"Server listens on http://{self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from: {client_address}")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()


        except KeyboardInterrupt:
            print("\nShutting down the server")
        finally:
            self.server_socket.close()

    def http_parse(self, request: str): #Parsing http into a tuple
        http_lines = request.split("\r\n")

        empty_index = http_lines.index('') if '' in http_lines else -1

        if empty_index != -1:
            header = http_lines[:empty_index]
            body = http_lines[empty_index + 1]
            return header, body
        else:
            return http_lines, None

    def request_line_parse(self, head: list):
        if not head:
            raise ValueError("Empty header list")
        request_line = head[0]
        request_parts = request_line.split(' ')
        if len(request_parts) >= 2:
            method = request_parts[0]
            path = request_parts[1]
            return (method, path)
        return ("GET", "/") # Fallback


    def handle_client(self, client_socket):
        # TODO Handle:
        # Recieve request data and parse the request

        # Example of a simple HTTP request
        # GET /path?query=value HTTP/1.1\r\n
        # Host: example.com\r\n
        # User-Agent: Mozilla/5.0\r\n
        # Content-Type: application/json\r\n
        # Content-Length: 18\r\n
        # \r\n
        # {"key": "value"}

        try:

            request_data = client_socket.recv(4096).decode("utf-8") #Reading 4096 bytes of data, decoding it into utf-8
            if not request_data:
                return "No request_data recieved"
        
            #Parsing HTTP(oh boy)
            header, body = self.http_parse(request_data)
            method, path = self.request_line_parse(header) #For some reason pyright keeps flagging it as an error yet is still works

            
            #Respond to request line
            if path == "/":
                response_body = "<h1>Welcome</h1><p>Server is running<p>"
                status_code = "200 OK"
            elif path == "/test":
                response_body = "<h1>Test Page</h1>"
                status_code = "200 OK"
            else:
                response_body = "<h1>404 Not Found Error</h1>"
                status_code = "404 Not Found"

            #Forming and sending HTTP response
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-length: {len(response_body)}\r\nConnection: close\r\n\r\n"
            response += response_body
        
            client_socket.send(response.encode("utf-8"))

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

# Run server
if __name__ == '__main__':
    server = HTTPServer(host='127.0.0.1', port=8080)
    server.start_server()
        
