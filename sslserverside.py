import socket
import ssl
import threading

class SecureServer:
    def __init__(self, host, port, server_cert, server_key, ca_cert_file):
        self.host = host
        self.port = port
        self.server_cert = server_cert
        self.server_key = server_key
        self.ca_cert_file = ca_cert_file
        
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=self.ca_cert_file)
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED
        self.ssl_context.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Server is listening on {self.host}:{self.port}")
            while True:
                client_conn, client_addr = server_socket.accept()
                print(f"Connection from {client_addr}")
                threading.Thread(target=self.handle_client, args=(client_conn,)).start()

    def handle_client(self, client_conn):
        try:
            
            with self.ssl_context.wrap_socket(client_conn, server_side=True) as secure_conn:
                print("Secure connection is up")
                while True:
                    data = secure_conn.recv(1024)
                    if not data:
                        break
                    print("Received:", data.decode())
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
        finally:
            client_conn.close()

if __name__ == "__main__":
    server = SecureServer(
        host="127.0.0.1",
        port=12345,
        server_cert="/home/kali/Desktop/LABA 4/server_certificate.pem",
        server_key="/home/kali/Desktop/LABA 4/server_private.key",
        ca_cert_file="/home/kali/Desktop/LABA 4/ca_certificate.pem"
    )
    server.start_server()
