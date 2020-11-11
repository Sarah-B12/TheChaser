import socket
import argparse
import threading
import random
import Questions


def ask_question(lvl):
    # Generates a number and gets the question from the database
    qnum = int(random.random() * 10)

    global q
    q = Questions.get_question(lvl, qnum)
    to_return = q[0]

    to_return += "\n A. " + q[1] + "\t\t B. " + q[2]
    to_return += "\n C. " + q[3] + "\t\t D. " + q[4]
    client.send(to_return.encode('utf-8'))

    global correct_answer
    correct_answer = q[5]
    return qnum


def check_answer():
    global correct_answer, q
    msg = client.recv(1024)
    answer = msg.decode()
    answer = answer.lower()
    if not (answer in acceptable_answers):  # Checking if the input makes sens
        reply = "I don't understand what you mean. Enter the answer letter"
        client.send(reply.encode('utf-8'))
        check_answer()
    elif (answer == "a" or answer == "b" or answer == "c" or answer == "d"):
        if (correct_answer == q[ord(answer) - 96]): # unicode table char (a=97, b=98...)
            right = "You're right! Bravo!"
            client.send(right.encode('utf-8'))
            # wallet += 5000
            # PROBLEM : Renvoie la prochaine question mais pas le message "right"
        else:
            wrong = "The answer you chose is incorrect."
            client.send(wrong.encode('utf-8'))
            # PROBLEM : Ne renvoie pas la prochaine question si wrong
    return


parser = argparse.ArgumentParser(description="This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=65433)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
acceptable_answers = ["a", "b", "c", "d"]

try:
    sck.bind((args.host, args.port))
    sck.listen(3)
except Exception as e:
    raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")


def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    global wallet
    print(f"THe new connection was made from IP: {ip}, and port: {port}!")
    while True:
        welcome = f"Welcome to the game! Do you want to play?"
        client.send(welcome.encode('utf-8'))
        msg = client.recv(1024)
        if msg.decode() == 'no':
            break
        print("The player wants to play!")
        for i in range(0, 3):
            j = i+1
            print("Asking question %s ..." % j)
            qnum = ask_question(0)
            check_answer()
        if wallet == 0:
            print("This guy is so dumb...")

    print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()


while True:
    try:
        client, ip = sck.accept()
        threading._start_new_thread(on_new_client, (client, ip))
    except KeyboardInterrupt:
        print(f"Gracefully shutting down the server!")
    except Exception as e:
        print(f"Well I did not anticipate this: {e}")

sck.close()
