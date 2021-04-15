#!/usr/bin/env python3
from cybres_mu import Cybres_MU
from zmq_publisher import ZMQ_Publisher
import numpy as np
import time

class Sensor_Node():

    def __init__(self):

        # TODO: find port, maybe in main and give as parameter
        self.mu = Cybres_MU('/dev/ttyACM0')
        self.pub = ZMQ_Publisher()


    def start(self):
        self.mu.start_measurement()
        time.sleep(0.2)
        print("sending")

        # send the header as string
        header = "".join(self.mu.return_serial() for _ in range(8))
        self.pub.publish_data(np.array([0]))
        self.pub.publish_header(header)
        try:
            time.sleep(1) # doesn't work without sleep
            while True:
                data = self.mu.return_serial()
                sanitized = self.sanitize_input(data)
                self.pub.publish_data(sanitized)
        except KeyboardInterrupt:
            pass

    
    # MU data is in String format and will be transformed in an np array
    def sanitize_input(self, mu_data):

        # Ignore first two chars and split at whitespace
        split_data = mu_data[2:].split(" ")

        # MU sends every 100 measurements id and measurement mode
        if split_data[0] == 'd':
            sanitized = [0, int(split_data[1])]
        elif split_data[0] == 'a':
            sanitized = [1, int(split_data[1])]
        else:
            # timestamp is in format 'YY.MM.DD.HH.mm.ss', gets transformated in array
            timestamp = [int(elem) for elem in split_data[0].split(":")]

            # measurement data starts after timestamp
            measurements = [int(elem) for elem in split_data[1:]]
            sanitized = timestamp + measurements

        # convert list in np array for serialization
        return np.array(sanitized)


    def stop(self):
        self.mu.stop_measurement()
        self.mu.restart()


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new mu and pub? 
        pass
