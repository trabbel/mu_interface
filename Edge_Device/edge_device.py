#!/usr/bin/env python3
import logging
from zmq_subscriber import ZMQ_Subscriber

class Edge_Device():

    def __init__(self):
        self.sub = ZMQ_Subscriber()

    def start(self):
        logging.info("Receiving.")
        
        while True:
            header, payload = self.sub.receive()
            logging.debug("Incoming data from node %d", header[0])

            # MU data header
            if header[1] == 0:
                payload = payload.split('\r\n')
                logging.info("Measurement started at %s", payload[4].split()[1])
                logging.info("Device ID: %s", payload[5].split()[1])
            # MU ID
            elif header[1] == 1:
                logging.info("Device ID: %s", payload[0])
            # MU measurement mode
            elif header[1] == 2:
                logging.info("Measurement mode: %s", payload[0])
            # MU data
            elif header[1] == 3:
                print(payload)
            else:
                logging.warning("Unknown message type: %d. Payload:\n%s", header[1], payload)


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