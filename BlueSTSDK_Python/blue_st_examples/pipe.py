import zmq

import globals

def main():
    globals.SOCKET_OUT.bind("tcp://*:5555")
    msg = globals.SOCKET_OUT.recv_json()

    return msg