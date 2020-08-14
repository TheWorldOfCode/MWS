import socket
import daemon
import time
import Xlib
import threading
from Xlib import X, XK
from Xlib.display import Display
from Xlib.ext import record
from Xlib.protocol import event


class mwsd:

    def __init__(self, args):

        self.verbose = args.verbose
        self.ip      = "localhost"
        self.port    = args.port
        self.ignore  = args.ignore

        self.disp   = Display()
        self.screen = self.disp.screen()
        self.root   = self.screen.root

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_socket()

        self.ids     = []
        self.windows = []

        self.status  = False
        self.running = True

        self.lock = threading.Lock()

# Communication to daemon
    def setup_socket(self):
#        self.socket.setblocking(False)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)

        # Running the server in a other thread
        self.running = True
        self.thread = threading.Thread(target = self.server_listen)
        self.thread.daemon = True
        self.thread.start()

    def server_listen(self):
        while self.running is True:

            connection, client_address = self.socket.accept()

            try:
                msg = ""
                while True:
                    data = connection.recv(16)

                    if data:
                        msg += data.decode()
                    else:
                        break

                if msg != "":
                    msg_list = msg.split()

                    if self.verbose is True:
                        print(msg)

                    if msg_list[0] == "add":
                        for id in msg_list[1:]:
                            self.add(int(id))
                        connection.sendall("done".encode())
                    elif msg_list[0] == "rm":
                        for id in msg_list[1:]:
                            self.rm(int(id))
                        connection.sendall("done".encode())
                    elif msg_list[0] == "clear":
                        self.clear()
                    elif msg_list[0] == "active":
                        self.active()
                    elif msg_list[0] == "deactive":
                        self.deactive()
                    elif msg_list[0] == "toggle":
                        if self.status is True:
                            self.active()
                        else:
                            self.deactive()
                    elif msg_list[0] == "stop":
                        self.terminate()
                    else:
                        print("Unknown command")
                        connection.sendall("UnknownCommand".encode())

            finally:
                connection.close()


# Actions

    def add(self, id: int):
        self.lock.acquire(blocking=True)
        self.ids.append(id)
        self.windows.append(self.disp.create_resource_object('window', id))
        self.grab(self.windows[-1])
        self.lock.release()

    def rm(self, id: int):
        self.lock.acquire(blocking=True)

        index = self.ids.index(id)
        self.ids.remove(id)
        self.windows.remove(self.windows[index])

        self.lock.release()

    def clear(self):
        self.lock.acquire(blocking=True)

        self.windows.clear()
        self.ids.clear()

        self.lock.release()

    def active(self):
        self.status = True

    def deactive(self):
        self.status = False

    def terminate(self):
        self.running = False

# Daemon main function
    def listen(self):
        while self.running:
            # X11
            if len(self.windows) != 0 and len(self.ids) != 0:
                evt = self.disp.next_event()
                if evt.type in [X.KeyPress ]:
                    keycode = evt.detail
                    if self.verbose is True:
                        print("Keycode:", keycode)

                    self.disp.allow_events(X.ReplayKeyboard, X.CurrentTime)
                    if self.status is True:
                        for window in self.windows:
                            self.press(window, keycode, evt.state)
                    else:
                        index = self.ids.index(evt.window.id)
                        self.press(self.windows[index], keycode, evt.state)


                if evt.type == X.DestroyNotify:
                    try:
                        self.rm(evt.window.id)
                    except ValueError:
                        pass


# X11
    def event(self, name, window, detail, state):
        return name(time=X.CurrentTime,
                    root=self.root,
                    window=window,
                    same_screen=0,
                    child=Xlib.X.NONE,
                    root_x=0, root_y=0,
                    event_x=0, event_y=0,
                    state = state,
                    detail=detail
                   )

    def press(self, window, keycode, mask=X.NONE):
        window.send_event(self.event(event.KeyPress, window, keycode, mask), propagate=True)
        window.send_event(self.event(event.KeyRelease, window, keycode, mask), propagate=True)
        self.disp.flush()
        self.disp.sync()

    def grab(self, window):
        window.grab_key(X.AnyKey, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)

        # Ungrab window manager shortcuts (Super + ...)
        for key in self.ignore:
            window.ungrab_key(key, X.AnyModifier, True)

        window.change_attributes(event_mask=X.KeyReleaseMask | X.KeyPressMask | X.StructureNotifyMask)

    def ungrab(self, window):
        window.ungrab_key(X.AnyKey, X.AnyModifier, True)

# Cleanup

    def cleanup(self):
        self.running = False

def _start_2(args):
    server = mwsd(args)
    server.listen()

def start(args):
    if args.server is True:
        args.verbose = False

        with daemon.DaemonContext():
            _start_2(args)
    else:
        _start_2(args)

