import socket
import os

HOST = '127.0.0.1'
PORT = 5050
BUFFER_SIZE = 4096
SHARED_FOLDER = 'test_files'   # renamed from shared_files to test_files

# Ensure test_files folder exists
if not os.path.exists(SHARED_FOLDER):
    os.makedirs(SHARED_FOLDER)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[*] Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"[+] Connected to client: {addr}")

    # List available files
    files = os.listdir(SHARED_FOLDER)
    if not files:
        file_list = "No files available."
    else:
        # Optional enhancement: include file sizes for realism
        file_list = "\n".join(
            [f"{f} ({os.path.getsize(os.path.join(SHARED_FOLDER, f))} bytes)" for f in files]
        )

    conn.send(file_list.encode())

    # Receive requested filename
    selected_file = conn.recv(BUFFER_SIZE).decode()
    filepath = os.path.join(SHARED_FOLDER, selected_file)

    if not os.path.exists(filepath):
        conn.send("FILE_NOT_FOUND".encode())
        print(f"[!] File '{selected_file}' not found in test_files.")
        conn.close()
        continue
    else:
        conn.send("FILE_FOUND".encode())
        print(f"[→] Sending file '{selected_file}'...")

        with open(filepath, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                conn.sendall(bytes_read)

        print(f"[✓] File '{selected_file}' sent successfully.")

    conn.close()
