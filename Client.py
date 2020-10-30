import socket

PORT = 65433        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT))

welcome_msg = s.recv(1024)
print(welcome_msg.decode("utf-8"))

msg_to_send = b""
while msg_to_send != b"end":
    msg_to_send = input()
    s.send(msg_to_send.encode())
    msg_received = s.recv(1024)
    print(msg_received.decode())

print("Connection closed")
s.close()