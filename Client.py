import socket

PORT = 65432        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT))

msg = s.recv(1024)
print(msg.decode("utf-8"))