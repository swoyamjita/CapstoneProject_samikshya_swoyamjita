#day3_file_transfer/server.py
import socket
import os

HOST = '127.0.0.1'
PORT = 5051
BUFFER_SIZE = 4096
TEST_FOLDER = 'test_files'   
if not os.path.exists(TEST_FOLDER):
    os.makedirs(TEST_FOLDER)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[*] Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"[+] Connected to client: {addr}")

    files = os.listdir(TEST_FOLDER)
    if not files:
        file_list = "No files available."
    else:
        file_list = "\n".join(files)

    conn.send(file_list.encode())

    selected_file = conn.recv(BUFFER_SIZE).decode()
    filepath = os.path.join(TEST_FOLDER, selected_file)

    if not os.path.exists(filepath):
        conn.send("FILE_NOT_FOUND".encode())
        print(f"[!] File '{selected_file}' not found.")
        conn.close()
        continue
    else:
        conn.send("FILE_FOUND".encode())
        print(f"[→] Sending '{selected_file}' to client...")
        with open(filepath, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                conn.sendall(bytes_read)

        print(f"[✓] File '{selected_file}' sent successfully.")
    conn.close()
