import socket

HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()


while True: # listen forever
    msg = input()
    conn.send(msg.encode())
    msg = conn.recv(1024)
    print('Received: ' + msg.decode())

conn.close()
s.close()