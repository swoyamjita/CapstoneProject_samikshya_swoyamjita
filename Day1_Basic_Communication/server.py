
# day 1 Server - Client Socket Communication - Server Side
#
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1' 
PORT = 5050
server_socket.bind((HOST, PORT))

server_socket.listen(1)
print(f"[*] Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"[+] Connected to client: {addr}")

data = conn.recv(1024).decode()
print(f"[Client]: {data}")

conn.send("Hello Client, connection established!".encode())

conn.close()
server_socket.close()
print("[*] Connection closed.")
