import socket
from _thread import *
import random
import Questions
from Player import Player
from SmartChaser import SmartChaser


def ask_question(lvl, qnum, with_joker):
    # Gets the question from the database
    global q
    q = Questions.get_question(lvl, qnum)
    print(q)
    to_return = q[0]

    to_return += "\n A. " + q[1] + "\t\t B. " + q[2]
    to_return += "\n C. " + q[3] + "\t\t D. " + q[4]

    if with_joker:
        to_return += "\nYou can also type 'joker'."

    client.send(to_return.encode('utf-8'))

    global correct_answer
    correct_answer = q[5]
    return


def check_answer(answer, with_joker):
    if with_joker and answer == "joker":  # If the player use his joker
        player.clr_joker()  # Joker now set to false
        acceptable_answers.remove('joker')  # Remove 'joker' in the acceptable answers
        joker_answers = [q[5]]
        mylist = [q[1], q[2], q[3], q[4]]
        choice = random.choice(mylist)
        while choice == q[5]:
            choice = random.choice(mylist)  # Chose randomly one of the other answer
        joker_answers.append(choice)
        # random.shuffle(joker_answers)  # Shuffle between the two elements of the list

        joker_used = f"You used your joker. The two possible answers are:\nA. {joker_answers[0]}\nB. {joker_answers[1]}"
        client.send(joker_used.encode('utf-8'))
        msg = client.recv(1024)  # Answer of the player (when joker)
        answer = msg.decode()
        answer = answer.lower()
        if answer == "a":
            player.step_plus_one()
            right = "You're right! Bravo!"
            client.send(right.encode('utf-8'))
        else:
            wrong = "The answer you chose is incorrect and you don't have your joker anymore."
            client.send(wrong.encode('utf-8'))

    else:
        while not (answer in acceptable_answers):  # Checking if the input makes sens
            redo = "I don't understand what you mean. Enter the answer letter"
            client.send(redo.encode('utf-8'))
            answer = (client.recv(1024)).decode()
            answer = answer.lower()
        if (answer == "a" or answer == "b" or answer == "c" or answer == "d"):
            if (correct_answer == q[ord(answer) - 96]):  # unicode table char (a=97, b=98...)
                right = f"You're right! Bravo!"
                if part_2:
                    player.step_plus_one()
                    right = right + f"\nYou are now in step {player.get_step()}"
                client.send(right.encode('utf-8'))
                if not part_2:
                    player.add_wallet()
            else:
                wrong = "The answer you chose is incorrect."
                client.send(wrong.encode('utf-8'))
        return



def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    q1 = 0
    global acceptable_answers, qnum
    global ThreadCount
    print(f"The new connection was made from IP: {ip}, and port: {port}!")
    while True:
        global player
        player = Player()
        if ThreadCount > 3:
            not_welcome = "Sorry we already have too much players. Try later"
            client.send(not_welcome.encode('utf-8'))
            print("Client refused")
            break
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
            j = i + 1
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
        choice = """ Now choose between the next 3 options:
1. Start from step 3 with your current wallet.
2. Start from previous step with the double of your wallet.
3. Start from next step with half of your wallet."""
        client.send((money + choice).encode('utf-8'))

        answer_choice = (client.recv(1024)).decode("utf-8")

        while answer_choice not in ("1", "2", "3"):
            redo = "It is not an acceptable answer. Choose between 1, 2 or 3"
            client.send(redo.encode('utf-8'))
            answer_choice = client.recv(1024)
            answer_choice = answer_choice.decode("utf-8")
        player.change_wallet_step(answer_choice)

        acceptable_answers.append('joker')

        # SECOND PART WITH CHASER
        part_2 = True
        chaser = SmartChaser()
        player.set_joker()  # Now the player can use his joker

        k = 1
        while 7 > player.get_step() > chaser.get_step():
            qnum = int(random.random() * 10)
            # TODO : qnum be different everytime
            print("Asking question %s ..." % k)
            ask_question(1, qnum, player.get_joker())
            k += 1
            msg = client.recv(1024)  # Answer of the player
            answer = msg.decode()
            check_answer(answer, player.get_joker())

            sthg = client.recv(1024)
            print(sthg.decode("utf-8"))

            chaser_answ = chaser.chaser_answer(qnum)
            if chaser_answ:
                chaser_response = "The chaser was right."
                chaser.step_plus_one()
            else:
                chaser_response = "The chaser was wrong."

            chaser_response += f"""\nThe user wallet is {player.get_wallet()}.
The user step is {player.get_step()}.
The chaser step is {chaser.get_step()}.
The joker has {'not ' if player.get_joker() else ''}been used."""

            if player.get_step() == 7:
                chaser_response += "\nPlayer has WON."
            elif chaser.get_step() == player.get_step():
                chaser_response += "\nChaser has WON."

            client.send(chaser_response.encode('utf-8'))

            sthg2 = client.recv(1024)
            print(sthg2.decode("utf-8"))


    print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()
    ThreadCount -= 1



sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 65530
ThreadCount = 0
all_connections = []
all_address = []

try:
    sck.bind((host, port))
    print("Waiting for connection")
    sck.listen(3)
except Exception as e:
    raise SystemExit(f"We could not bind the server because: {e}")

# Close all connections that were before
for c in all_connections:
    c.close()
del all_connections[:]
del all_address[:]

while True:
    try:
        client, ip = sck.accept()
        all_connections.append(client)
        all_address.append(ip)
        start_new_thread(on_new_client, (client, ip))
        ThreadCount += 1
        print("Thread Count = " + str(ThreadCount))
    except KeyboardInterrupt:
        print(f"Gracefully shutting down the server!")
    except Exception as e:
        print(f"Well I did not anticipate this: {e}")

sck.close()
