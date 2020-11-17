import socket
import argparse
import threading
import random
import Questions
import SmartChaser


def ask_question(lvl, qnum, with_joker):
    acceptable_answers = []
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
    global correct_answer, q
    global wallet
    global player_step
    # wallet = 0
    if with_joker and answer == "joker":
        global joker_used
        joker_used = True
        acceptable_answers.remove('joker')
        joker_answers = [q[5]]

        for possible_answer in [q[1], q[2], q[3], q[4]]:
            if possible_answer != q[5]:
                joker_answers.append(possible_answer)
                break

        client.send(f"""You used your joker. The two possible answers are:
A. {joker_answers[0]}
B. {joker_answers[1]}
    """.encode('utf-8'))

        msg = client.recv(1024)  # Answer of the player
        answer = msg.decode()
        answer = answer.lower()
        if answer == "a":
            player_step += 1
            right = "You're right! Bravo!"
            client.send(right.encode('utf-8'))
        else:
            wrong = "The answer you chose is incorrect."
            client.send(wrong.encode('utf-8'))

    else:
        answer = answer.lower()
        if not (answer in acceptable_answers):  # Checking if the input makes sens
            reply = "I don't understand what you mean. Enter the answer letter"
            client.send(reply.encode('utf-8'))
        if (answer == "a" or answer == "b" or answer == "c" or answer == "d"):
            if (correct_answer == q[ord(answer) - 96]): # unicode table char (a=97, b=98...)
                player_step += 1
                right = f"""You're right! Bravo!
You are now in step {player_step}."""
                client.send(right.encode('utf-8'))
                wallet += 5000
            else:
                wrong = "The answer you chose is incorrect."
                client.send(wrong.encode('utf-8'))
        return


parser = argparse.ArgumentParser(description="This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=65433)
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

def chaser_answer(lvl, qnum):
    global correct_answer, q
    global chaser_step
    q = Questions.get_question(lvl, qnum)
    answer = SmartChaser.chose_answer(q)
    if answer == True:
        return True
    else:
        return False
    #if (correct_answer == q[ord(answer) - 96]):
       # chaser_step+=1
        #return True
    #else:
        #return False




def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    q1 = 0
    q2 = 0
    global acceptable_answers
    print(f"THe new connection was made from IP: {ip}, and port: {port}!")
    while True:
        welcome = f"Welcome to the game! Do you want to play?"
        client.send(welcome.encode('utf-8'))
        msg = client.recv(1024)
        if msg.decode() == 'no':
            break
        print("The player wants to play!")
        # FIRST PART QUESTIONS
        acceptable_answers = ["a", "b", "c", "d"]
        global player_step
        player_step = 0
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
            ask_question(0, qnum,False)
            msg = client.recv(1024)  # Answer of the player
            answer = msg.decode()
            check_answer(answer, False)
            # For the server to recv between two send
            sthg = client.recv(1024)
            print(sthg.decode("utf-8"))
        global wallet
        player_step = 3
        if wallet == 0:
            print("This guy is so dumb...")
            money = "You answer it all wrong! Try again."
            client.send(money.encode('utf-8'))
            player_step = 0
            continue
        else:
            print("%s" % wallet)
            money = f"Your wallet is {wallet}. You are now at step 3."
        global chaser_step
        chaser_step = 0
        choice = """Now choose between the next 3 options:
1. Start from step 3 with the current sum.
2. Start from previous step with the double of the sum.
3. Start from next step with half of the sum."""
        client.send((money + choice).encode('utf-8'))

        answer_choice = "0"
        while answer_choice not in ("1", "2", "3"):
            answer_choice = client.recv(1024)
            answer_choice = answer_choice.decode("utf-8")
            if answer_choice == "1":
                pass
            elif answer_choice == "2":
                player_step -= 1
                wallet *= 2
            elif answer_choice == "3":
                player_step += 1
                wallet /= 2
            else:
                client.send("Please enter a correct choice (1, 2 or 3).".encode('utf-8'))

        acceptable_answers.append('joker')
# partie ou il joue avec le chaser
        global joker_used
        joker_used = False  # Au debut le joker n'est pas utilise.

        while player_step < 7 and chaser_step < player_step:
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

            chaser_answ = chaser_answer(1, qnum)
            if chaser_answ == True:
                chaser_response = "The chaser was right."
                chaser_step += 1
            else:
                chaser_response = "The chaser was wrong."

            chaser_response += f"""\nThe user wallet is {wallet}.
The user step is {player_step}.
The chaser step is {chaser_step}.
The joker has {'not' if not joker_used else ''} been used."""

            if player_step == 7:
                chaser_response += "\nPlayer has WON."
            elif chaser_step == player_step:
                chaser_response += "\nChaser has WON."

            client.send(chaser_response.encode('utf-8'))



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
