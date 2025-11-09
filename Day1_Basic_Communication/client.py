# day 1 Server - Client Socket Communication - Client Side
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1' 
PORT = 5050
client_socket.connect((HOST, PORT))

client_socket.send("Hello Server, this is Client!".encode())

data = client_socket.recv(1024).decode()
print(f"[Server]: {data}")

client_socket.close()
