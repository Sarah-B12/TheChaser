import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
while True:
    msg = conn.recv(1024) # accept the message
    print('Received: ' + msg.decode())
    msg = input()
    conn.send(msg.encode())

conn.close()

