# Day 4 File Upload - Server Side
import socket
import threading
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002
BUFFER_SIZE = 4096

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def handle_client(client_socket, address):
    print(f"[+] New connection from {address}")
    try:
        # Receive filename and filesize
        received = client_socket.recv(BUFFER_SIZE).decode()
        if not received:
            print("[!] Empty data received, closing connection.")
            client_socket.close()
            return

        filename, filesize = received.split("|")
        filename = os.path.basename(filename)
        filesize = int(filesize)
        filepath = os.path.join(UPLOAD_DIR, filename)

        print(f"[→] Receiving '{filename}' ({filesize} bytes) from {address}")

        # Receive file data
        with open(filepath, "wb") as f:
            bytes_received = 0
            while bytes_received < filesize:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                bytes_received += len(bytes_read)

        print(f"[✓] File '{filename}' received successfully from {address}")
        client_socket.send("UPLOAD_COMPLETE".encode())

    except Exception as e:
        print(f"[!] Error while receiving file: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()
