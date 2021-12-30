# Nichole Maldonado
# This file creates N 
# client processes that
# connect to the server.

import os
import sys
from lib.utils import str_to_pos_int

# Executes client.py.
# Input: The args that will be passed to the client.
# Output: None.
def run_client_code(client_args):
    os.execvp("python3", client_args)
    print("Error: Unable to exec()")
    exit(1)

# Creates N clients.
# Input: The arguments that will be passed
#        to each client process and the number
#        of child processes to spawn.
# Output: None.
def create_clients(client_args, num_clients):
    
    # Create N clients.
    for i in range(num_clients):
        pid = os.fork()
        if pid < 0:
            print("Error: Unable to fork all children. Killing processes")
            sys.exit(1)
        
        # If child, run client.py
        elif pid == 0:
            run_client_code(client_args)
    # Once parent is done spawning N children,
    # have it wait for each one to complete.
    for i in range(num_clients):
        os.wait()

# Gets args passed in by user and starts prog.
# Input: None.
# Output: None.
def setup_mutli_clients():
    argc = len(sys.argv)
    if argc < 3 or argc > 4:
        print("Usage: python3 multi_clients.py <server_port> <num_clients> [<server_ip>]")
        return
    
    client_args = ["python3", "client.py"]
    
    # Gets port of server. Make sure it is a valid int.
    if str_to_pos_int(sys.argv[1], "port") < 0:
        return
    client_args.append(sys.argv[1])
    
    # Gets the number of client processes that will be
    # spawned.
    num_clients = str_to_pos_int(sys.argv[2], "num_clients")
    if num_clients < 0:
        return
    
    # Add ip of server if included
    if argc == 4:
        client_args.append(sys.argv[3])
    
    # Creates client processes and exec() them.
    create_clients(client_args, num_clients)
    
# Runs made code that creates N
# client.py processes.
if __name__ == "__main__":
    setup_mutli_clients()