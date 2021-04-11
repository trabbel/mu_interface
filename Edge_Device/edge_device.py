#!/usr/bin/env python3
from zmq_subscriber import ZMQ_Subscriber

class Edge_Device():

    def __init__(self):
        self.sub = ZMQ_Subscriber()


    def start(self):
        # TODO: Decide on a directory to save the data. On RPI or ITI-server?
        data = self.sub.receive()
        print(data)


    def stop(self):
        # TODO: Relevant if start() saves data in a file, then: close file 
        pass


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new sub? 
        pass


    def visualize(self):
        # TODO: Data diagrams, mathplotlib or gnuplot? Will the ED have a monitor?
        # If not, where should the data be shown?
        pass