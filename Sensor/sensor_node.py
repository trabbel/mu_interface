#!/usr/bin/env python3
import sys
import re
import time
import logging
import datetime
import numpy as np

from cybres_mu import Cybres_MU
from zmq_publisher import ZMQ_Publisher

sys.path.append("..") # Adds higher directory to python modules path.
from Utilities.data2csv import data2csv

class Sensor_Node():

    def __init__(self, hostname, port, baudrate, meas_interval, address, file_path):

        self.mu = Cybres_MU(port, baudrate)
        self.pub = ZMQ_Publisher(address)
        self.hostname = hostname
        self.measurment_interval = meas_interval
        self.file_path = file_path
        self.csv_object = None

    def start(self):
        """
        Start the measurements. Continue to publish over MQTT and store to csv.
        """
        self.mu.start_measurement()
        time.sleep(0.2)

        # Record the starting time and notify the user.
        start_time = datetime.datetime.now()
        logging.info("Measurement started at %s.", start_time.strftime("%d.%m.%Y. %H:%M:%S"))
        logging.info("Saving data to: %s", self.file_path)

        # Send the MU header:
        header = "".join(self.mu.return_serial() for _ in range(9))
        self.pub.publish((self.hostname, 0), header)

        time.sleep(1) # This is neccesarry, otherwise the next input is just 'Z'

        # Measure at set interval.
        self.mu.set_measurement_interval(self.measurment_interval)

        # Create the file for storing measurement data.
        file_name = f"{self.hostname}_{start_time.strftime('%d_%m_%Y-%H_%M_%S')}.csv"
        self.csv_object = data2csv(self.file_path, file_name)
        last_time = start_time

        while True:
            # Create a new csv file after the specified interval.
            current_time = datetime.datetime.now()
            if current_time.hour in {0, 6, 12, 18} and current_time.hour != last_time.hour:
                logging.info("Creating a new csv file.")
                self.csv_object.close_file()
                file_name = f"{self.hostname}_{current_time.strftime('%d_%m_%Y-%H_%M_%S')}.csv"
                self.csv_object = data2csv(self.file_path, file_name)
                last_time = current_time

            # Get the current measurements.
            data = self.mu.return_serial()
        
            # delete "Z" and "A" from data strings
            stripped_data = re.sub("A|Z", "", data)
            if len(stripped_data) != 0:
                # Send the sanitized data over the MQTT.
                header, payload = self.sanitize_input(stripped_data)
                self.pub.publish(header, payload)

                # Store the data to the csv file.
                e = self.csv_object.write2csv(stripped_data)
                if e is not None:
                    logging.error("Writing to csv file failed with error:\n%s\n\n\
                        Continuing because this is not a fatal error.", e)
    
    # MU data is in String format and will be transformed in an np array
    def sanitize_input(self, mu_data):
        """
        Transform MU data from string to numpy array.

        Args:
            mu_data (str): MU data in string format.

        Returns:
            A tuble containing a header and payload for the MQTT message.
        """
        # Split the string at whitespace
        split_data = mu_data.split(" ")

        # MU sends every 100 measurements id and measurement mode --> THIS PART BREAKS WHEN RESTARTING MEASUREMENTS, BUT THE PLAN IS TO REMOVE IT ANYWAY
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
            # There is probably a better way to transform the timestamp.
            timestamp = [int(x) for x in (datetime.datetime.now().strftime('%y:%m:%d:%H:%M:%S').split(':'))]

            # measurement data starts after timestamp
            measurements = [int(elem) for elem in split_data[1:]]
            # sanitized = timestamp + measurements
            sanitized = [0] + measurements
        
        header = (self.hostname, messagetype)
        payload = np.array(sanitized)
        # convert list in np array for serialization
        return header, payload


    def stop(self):
        """
        Stop the measurement and clean up.
        """
        logging.info("Measurement stopped at %s.", datetime.datetime.now().strftime("%d.%m.%Y. %H:%M:%S"))
        _ = self.mu.return_serial()
        self.mu.stop_measurement()
        if self.csv_object is not None:
            self.csv_object.close_file()

    def shutdown(self):
        """
        Perform final clean up on shutdown.
        """
        self.pub.socket.close()
        self.pub.context.term()


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new mu and pub? 
        pass
