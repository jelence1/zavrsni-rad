#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import sys
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    message = message.decode("utf-8")
    print(message)
    if "?" in message:
        socket.send(input().encode("utf-8"))
    else:
        socket.send(str().encode("utf-8"))