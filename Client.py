import socket


HOST = "localhost"
PORT = 65433        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

welcome_msg = s.recv(1024)
print(welcome_msg.decode("utf-8"))

msg_to_send = b""
while msg_to_send != b"no":
    msg_to_send = input()
    s.send(msg_to_send.encode())
    msg_received = s.recv(1024)
    print(msg_received.decode())

def answer_questions:
    answer= input("choose an answer")
    s.send(answer.encode())



print("Connection closed")
s.close()

Money=0
 def get_money:
     return Money

def first_level
    msg_received2 = s.recv(1024)
    if msg_received2 == "ZERO-RESTART"
        Money = 0
    if msg_received2 == "5000-next level"
        Money = 5000
    if msg_received2 == "10000 next level"
        Money= 10000
    if msg_received2 == "15000 next level"
        Money = 15000