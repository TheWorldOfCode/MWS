import argparse
import configparser

from os.path import isfile, expanduser, dirname, exists
from os import mkdir

def arguments():
    """ Handling the allowed arguments """
    parser = argparse.ArgumentParser(description="Multi window sender")

    # General
    parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
    #parser.add_argument("-i", "--ip", help="Server ip address",  type=str, action="store", default="localhost")
    parser.add_argument("-p", "--port", help="Server port",  type=int, action="store")
    parser.add_argument("-C", "--config", help="Filepath to config file",  type=str, action="store", default="~/.config/msw/config")
    parser.add_argument("-I", "--ignore", help="Keycodes to ignore", type=list, nargs='+')

    client_server = parser.add_mutually_exclusive_group()
    # Client

    add_group = client_server.add_mutually_exclusive_group()
    add_group.add_argument("-a", "--add", help="Add window", type=int, action="store")
    add_group.add_argument("-r", "--rm", help="Remove window", type=int, action="store")
    add_group.add_argument("-c", "--clear", help="Remove all window", action="store_true")

    active_group = client_server.add_mutually_exclusive_group()
    active_group.add_argument("-A", "--active", help="Activate the utility", action="store_true")
    active_group.add_argument("-D", "--deactive", help="Deactivate the utility", action="store_true")
    active_group.add_argument("-T", "--toggle", help="Toggle the status of the utility", action="store_true")

    # Server
    #server_group = client_server.add_argument_group()
    #server_group.add_mutually_exclusive_group()
    client_server.add_argument("-s", "--server", help="Launch the server as daemon", action="store_true")
    client_server.add_argument("-k", "--kill", help="Kill the server", action="store_true")

    args = parser.parse_args()

    # The Ignore is a list of number in string format and therefore they must be convert to integer
    if  args.ignore is not None:
        new_list = []
        for l in args.ignore:
            new_list.append((int("".join(l))))

        args.ignore = new_list

    return args

def client_server_check(args):
   """ Check if running in server or in client mode
   :args: arguments given by user
   :returns: True if in client mode
   """

   if args.server is True:
       return False

   if args.active is False:
       if args.add is None:
           if args.clear is False:
               if args.deactive is False:
                   if args.rm is None:
                       if args.toggle is False:
                           if args.kill is False:
                               return False

   return True

def load_configuration(args):
    """ load configuration for the program
    :args: arguements given by the user
    :returns: Modificerd argument list
    """

    PATH = expanduser(args.config)

    config = configparser.ConfigParser(delimiters = [' ', ','])

    if isfile(PATH) is False:
        i = input("Config file doesn't exists. Will you create it ? [Y/n]: ")

        if i in ["yes", "Y", "y", "Yes", ""]:
            print("Creating")
            path = dirname(PATH)

            if exists(path) is False:
                mkdir(path)

            setup_config(PATH, config)
        else:
            print("Continuing without configuration file")
            if args.port is None:
                print("Cannot continue without a port number")
                raise Exception()
    else:
        config.read(PATH)


    return config


def setting_config(args, config):
    """ Coping config to arguments

    :args: User given arguments
    :config:  ConfigParser with configfile readed
    :returns:  modificed arguments

    """
    for option in config['DEFAULT']:

        if option == "port" and args.port is None:
            args.port = config.getint('DEFAULT', option)

        if option == "ignorekeycode":
            code = config.get('DEFAULT', option)
            code = code.replace(']', '')
            code = code.replace('[', '')
            code = code.split(',')

            if args.ignore is None:
                args.ignore = []

            for key in code:
                args.ignore.append(int(key))

            args.ignore = list(set(args.ignore))



def setup_config(path, config):
    """ Create default configuration file

    :path: The path where to create the configuration file
    :config: The configuration parser

    """
    config['DEFAULT'] = {'port': 36540, 'ignorekeycode': [133]}

    with open(path, 'w') as configfile:
        config.write(configfile)

