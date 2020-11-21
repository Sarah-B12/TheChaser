import socket
import argparse
import threading
import numpy as np
import random
import Questions
from Player import Player
from SmartChaser import SmartChaser


def ask_question(lvl, qnum, with_joker):
    # Gets the question from the database
    print("Je suis ask_question")  # TO ERASE
    global q
    q = Questions.get_question(lvl, qnum)
    to_return = q[0]

    to_return += "\n A. " + q[1] + "\t\t B. " + q[2]
    to_return += "\n C. " + q[3] + "\t\t D. " + q[4]

    if with_joker:
        to_return += "\n You can also type 'joker'."
    client.send(to_return.encode('utf-8'))

    global correct_answer
    correct_answer = q[5]
    return to_return


def check_answer(answer, with_joker):
    # global correct_answer, q
    if with_joker and answer == "joker":  # If the player use his joker
        player.set_joker()
        acceptable_answers.remove('joker')
        joker_answers = [q[5]]  # Put the right answer in the list
        mylist = [q[1], q[2], q[3], q[4]]
        answer = np.random.choice(mylist, 1, p=[0.25, 0.25, 0.25, 0.25])  # Chose randomly one of the other answer
        joker_answers.append(answer)
        random.shuffle(joker_answers)  # Shuffle between the two elements of the list

        client.send(f"""You used your joker. The two possible answers are:
A. {joker_answers[0]}
B. {joker_answers[1]}
    """.encode('utf-8'))
        # TODO : CHECK THIS
        msg = client.recv(1024)  # Answer of the player (when joker)
        answer = msg.decode()
        answer = answer.lower()
        if answer == "a":
            player.step_plus_one()
            right = "You're right! Bravo!"
            client.send(right.encode('utf-8'))
        else:
            wrong = "The answer you chose is incorrect."
            client.send(wrong.encode('utf-8'))

    else:
        while not (answer in acceptable_answers):  # Checking if the input makes sens
            redo = "I don't understand what you mean. Enter the answer letter"
            client.send(redo.encode('utf-8'))
            answer = (client.recv(1024)).decode()
            answer = answer.lower()
        if (answer == "a" or answer == "b" or answer == "c" or answer == "d"):
            if (correct_answer == q[ord(answer) - 96]): # unicode table char (a=97, b=98...)
                right = f"You're right! Bravo!"
                if part_2:
                    player.step_plus_one()
                    right = right + "You are now in step " + {player.get_step()}
                client.send(right.encode('utf-8'))
                player.add_wallet()
            else:
                wrong = "The answer you chose is incorrect."
                client.send(wrong.encode('utf-8'))
        return




parser = argparse.ArgumentParser(description="This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=65430)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
wallet = 0

try:
    sck.bind((args.host, args.port))
    sck.listen(3)
except Exception as e:
    raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")


def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    q1 = 0
    q2 = 0
    global acceptable_answers
    print(f"THe new connection was made from IP: {ip}, and port: {port}!")
    while True:
        global player
        player = Player()
        welcome = f"Welcome to the game! Do you want to play?"
        client.send(welcome.encode('utf-8'))
        msg = client.recv(1024)
        if msg.decode() == 'no':
            break
        print("The player wants to play!")
        # FIRST PART QUESTIONS
        global part_2
        part_2 = False
        acceptable_answers = ["a", "b", "c", "d"]
        for i in range(0, 3):
            j = i+1
            print("Asking question %s ..." % j)
            # Check that the progr. don't ask the same question
            if j == 1:
                qnum = int(random.random() * 10)
            elif j == 2:
                q1 = qnum
                while (q1 == qnum):
                    qnum = int(random.random() * 10)
            elif j == 3:
                q2 = qnum
                while (q2 == qnum or q1 == qnum):
                    qnum = int(random.random() * 10)
            ask_question(0, qnum, player.get_joker())
            msg = client.recv(1024)  # Answer of the player
            answer = msg.decode()
            answer = answer.lower()
            check_answer(answer, player.get_joker())
            # For the server to recv between two send
            sthg = client.recv(1024)
            print(sthg.decode("utf-8"))

        if player.get_wallet() == 0:
            print("This guy is so dumb...")
            money = "You answer it all wrong! Try again."
            client.send(money.encode('utf-8'))
            continue
        else:
            print("%s" % player.get_wallet())
            money = f"Your wallet is {player.get_wallet()}. You are now at step 3."
        #global chaser_step
        #chaser_step = 0
        choice = """Now choose between the next 3 options:
1. Start from step 3 with the current sum.
2. Start from previous step with the double of the sum.
3. Start from next step with half of the sum."""
        client.send((money + choice).encode('utf-8'))

        answer_choice = (client.recv(1024)).decode("utf-8")

        while answer_choice not in ("1", "2", "3"):
            redo = "It is not an acceptable answer. Choose between 1, 2 or 3"
            redo = client.send(redo.encode('utf-8'))
            answer_choice = client.recv(1024)
            answer_choice = answer_choice.decode("utf-8")
        player.change_wallet_step(answer_choice)

        '''
        acceptable_answers.append('joker')

        # SECOND PART WITH CHASER
        part_2 = true
        chaser = SmartChaser()
        global joker_used
        joker_used = False  # Au debut le joker n'est pas utilise.

        while 7 > player_step > chaser.get_step():
            qnum = int(random.random() * 10)
            ask_question(1, qnum, not joker_used)
            # Premiere fois on rentre dans la function avec possibilite de l'utiliser
            # Si il a ete utilise, joker_used = True et donc on envoie False pour les prochaines fois.

            answer = ""

            msg = client.recv(1024)  # Answer of the player
            answer = msg.decode()
            check_answer(answer, not joker_used)

            print("receive sthg")
            sthg = client.recv(1024)
            print(sthg.decode("utf-8"))
            # Test

            chaser_answ = chaser.chaser_answer(1, qnum)
            if chaser_answ:
                chaser_response = "The chaser was right."
                chaser.step_plus_one()
            else:
                chaser_response = "The chaser was wrong."

            chaser_response += f"""\nThe user wallet is {wallet}.
The user step is {player_step}.
The chaser step is {chaser.get_step()}.
The joker has {'not' if not joker_used else ''} been used."""

            if player_step == 7:
                chaser_response += "\nPlayer has WON."
            elif chaser.get_step() == player_step:
                chaser_response += "\nChaser has WON."

            client.send(chaser_response.encode('utf-8'))

'''

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
