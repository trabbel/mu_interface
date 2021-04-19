#!/usr/bin/env python3
import sys
import logging
import datetime
import numpy as np

from zmq_subscriber import ZMQ_Subscriber

sys.path.append("..") # Adds higher directory to python modules path.
from Utilities.data2csv import data2csv

class Edge_Device():

    def __init__(self, file_path):
        self.sub = ZMQ_Subscriber()
        self.file_path = file_path
        self.csv_objects = {}

    def start(self):
        """
        Start listening to MQTT messages and store data to csv files.
        """
        logging.info("Started listening at %s.", datetime.datetime.now().strftime("%d.%m.%Y. %H:%M:%S"))
        logging.info("Saving data to: %s", self.file_path)
        
        while True:
            header, payload = self.sub.receive()
            sender = header['name']
            msg_type = header['msg_type']

            logging.debug("Incoming data from node %s", sender)

            # MU data header
            if msg_type == 0:
                payload = payload.split('\r\n')
                logging.info("Measurement started at %s", payload[4].split()[1])
                logging.info("Device ID: %s", payload[5].split()[1])
            # MU ID
            elif msg_type == 1:
                logging.info("Device ID: %s", payload[0])
            # MU measurement mode
            elif msg_type == 2:
                logging.info("Measurement mode: %s", payload[0])
            # MU data
            elif msg_type == 3:
                logging.debug(" \n%s", payload)

                # Create a new csv file if it doesn't exist for this sender.
                if sender not in self.csv_objects:
                    file_name = f"{sender}_{datetime.datetime.now().strftime('%d_%m_%Y-%H_%M_%S')}.csv"
                    self.csv_objects[sender] = data2csv(self.file_path + sender + '/', file_name)
                    logging.info("Created file: %s", file_name)

                # Read and format the data.
                data = np.array2string(payload, suppress_small=True).strip('[]')

                # Store the data to the csv file.
                e = self.csv_objects[sender].write2csv(data)
                if e is not None:
                    logging.error("Writing to csv file failed with error:\n%s\n\n\
                        Continuing because this is not a fatal error.", e)
            # Unknown
            else:
                logging.warning("Unknown message type: %d. Payload:\n%s", msg_type, payload)

            # Create new csv files at midnight.
            current_time = datetime.datetime.now()
            if current_time.second == 0 and not saved:
                logging.info("Creating new csv files.")
                for node in self.csv_objects:
                    self.csv_objects[node].close_file()
                    file_name = f"{node}_{current_time.strftime('%d_%m_%Y-%H_%M_%S')}.csv"
                    self.csv_objects[node] = data2csv(self.file_path  + node + '/', file_name)
                saved = True
            elif current_time.second != 0:
                saved = False


    def stop(self):
        """
        Stop the subscriber and close all open csv files.
        """
        for node in self.csv_objects:
            self.csv_objects[node].close_file()


    def restart(self):
        # TODO: Decide on restart routine: Only stop/start or new sub? 
        pass


    def visualize(self):
        # TODO: Data diagrams, matplotlib or gnuplot? Will the ED have a monitor?
        # If not, where should the data be shown?
        pass