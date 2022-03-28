import sys
import os
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    try:
        message = socket.recv()
        print(message)
        if "?" in message:
            message.send_string(input())
        elif "$" in message:
            socket.close()
            context.term()
            sys.exit(0)
    except KeyboardInterrupt:
        socket.close()
        context.term()
        sys.exit(0)