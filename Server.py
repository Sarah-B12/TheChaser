import socket
import select
import Questions
import random

HOST = ''
PORT = 65433

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(3)

run_server = True
connected_clients = []

while run_server:
    asked_connections, wlist, xlist = select.select([s], [], [], 0.05)
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Welcome to the game! Do you want to play?", "utf-8"))

    for connection in asked_connections:
        connection_with_client, infos_connection = connection.accept()
        connected_clients.append(connection_with_client)

    clients_to_read = []
    try:
        clients_to_read, wlist, xlist = select.select(connected_clients, [], [], 0.05)
    except select.error:
        pass
    else:
        # We go through the list of clients to read
        for client in clients_to_read:
            msg_received = client.recv(1024)
            msg_received = msg_received.decode()
            print("Reçu {}".format(msg_received))
            client.send(b"5 / 5")
            if msg_received == "no":
                run_server = False

print("Close connections")
for client in connected_clients:
    client.close()

s.close()


def ask_question(lvl):
    # Generates a number and gets the question from the database
    qnum = int(random.random() * 10)

    global q
    q = Questions.get_question(lvl, qnum)
    to_return = q[0]
    to_return += "\n A. " + q[1] + "\t\t B. " + q[2]
    to_return += "\n C. " + q[3] + "\t\t D. " + q[4]

    global correct_answer
    correct_answer = q[5]
    return to_return