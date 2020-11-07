import socket
import selectors
import select
import Questions
import random
import types


def accept_wrapper(sock):  # get the new socket object and register it with the selector.
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False) # put the socket in non-blocking mode
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'') # hold the data we want included along with the socket
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data) # The events mask, socket, and data objects are passed


def service_connection(key, mask):  # Client connection handler when it’s ready
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:  # Socket ready for reading
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:  # block if no data is received
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


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



HOST = ''
PORT = 65433

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(3)
s.setblocking(False) # Socket in non-blocking mode

run_server = True
connected_clients = []

while run_server:
    events = sel.select(timeout=None) # returns a list of (key, events) tuples, one for each socket.
    for key, mask in events:
        if key.data is None: # we know it’s from the listening socket and we need to accept() the connection.
            accept_wrapper(key.fileobj)
        else: # it’s a client socket that’s already been accepted, and we need to service it
            service_connection(key, mask)




'''
while run_server:
    asked_connections, wlist, xlist = select.select([s], [], [], 0.05)
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Welcome to the game! Do you want to play?", "utf-8"))

    for connection in asked_connections:
        connection_with_client, infos_connection = connection.accept() # PROBLEM
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

'''


print("Close connections")
for client in connected_clients:
    client.close()

s.close()


