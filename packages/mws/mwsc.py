import socket
import sys
from Xlib.display import Display
from Xlib import X


def send(s: socket.socket, msg: str):
    s.sendall(msg.encode())

def generate_message(args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', args.port))
    flag = False
    disp = Display()
    root = disp.screen().root
    NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')

    if args.add == 0:
        response = root.get_full_property(NET_ACTIVE_WINDOW, X.AnyPropertyType)

        if not response:
            print("Couldn't find the active window", file=sys.stderr)

        send(s, "add " + str(response.value[0]))
    elif args.add is None:
        pass
    else:
        send(s, "add " + str(args.add))
        flag = True

    if args.rm == 0:
        response = root.get_full_property(NET_ACTIVE_WINDOW, X.AnyPropertyType)

        if not response:
            print("Couldn't find the active window", file=sys.stderr)

        send(s, "rm " + str(response.value[0]))
    if args.rm is None:
        pass
    else:
        send(s, "rm " + str(args.rm))
        flag = True

    if args.clear is True:
        send(s, "clear")
        flag = True

    if args.active is True:
        send(s, "active")
        flag = True

    if args.deactive is True:
        send(s, "deactive")
        flag = True

    if args.toggle is True:
        send(s, "toggle")
        flag = True

    if args.kill is True:
        send(s, "stop")
        flag = True

    return flag
