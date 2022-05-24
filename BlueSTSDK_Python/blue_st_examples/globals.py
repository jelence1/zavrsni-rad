import zmq

RECORDING_CODE = 50
EDIT_CODE = 100

CONTEXT = zmq.Context()

SOCKET_BLE = CONTEXT.socket(zmq.REQ)
#SOCKET_BLE.connect("tcp://localhost:5555")

CONTEXT2 = zmq.Context()
SOCKET_OUT = CONTEXT2.socket(zmq.REP)
#SOCKET_OUT.bind("tcp://*:5555")

