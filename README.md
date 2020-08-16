# Multi Window Sender (MWS)
This utility allow the user to send keyboard inputes to multi windows at the same time. The utility consist of two different applications with are access through the same program. A server and a client. The server when active intercepts keypress that are speficied by the client and send them to all the windows that the client have given the server. 

## Installing
In order to install the program run the command 
``` bash
make install
```
and to uninstall
``` bash
make uninstall
```

## Usages 
``` bash
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
``` 

### Server
In order to run the server don't add any of the client option. If the `-s` is not given will the server start attach to the terminal else will it start as a daemon. 

### Client 
When the server is running, you can add window in to different ways, `mws -a 0` this will add the current active window or by `mws -a window_id`. The same goes for the remove function. You can activate the server by using the `--active` option, by default is the server deactivated. You can then deactivate the server by using the option `--deactive` or toggle. 

The easies way to kill the server is using the `-k / --kill` option. 

## Configuration file
This program uses a simple configuration file which only contains two lines. 
``` bash
port xxxxxx
ignorekeycode [ key 1, key 2, ...]
```
In order to quick setup the configuration just run the program and it will ask if you want to create the configuration file. The default file path is `~/.config/mws/config` (config is the filename) but can be changed by the `-C / --config` option. The default configuration file will ignore any key comparation that contains the windows key. 

In order to optain the keycodes can the server be runned attach to the terminal without a configuration file and a specificed port. 
``` bash
mws -v -C /tmp/config -p 36540 
```
When just don't create the config file. 
