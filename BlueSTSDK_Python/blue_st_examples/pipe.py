import zmq

import globals

def main():
    globals.SOCKET_OUT.bind("tcp://*:5555")
    msg = globals.SOCKET_OUT.recv_json()
    globals.SOCKET_OUT.send(str().encode("utf-8"))

    return msg