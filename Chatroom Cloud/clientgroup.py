import time, socket, sys,threading
 
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 3040
 
print('This is your IP address: ',ip)
server_host = input('Enter server IP address:')
nickname = input("Choose your nickname: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((server_host, sport))                            #connecting client to server


def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break
def write():
    while True:                                                 #message layout
        print("You: ")
        x = input("")
        message = '{}: {}'.format(nickname, x)
        client.send(message.encode('ascii'))

write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()
receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
