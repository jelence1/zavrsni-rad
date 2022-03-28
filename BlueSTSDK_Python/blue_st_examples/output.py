import sys
import os
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    try:
        message = socket.recv()
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