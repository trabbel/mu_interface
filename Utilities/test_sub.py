from Edge_Device.zmq_subscriber import ZMQ_Subscriber
import numpy as np

Sub = ZMQ_Subscriber()

while True:
    a, b =Sub.receive()
    print(a)
    print(b)
