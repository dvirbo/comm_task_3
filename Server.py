# import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
'''
SOCK_STREAM: Connection type (TCP)
AF_INET: Internet protocol (IPv4)
'''

# Prepare a sever socket:
serverPort = 6789
# Listen to all IP’s on this computer:
serverSocket.bind(('0.0.0.0', serverPort))
# Server only handles one connection at a given time. ‘1’ is a number of incoming connections are waiting in the queue.
serverSocket.listen(1)
print('server is up on port:', serverPort)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # Wait for client connection
    try:
        message = connectionSocket.recv(1024)  # read bytes from the Socket
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        # Send one HTTP header line into socket

        connectionSocket.send('\nHTTP/1.1 200 OK\n\n'.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        connectionSocket.send("\nHTTP/1.1 404 Not Found\n\n".encode())

        connectionSocket.close()  # Close client socket

        serverSocket.close()  # # Close main socket
    finally:
        sys.exit()  # Terminate the program after sending the corresponding data
