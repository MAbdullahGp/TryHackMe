import socket
HOST = "10.49.169.204"
PORT = 29536
s = socket.create_connection((HOST, PORT))
print(s.recv(1024).decode())
s.sendall(b"< open vcan0 >\n")
print(s.recv(1024).decode())
s.sendall(b"< rawmode >\n")
while True:
    data = s.recv(4096)
    if data:
        print(data.decode(errors="ignore"))