import zmq

RECORDING_CODE = 50
EDIT_CODE = 100

CONTEXT_BLE = zmq.Context()

SOCKET_BLE = CONTEXT_BLE.socket(zmq.REQ)
#SOCKET_BLE.connect("tcp://localhost:5555")

CONTEXT_OUT = zmq.Context()
SOCKET_OUT = CONTEXT_OUT.socket(zmq.REP)
#SOCKET_OUT.bind("tcp://*:5555")

