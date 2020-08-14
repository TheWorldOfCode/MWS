from . import mwsd
from . import mwsc
from . import arg

import socket


def cli():

    args = arg.arguments()

    config = arg.load_configuration(args)
    arg.setting_config(args, config)

    if arg.client_server_check(args) is True:
        mwsc.generate_message(args)
    else:
        mwsd.start(args)

