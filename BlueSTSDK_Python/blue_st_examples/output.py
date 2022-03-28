import sys
import os
import zmq

CONTEXT = zmq.Context()
SOCKET = CONTEXT.socket(zmq.REP)
SOCKET.bind("tcp://*:5555")

while True:
    try:
        message = SOCKET.recv().decode("utf-8")
        print(message)
        if "?" in message:
            SOCKET.send(input().encode("utf-8"))
        elif "$" in message:
            SOCKET.send(str().encode("utf-8"))
            SOCKET.close()
            CONTEXT.term()
            sys.exit(0)
        else:
            SOCKET.send(str().encode("utf-8"))

    except KeyboardInterrupt:
        SOCKET.close()
        CONTEXT.term()
        sys.exit(0)