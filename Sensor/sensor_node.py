#!/usr/bin/env python3
from cybres_mu import Cybres_MU
from zmq_publisher import ZMQ_Publisher
import numpy as np
import time, re

class Sensor_Node():

    def __init__(self, sensor_number, port, baudrate, meas_interval):

        self.mu = Cybres_MU(port, baudrate)
        self.pub = ZMQ_Publisher()
        self.number = sensor_number # This is the sensor number/hostname
        self.measurment_interval = meas_interval


    def start(self):
        self.mu.start_measurement()
        time.sleep(0.2)
        print("sending")

        # Send the MU header:
        header = "".join(self.mu.return_serial() for _ in range(8))
        self.pub.publish(np.array([self.number, 0]), header)

        time.sleep(1) # This is neccesarry, otherwise the next input is just 'Z'

        # measure every 10 seconds
        self.mu.set_measurement_interval(self.measurment_interval)

        while True:
            data = self.mu.return_serial()
            stripped_data = re.sub("A|Z", "", data)
            if len(stripped_data) != 0:
                header, payload = self.sanitize_input(stripped_data)
                self.pub.publish(header, payload)

    
    # MU data is in String format and will be transformed in an np array
    def sanitize_input(self, mu_data):
        # Split the string at whitespace
        split_data = mu_data.split(" ")

        # MU sends every 100 measurements id and measurement mode
        if split_data[0] == '#id':
            sanitized = [int(split_data[1])]
            # message is device ID
            messagetype = 1
        elif split_data[0] == '#ta':
            # message is measurement mode
            messagetype = 2
            sanitized = [int(split_data[1])]
        else:
            # message is data
            messagetype = 3
            # timestamp is in format 'YY.MM.DD.HH.mm.ss', gets transformated in array
            timestamp = [int(elem) for elem in split_data[0].split(":")]

            # measurement data starts after timestamp
            measurements = [int(elem) for elem in split_data[1:]]
            sanitized = timestamp + measurements
            # sanitized = measurements
        
        header = np.array([self.number, messagetype])
        payload = np.array(sanitized)
        # convert list in np array for serialization
        return header, payload


    def stop(self):
        self.mu.stop_measurement()
        self.mu.restart()


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new mu and pub? 
        pass
