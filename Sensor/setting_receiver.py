import zmq
from subprocess import Popen

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:5557")
socket.subscribe("")

while True:
    command = socket.recv_string(flags=0)
    if command == "hello":
        print(f"received: {command}")
        p = Popen("sudo shutdown -h now", shell=True)
        #p.wait()