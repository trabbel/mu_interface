#!/usr/bin/env python3
import zmq
import numpy as np

class ZMQ_Publisher():

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5556")


    def publish_data(self, data):
        self.send_array(data)


    def publish_header(self, header):
        self.socket.send_string(header)


    # function for serializing and sending np arrays
    def send_array(self, array, flags=0, copy=True, track=False):
        md = dict(
            dtype = str(array.dtype),
            shape = array.shape,
        )
        self.socket.send_json(md, flags|zmq.SNDMORE)
        return self.socket.send(array, flags, copy=copy, track=track)
