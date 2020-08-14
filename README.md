# Multi Window Sender (MWS)
This utility allow the user to send keyboard inputes to multi windows at the same time. The utility consist of two different applications. A server and a client.

Both the server and the client are access through the same program.

usage: mws [-h] [-v] [-p PORT] [-C CONFIG] [-I IGNORE [IGNORE ...]]
           [[-a ADD | -r RM | -c |] [-A | -D | -T |] -s | -k]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -p PORT, --port PORT  Server port
  -C CONFIG, --config CONFIG
                        Filepath to config file
  -I IGNORE [IGNORE ...], --ignore IGNORE [IGNORE ...]
                        Keycodes to ignore
Client options
  -a ADD, --add ADD     Add window
  -r RM, --rm RM        Remove window
  -c, --clear           Remove all window
  -A, --active          Activate the utility
  -D, --deactive        Deactivate the utility
  -T, --toggle          Toggle the status of the utility
  -k, --kill            Kill the server
Server option
  -s, --server          Launch the server as daemon


## Configuration file
This program uses a simple configuration file 
