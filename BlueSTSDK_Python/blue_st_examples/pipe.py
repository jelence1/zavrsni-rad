import zmq

import globals

def main():
    print("i am here")
    globals.SOCKET_OUT.bind("tcp://*:5555")
    msg = globals.SOCKET_OUT.recv_json()
    globals.SOCKET_OUT.send_json(msg)
