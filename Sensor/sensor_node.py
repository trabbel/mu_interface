#!/usr/bin/env python3
from cybres_mu import Cybres_MU
from zmq_publisher import ZMQ_Publisher

class Sensor_Node():

    def __init__(self):

        # TODO: find port, maybe in main and give as parameter
        self.mu = Cybres_MU('/dev/ttyACM0')
        self.pub = ZMQ_Publisher()


    def start(self):
        self.mu.start_measurement()
        #print("sending")
        try:
            while True:
                self.pub.publish(self.mu.return_serial)
        except KeyboardInterrupt:
            pass


    def stop(self):
        self.mu.stop_measurement()
        self.mu.restart()


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new mu and pub? 
        pass
