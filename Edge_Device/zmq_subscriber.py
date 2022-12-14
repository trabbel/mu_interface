#!/usr/bin/env python3
import zmq
import numpy as np

class ZMQ_Subscriber():

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind("tcp://*:5556")
        self.socket.subscribe("")


    # receive a custom multipart message
    # refer to readme for more information
    def receive(self, flags=0, copy=True, track=False):
        header = self.socket.recv_json(flags=flags)
        additionalSensors = False
        if header['msg_type'] == 0:
            payload = self.socket.recv_string(flags=flags)
        else:
            if header['add_sensor']:
                additionalSensors = self.socket.recv_json(flags=flags)
            payload = self.recv_array(flags=flags)
        return header, additionalSensors, payload


    # function for receiving and deserializing np arrays
    def recv_array(self, flags=0, copy=True, track=False):
        md = self.socket.recv_json(flags=flags)
        message = self.socket.recv(flags=flags, copy=copy, track=track)
        buffer = memoryview(message)
        array = np.frombuffer(buffer, dtype=md['dtype'])
        return array.reshape(md['shape'])
