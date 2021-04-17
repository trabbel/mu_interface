#!/usr/bin/env python3
from zmq_subscriber import ZMQ_Subscriber

class Edge_Device():

    def __init__(self):
        self.sub = ZMQ_Subscriber()


    def start(self):
        print("receiving")
        
        while True:    
            header, payload = self.sub.receive()
            print(header)
            print(payload)


    def stop(self):
        # TODO: Relevant if start() saves data in a file, then: close file 
        pass


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new sub? 
        pass


    def visualize(self):
        # TODO: Data diagrams, matplotlib or gnuplot? Will the ED have a monitor?
        # If not, where should the data be shown?
        pass