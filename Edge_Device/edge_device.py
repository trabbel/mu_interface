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
        last_time = datetime.datetime.now()
        
        while True:
            header, payload = self.sub.receive()
            sender = header['name']
            msg_type = header['msg_type']

            logging.debug("Incoming data from node %s", sender)

            # MU data header
            if msg_type == 0:
                payload = payload.split('\r\n')
                logging.info("Measurement started at %s", payload[2].split()[1])
                logging.info("Device ID: %s", payload[3].split()[1])
            # MU data
            elif msg_type == 1:
                self.save_data(sender, payload)
            # MU data/ID/measurement mode
            elif msg_type == 2:
                self.save_data(sender, payload[:-2])
                logging.info("Device ID: %s", payload[-2])
                logging.info("Measurement mode: %s", payload[-1])
            # Unknown
            else:
                logging.warning("Unknown message type: %d. Payload:\n%s", msg_type, payload)

            # Create new csv files at midnight.
            current_time = datetime.datetime.now()
            if current_time.hour in {0, 6, 12, 18} and current_time.hour != last_time.hour:
                logging.info("Creating new csv files.")
                for node in self.csv_objects:
                    self.csv_objects[node].close_file()
                    file_name = f"{node}_{current_time.strftime('%d_%m_%Y-%H_%M_%S')}.csv"
                    self.csv_objects[node] = data2csv(self.file_path  + node + '/', file_name)
                last_time = current_time


    def save_data(self, sender, payload):
        # Create a new csv file if it doesn't exist for this sender.
        if sender not in self.csv_objects:
            file_name = f"{sender}_{datetime.datetime.now().strftime('%d_%m_%Y-%H_%M_%S')}.csv"
            self.csv_objects[sender] = data2csv(self.file_path + sender + '/', file_name)
            logging.info("Created file: %s", file_name)

        # Read and format the data.
        data = payload.tolist()
        logging.debug(" \n%s", data)


        # Store the data to the csv file.
        e = self.csv_objects[sender].write2csv(data)
        if e is not None:
            logging.error("Writing to csv file failed with error:\n%s\n\n\
                Continuing because this is not a fatal error.", e)


    def stop(self):
        """
        Stop the subscriber and close all open csv files.
        """
        logging.info("Stopped listening at %s.", datetime.datetime.now().strftime("%d.%m.%Y. %H:%M:%S"))
        for node in self.csv_objects:
            self.csv_objects[node].close_file()
        self.csv_objects = {}

    def shutdown(self):
        """
        Perform final clean up on shutdown.
        """
        self.sub.socket.close()
        self.sub.context.term()