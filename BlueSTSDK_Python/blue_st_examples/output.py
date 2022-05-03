import sys
import os
import zmq

CONTEXT = zmq.Context()
SOCKET = CONTEXT.socket(zmq.REP)
SOCKET.bind("tcp://*:5555")

def main():
	try:
		while True:
			message = SOCKET.recv().decode("utf-8")
			if "?" in message:
			    print(message)
			    SOCKET.send(input().encode("utf-8"))
			elif "$" in message:
			    SOCKET.send(str().encode("utf-8"))
			    SOCKET.close()
			    CONTEXT.term()
			    sys.exit(0)
			else:
			    print(message)
			    SOCKET.send(str().encode("utf-8"))
	except KeyboardInterrupt:
		SOCKET.close()
		CONTEXT.term()
		sys.exit(0)

main()
