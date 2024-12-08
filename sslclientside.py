import socket
import ssl

class SecureClient:
    def __init__(self, server_address, server_port, client_cert_file, client_key_file, ca_cert_file):
        self.server_address = server_address
        self.server_port = server_port
        self.client_cert_file = client_cert_file
        self.client_key_file = client_key_file
        self.ca_cert_file = ca_cert_file
        
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.ca_cert_file)
        self.context.verify_mode = ssl.CERT_REQUIRED  
        self.context.load_cert_chain(certfile=self.client_cert_file, keyfile=self.client_key_file)
    
    def connect(self):
        with socket.create_connection((self.server_address, self.server_port)) as sock:
            with self.context.wrap_socket(sock, server_hostname=self.server_address) as ssock:
                print(f"Connected to {self.server_address} on port {self.server_port}")
                return ssock
    
    def send_message(self, message):
        with self.connect() as secure_socket:
            secure_socket.sendall(message.encode())
            print("Message sent.")

if __name__ == "__main__":
    client = SecureClient(
        server_address="127.0.0.1",
        server_port=12345,
        client_cert_file="/home/kali/Desktop/LABA 4/client_certificate.pem",
        client_key_file="/home/kali/Desktop/LABA 4/client_private.key",
        ca_cert_file="/home/kali/Desktop/LABA 4/ca_certificate.pem"
    )
    
    client.send_message("Confidential information to be securely transmitted.")
