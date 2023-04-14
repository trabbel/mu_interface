import zmq
from subprocess import Popen

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://*:5557")
socket.subscribe("")

while True:
    command = socket.recv_string(flags=0)
    print(f"received: {command}")
    if command == "shutdown":
        p = Popen("sudo shutdown -h now", shell=True)
    elif command == "reboot":
        p = Popen("sudo shutdown -r now", shell=True)