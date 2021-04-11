#!/usr/bin/env python3
import zmq

class ZMQ_Subscriber():

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5556")
        self.socket.subscribe("")


    def receive(self):
        data = self.socket.recv_string()
        return data