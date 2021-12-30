Assignment 4d
=================

To run, first start the server by typing:

"python3 server.py <port> <file>"

where <port> is the port that you want the server to run on and <file> is the file path that you want you want the server to send to connecting clients.

For example:
"python3 server.py 5005 test_files/bio.txt"

** I included bio.txt in the folder test_files, so if you just enter the name, like in the example above, it will work.

To run the client, enter:

"python3 client.py <port> [<server_ip>]"

** NOTE: All client files will be stored to client_files

where <port> is the port that the server is bound to. The <server_ip> by default is "localhost", but you can include a different server_ip since the server binds to all interfaces. (0.0.0.0)

If you would like to run multiple clients simultaneously, run:

"python3 multi_clients.py <port> <num_clients> [<server_ip>]"

Which will create <num_clients> child processes that run "python3 client.py <port> [<server_ip>]". <server_ip> is optional.