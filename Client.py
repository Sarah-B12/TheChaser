import socket
import argparse

'''
Money=0
def get_money:
     return Money

def answer_questions:
    answer= input("choose an answer")
    s.send(answer.encode())


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

'''


parser = argparse.ArgumentParser(description="This is the client for the multi threaded socket server!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=65433)
args = parser.parse_args()

print(f"Connecting to server: {args.host} on port: {args.port}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
    try:
        sck.connect((args.host, args.port))
    except Exception as e:
        raise SystemExit(f"We have failed to connect to host: {args.host} on port: {args.port}, because: {e}")

firstlevel = 0
while True:
    welcome_msg = sck.recv(1024)
    print(welcome_msg.decode("utf-8"))
    msg = input("> ")
    sck.send(msg.encode('utf-8'))
    if msg == 'no':
        print("Bye!")
        break
    while True:
        firstq = sck.recv(1024)
        print(f"{firstq.decode()}")
        firstansw = input("> ")
        sck.send(firstansw.encode('utf-8'))

