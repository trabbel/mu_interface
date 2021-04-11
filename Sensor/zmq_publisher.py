#!/usr/bin/env python3
import zmq

class ZMQ_Publisher():
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5556")

    def publish(self, data):
        self.socket.send_string(str(data))
