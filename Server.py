import socket
import argparse
import threading
import random
import Questions

'''
def first_lvl:
    #first part of the game: the client recieve 3questions of the first level
        counter = 0
        num=3
        while num!=0:
           for client in clients_to_read:
              qnum=ask_question(1)
              answer=client.recv(1024)
              answer=answer.decode
              good_answer = Questions.get_answer(qnum,1)

            if answer == good_answer
                counter++

            switch(counter)
              case 0 : message = "ZERO-RESTART"
                       printf(message)
                       client.send(message.encode())
              case 1 : message ="5000-next level"
                       printf(message)
                       client.send(message.encode())
              case 2 : message = "10000 next level"
                       printf(message)
                       client.send(message.encode())
              case 3:  message ="15000 next level"
                       printf(message)
                       client.send(message.encode())

'''


def ask_question(lvl):
    # Generates a number and gets the question from the database
    qnum = int(random.random() * 10)

    global q
    q = Questions.get_question(lvl, qnum)
    to_return = q[0]

    to_return += "\n A. " + q[1] + "\t\t B. " + q[2]
    to_return += "\n C. " + q[3] + "\t\t D. " + q[4]
    print("The question is: {}".format(to_return))

    global correct_answer
    correct_answer = q[5]
    return qnum


def check_answer(lvl):
    global correct_answer, q
    msg = client.recv(1024)
    answer = msg.decode()
    answer = answer.lower()
    if not (answer in acceptable_answers):  # Checking if the input makes sens
        reply = "I don't understand what you mean. Enter the answer letter"
        client.send(reply.encode('utf-8'))
        check_answer(lvl)
    elif (answer == "a" or answer == "b" or answer == "c" or answer == "d"):
        if (correct_answer == answer):
            print("TO DO TO DO TO DO TO DO TO DO")
        else:
            print("\n The answer you chose is incorrect.\n The right answer is %s." % correct_answer)



parser = argparse.ArgumentParser(description="This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=65433)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
acceptable_answers = ["a", "b", "c", "d", "A", "B", "C", "D"]

try:
    sck.bind((args.host, args.port))
    sck.listen(3)
except Exception as e:
    raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")


def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    print(f"The new connection was made from IP: {ip}, and port: {port}!")
    while True:  # Reboucle à welcome to the game
        welcome = f"Welcome to the game! Do you want to play?"
        client.send(welcome.encode('utf-8'))
        msg = client.recv(1024)
        if msg.decode() == 'no':
            break
        print(f"The client said: {msg.decode()}")
        reply = f"Let's start!"
        client.send(reply.encode('utf-8'))



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