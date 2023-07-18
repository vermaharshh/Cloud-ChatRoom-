import time, socket, sys,threading
 
server = socket.socket()
host_name = socket.gethostname()
s_ip = socket.gethostbyname(host_name)
 
port = 3040
 


server.bind((host_name, port))
print("Binding successful!")
print("This is your IP: ", s_ip)
 
name = input('Enter name: ')
 
server.listen(1) 
clients = []
nicknames = []
pp = {}


def private(message):
    x = message
    neww = str(x.decode("ascii"))
    index = neww.index("@") + 1
    neww = neww[index:]
    for x in nicknames:
        if neww.startswith(str(x)):
            client = pp[x]
            client.send(message)


def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            x = message
            test = x.decode("ascii")
            print(test)
            if "@" in test:
                private(message)
            else:
                broadcast(message)
        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():                                                          #accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        pp[nickname] = client
        print("Client name is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()