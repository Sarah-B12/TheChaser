import socket
import argparse

parser = argparse.ArgumentParser(description="This is the client for the multi threaded socket server!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=65433)
args = parser.parse_args()

acceptable_answers = ["a", "b", "c", "d"]

print(f"Connecting to server: {args.host} on port: {args.port}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
    try:
        sck.connect((args.host, args.port))
    except Exception as e:
        raise SystemExit(f"We have failed to connect to host: {args.host} on port: {args.port}, because: {e}")

    while True:
        welcome_msg = sck.recv(1024)
        print(welcome_msg.decode("utf-8"))
        msg = input("> ")
        sck.sendall(msg.encode('utf-8'))
        if msg == 'no':
            print("Bye!")
            break
        # FIRST PART QUESTIONS
        for i in range(0, 3):
            j = i+1
            print("Question number %s :" % j)
            question = sck.recv(1024)  # In function ask_question
            print(question.decode("utf-8"))
            answ = input("> ")
            sck.sendall(answ.encode('utf-8'))
            answer = answ.lower()
            while not (answer in acceptable_answers):
                redo = sck.recv(1024)
                print("In while not")  # TO ERASE
                print(redo.decode("utf-8"))
                answ = input("> ")
                sck.sendall(answ.encode('utf-8'))
                answer = answ.lower()
            right_or_wrong = sck.recv(1024)
            print(right_or_wrong.decode("utf-8"))
            print("HERE")  # TO ERASE
