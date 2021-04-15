#!/usr/bin/env python3
import zmq
import numpy as np

class ZMQ_Subscriber():

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5556")
        self.socket.subscribe("")


    def receive(self):
        data = self.recv_array()
        # check if header
        if len(data) == 1:
            data = self.socket.recv_string()
        return data


    # function for receiving and deserializing np arrays
    def recv_array(self, flags=0, copy=True, track=False):
        md = self.socket.recv_json(flags=flags)
        message = self.socket.recv(flags=flags, copy=copy, track=track)
        buffer = memoryview(message)
        array = np.frombuffer(buffer, dtype=md['dtype'])
        return array.reshape(md['shape'])