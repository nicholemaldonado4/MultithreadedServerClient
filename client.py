# Nichole Maldonado
# This file provides an impl
# for a client that gets info from
# a server and writes it to a file.

import socket
import sys
import datetime
from lib.utils import str_to_pos_int

# The Client class gets information from a 
# server via its socket and writes this
# information to a file.
class Client:
    
    # File name format that the client will use
    # to createe a file.
    FILE_NAME = "client_files/received_bio_%d_%s.txt"
    
    # Constructor for the client.
    # Input: None
    # Output: None
    def __init__(self):
        # Default server ip address is localhost.
        # Can be changed by user through command line arg.
        self.server_ip = "localhost"
        
        # Port that server is bound to.
        self.server_port = None
        
        # TCP client side socket.
        self.socket = None

    # Builds file name based with client id and timestamp
    # appended.
    # Input: None
    # Output: file name for this specific client.
    def get_file_name(self):
        # Get timestamp
        time_str = datetime.datetime.now().strftime('%m%d%H%M%S%f')
        
        # Get client id (aka port number that client socket
        # is located on)
        client_port = self.socket.getsockname()[1]
        
        # Return file name.
        return self.FILE_NAME % (client_port, time_str)
    
    # Runs main client code that waits to 
    # get info from the server and writes it 
    # to a file.
    # Input: None.
    # Output: None.
    def run(self):
        try:
            # Client initiates handshake with server
            # to establish connection.
            self.socket.connect((self.server_ip, self.server_port))
            
            # Gets file name that it will write info to.
            file_name = self.get_file_name()
            print("Creating file", file_name)
            with open(file_name, "a") as new_file:
                
                # As soon as msg == b'', then the server
                # is done sending info, so stop trying to
                # recv(). 
                msg = b'1'
                while msg != b'':
                    
                    # Wait for info sent by server.
                    msg = self.socket.recv(1000)
                    
                    # Write info to the file.
                    new_file.write(msg.decode())
                    
            print("Done creating file", file_name)
        except (socket.error, IOError) as e:
            print("Error: ", str(e))
        finally:
            self.socket.close()

    # Sets up client so that it can connect to the server.
    def setup(self):
        num_args = len(sys.argv)
        if num_args < 2 or num_args > 3:
            print("Usage: python3 client.py <server_port> [<server_ip>]\n")
            print("Where <server_port> is the port that the server is runnning on")
            print("and <server_ip> is 'localhost' by default (if not included) or")
            print("if provided will be used as the ip address of the server.")
            return
        
        # Server port is the second argument.
        # Return if the port num is not an int
        port = str_to_pos_int(sys.argv[1], "port")
        if (port < 0):
            return
        self.server_port = port
        
        # Server's ip address is the third argument.
        if num_args == 3:
            self.server_ip = sys.argv[2]
        try:
            
            # Create client side TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Error: unable to create socket")
            print(str(e))
            return
        
        # If we reach this point, we are now ready connect() to
        # the server.
        self.run()
    
# Creates a client and calls for
# client to be setup and run.
if __name__ == "__main__":
    client = Client()
    client.setup()