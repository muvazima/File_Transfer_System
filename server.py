import socket
import sys
import os.path
import operator

serverPort = int(input("Enter the Server Port[3500]: ") or 3500)
#create socket object for server
#AF_INET refers to the address family ipv4. The SOCK_STREAM means connection oriented TCP protocol.
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('',serverPort)) #socket is bound to localhost and port 3500

serverSocket.listen(1) #accepting up to 2 incoming connections

print ('Server is listening...')
print (socket.gethostname())

while True:

    #return value of accept() is assigned to socket object
    #and address bound to that socket
    connectionSocket, addr = serverSocket.accept()
    
    #connection established with client
    print ('Got connection from', addr)

    #waiting for GET or SEND command from client
    print ('Awaiting command from client...')
    client_request = connectionSocket.recv(1024)
    #convert from byte object so we can read as string
    request_str = client_request.decode("utf-8")


    #server receives GET command from client and reads from file to be sent back
    #to client after they input the filename
    if request_str == 'GET':
        print('Received GET command from client. Waiting for filename.')

        client_request = connectionSocket.recv(1024)        


        file_name = client_request.decode("utf-8")

        f = open(file_name, "rb")
        print('Sending file...')
        l = f.read(1024)
        while(l):
            connectionSocket.send(l)
            l = f.read(1024)
        f.close()
        print('Done sending')

    #server receives SEND command from client and creates file to be received
    #by the client
    elif request_str == 'SEND':
        print('Received SEND command from client. Awaitng filename')
        client_request = connectionSocket.recv(1024)
        file_name = client_request.decode("utf-8")

        f = open("fromClient_" + file_name, "wb")
        print('Receiving file from client..')
        l = connectionSocket.recv(1024)
        while(l):
            f.write(l)
            l = connectionSocket.recv(1024)
        f.close()
        print('Done receiving file')
        
    elif request_str =='LIST':
        fileList=os.listdir(os.getcwd())
        for file in fileList:
            f = file+"\n"
            connectionSocket.send(f.encode("utf-8"))
        print('Done sending')

    connectionSocket.close()