# 🔐 Secure Network File Sharing System

Hey there 👋  
This project is my take on building a **secure client-server file sharing system** from scratch using Python.  
It was developed as part of my **Wipro Capstone Assignment (LSP)** — and it focuses on networking, encryption, authentication, and clean modular design.

---

## 🚀 Overview

The system allows multiple clients to **upload encrypted files** to a central server securely over sockets.  
The server handles **authentication**, **decryption**, and **logging** — making it a mini real-world secure file transfer system.

I’ve broken down the development into stages (like we did in the assignment), improving functionality step by step — from basic socket communication to full-blown encrypted file transfer with authentication.

---

## ⚙️ Features

✅ **Client-Server Architecture**  
Simple TCP connection using Python’s `socket` module.

✅ **User Authentication**  
Each user logs in with a username and password.  
Passwords are hashed using **SHA-256** (so no plaintext anywhere).

✅ **Encrypted File Transfer**  
Files are encrypted with **Fernet symmetric encryption** (from the `cryptography` library).  
Even if intercepted, no one can read the file contents.

✅ **Upload Progress Bar**  
Shows real-time upload progress on the client side with `tqdm`.

✅ **Activity Logs**  
Every login, upload, or failed attempt is stored in `server/logs/activity.log`.

✅ **Add User Utility**  
Comes with a simple CLI tool (`add_user.py`) to add new users safely with hashed passwords.

✅ **Modular Structure**  
Clean folder separation for `client`, `server`, and `utils`, so everything’s easy to manage and extend later.

---

## 🧩 Folder Structure
Finished_Version/
│
├── client/
│ ├── uploads/ # Files to send
│ ├── downloads/ # (Optional future feature)
│ └── client.py
│
├── server/
│ ├── uploads/ # Received + decrypted files
│ ├── shared_files/ # Placeholder for future use
│ ├── logs/ # Contains activity.log
│ ├── users.txt # Username:hashed_password list
│ └── server.py
│
├── utils/
│ ├── config.py # Configuration (host, port, buffer size)
│ └── encryption.py # Handles key generation + encryption logic
│
├── add_user.py # CLI tool to add new users
├── README.md 
└── requirements.txt # Dependencies list

## Technologies used
Purpose	              Technology
Networking	  -       Python socket
Encryption	  -       cryptography (Fernet)
Progress Bar  -       tqdm
Password Security	- hashlib (SHA-256)
Logging	File-based  - event logs