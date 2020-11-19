import socket
import argparse

parser = argparse.ArgumentParser(description="This is the client for the multi threaded socket server!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=65430)
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
            # For the client to send between two recv
            sthg = "Receive"
            sck.sendall(sthg.encode('utf-8'))
            print("HERE")  # TO ERASE

        choice = "0"
        while choice not in ("1", "2", "3"):
            message = sck.recv(1024)
            print(message.decode("utf-8"))
            choice = input("> ")
            sck.sendall(choice.encode('utf-8'))

#      #start playing with the chaser
        chaser_response = ""
        while "WON" not in chaser_response:
            question = sck.recv(1024)  # In function ask_question
            print(question.decode("utf-8"))
            answ = input("> ")
            sck.sendall(answ.encode('utf-8'))
            answer = answ.lower()
            if answer != "joker" :
                while not (answer in acceptable_answers) and answer != "joker":
                    redo = sck.recv(1024)
                    print("In while not")  # TO ERASE
                    print(redo.decode("utf-8"))
                    answ = input("> ")
                    sck.sendall(answ.encode('utf-8'))
                    answer = answ.lower()


            if answ == "joker":
                possible_answers_joker = sck.recv(1024)  # In function ask_question
                print(possible_answers_joker.decode("utf-8"))
                joker_answer = input("> ")
                sck.sendall(joker_answer.encode('utf-8'))

            right_or_wrong = sck.recv(1024)
            print(right_or_wrong.decode("utf-8"))
            sthg = "Receive"
            print("send sthg")
            sck.sendall(sthg.encode('utf-8'))
            # Test

            #reponse du chaser
            chaser_response = sck.recv(1024).decode("utf-8")
            print(chaser_response)


