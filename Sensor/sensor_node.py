#!/usr/bin/env python3
from cybres_mu import Cybres_MU
from zmq_publisher import ZMQ_Publisher
import numpy as np
import logging
import time, re

class Sensor_Node():

    def __init__(self, hostname, port, baudrate, meas_interval):

        self.mu = Cybres_MU(port, baudrate)
        self.pub = ZMQ_Publisher()
        self.hostname = hostname
        self.measurment_interval = meas_interval

    def start(self):
        self.mu.start_measurement()
        time.sleep(0.2)

        # Record the starting time and notify the user.
        start_time = datetime.datetime.now()
        logging.info("Measurement started at %s.", start_time.strftime("%d.%m.%Y. %H:%M:%S"))

        # Send the MU header:
        header = "".join(self.mu.return_serial() for _ in range(8))
        self.pub.publish((self.hostname, 0), header)

        time.sleep(1) # This is neccesarry, otherwise the next input is just 'Z'

        # Measure at set interval.
        self.mu.set_measurement_interval(self.measurment_interval)

        while True:
            # Get the current measurements.
            data = self.mu.return_serial()
        
            stripped_data = re.sub("A|Z", "", data)
            if len(stripped_data) != 0:
                # Send the sanitized data over the MQTT.
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
        
        header = (self.hostname, messagetype)
        payload = np.array(sanitized)
        # convert list in np array for serialization
        return header, payload


    def stop(self):
        self.mu.stop_measurement()
        self.mu.restart()


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new mu and pub? 
        pass
