# Nichole Maldonado
# This file holds code for a server
# that sends a file to a connected client
# 1000 bytes at a time.

import socket
import threading
import sys
import os.path
from lib.utils import str_to_pos_int

# Class that runs the server that creates a 
# TCP socket and listens for client requests
# When a client requests to connect and the
# handshake is performed, the connection is
# established and the server will create a
# new thread. This new thread will send a 1000 bytes
# at a time of the file provided (bio.txt)
class Server:
    # Max number of clients that this server
    # can listen out for.
    MAX_NUM_CLIENTS = 100
    
    # Number of bytes a server socket sends at a time
    NUM_BYTES = 1000
    
    # Creates blank server that needs to be setup
    # Input: None
    # Output: None
    def __init__(self):
        # Port that this server will be using.
        self.port = None
        
        # Socket that will listen out to requests to connect
        self.socket = None
        
        # Path of the file. Must be included as an arg!
        # This allows users to run the server sending any
        # type of file (more flexible). Also in doing so
        # bio.txt can be saved anywhere, and not just in 
        # current folder that the program resides in.
        self.file_path = None
    
    # Sends a file at file_path to the client at client_addr 
    # through the server_socket.
    # Input: The file that will be sent to the client,
    #        the client's socket address, and the server socket.
    #        NOTE: since we have a TCP connection, the client's 
    #        socket address is used to print out only and used
    #        used for actually send()ing the file.
    # Output: None.
    @staticmethod
    def send_file(file_path, client_addr, server_socket):
        print("Server: Starting to send file to client", client_addr)
        print()
        try:
            # Try to read the file.
            with open(file_path, "r") as fd:
                bytes_read = b'1'
                
                # Continue to send 1000 bytes of the file at a time to
                # the client. We keep track of bytes_read because
                # send will return 0 if the client disconnects.
                # This prevents the server socket from sending bytes
                # to a connection that no longer exists.
                while bytes_read != b'':
                    
                    # Read 1000 bytes from the file.
                    data = fd.read(Server.NUM_BYTES)
                    
                    # If we have no more bytes to read, stop.
                    if data == '':
                        break
                        
                    # Send the bytes to the client.
                    bytes_read = server_socket.send(data.encode())
        except IOError as e:
            printf("Error: ", str(e))
            server_socket.close()
            return
        server_socket.close()
        print("Server: Done. File sent to client", client_addr)
        print()
        
    # Main loop that allows the server to wait
    # for requests. Once the server gets a request, it
    # creates a new thread and has that thread deal with the client.
    # Input: None
    # Output: None
    def run(self):
        print("Server: Now accepting requests on port:", self.port)
        print()
        try:
            # Keep server active forever.
            while True:
                
                # Wait for a client to connect()
                helper_server, client_addr = self.socket.accept()
                print("Server: Got request from client", client_addr)
                print()
                
                # Create new thread and pass in spawned socket that
                # will be used to send the file to the client.
                tid = threading.Thread(target=Server.send_file, 
                        args=(self.file_path, client_addr, helper_server,))
                
                # Start thread. NOTE: We do not join() because it is blocking
                # Essentially, we create threads and allow them to run
                # freely and never wait for a specific thread to finish.
                tid.start()
        except socket.error as e:
            print("Error: ", str(e))
            self.socket.close()
        except KeyboardInterrupt:
            self.socket.close()
    
    # Has server create a socket, bind to an address,
    # and indicate that it is willing to listen to client requests.
    # Input: None
    # Output: None
    def setup(self):
        # There should be three args: the program name, the 
        # port that the server will bind to, and the file name
        if len(sys.argv) != 3:
            print("Usage: python3 server.py <port> <file>")
            return
        
        # Return if the port num is not an int
        port = str_to_pos_int(sys.argv[1], "port")
        if (port < 0):
            return
        self.port = port
        
        # Get file path and check that it exists. We do not
        # hardcode "bio.txt" because I wanted to make it flexible
        self.file_path = sys.argv[2]
        if not os.path.exists(self.file_path):
            print("Error: file '%s' does not exist" % self.file_path)
            return
        
        # Create TCP server side socket.
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Error: unable to create socket")
            print(str(e))
            return
        
        # Bind server socket to address and get it ready to listen
        # to client requests.
        try:
            # Binding to "" means binding to 0.0.0.0 which
            # binds to all interface.
            self.socket.bind(("", self.port))
            self.socket.listen(Server.MAX_NUM_CLIENTS)
        except socket.error as e:
            print("Error: unable to setup socket on port ", self.port)
            print(str(e))
            self.socket.close()
            return

        self.run()

# Create a server instance, set it up, and run it.
if __name__ == "__main__":  
    server = Server()
    server.setup()