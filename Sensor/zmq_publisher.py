#!/usr/bin/env python3
import zmq
import numpy as np

class ZMQ_Publisher():

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect("tcp://localhost:5556")


    # function for sending a custom multipart message
    def publish(self, header, payload, flags=0):
        self.send_array(header, flags|zmq.SNDMORE)
        if header[1] == 0:
            return self.socket.send_string(payload, flags)
        else:
            return self.send_array(payload, flags)


    # function for serializing and sending np arrays
    def send_array(self, array, flags=0, copy=True, track=False):
        md = dict(
            dtype = str(array.dtype),
            shape = array.shape,
        )
        self.socket.send_json(md, flags|zmq.SNDMORE)
        return self.socket.send(array, flags, copy=copy, track=track)
