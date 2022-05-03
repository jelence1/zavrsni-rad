#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import sys
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for request in range(10):
    socket.send(input("Sending this.").encode("utf-8"))
    socket.recv()
    socket.send(input("Sending that.").encode("utf-8"))
    socket.recv()
    socket.send(("Send me something?").encode("utf-8"))
    try:
        message = socket.recv().decode("utf-8")

    except KeyboardInterrupt:
        socket.close()
        context.term()
        sys.exit(0)
    else:
        print("Received reply {} [ {} ]".format(request, message))