#!/usr/bin/env python3
import sys
import logging
import datetime
import numpy as np
from collections import Counter

from zmq_subscriber import ZMQ_Subscriber

sys.path.append("..") # Adds higher directory to python modules path.
from Utilities.data2csv import data2csv

class Edge_Device():

    def __init__(self, file_path):
        self.sub = ZMQ_Subscriber()
        self.file_path = file_path
        self.csv_objects = {}
        self.msg_counter = Counter()
        self.start_time = None

    def start(self):
        """
        Start listening to MQTT messages and store data to csv files.
        """
        self.start_time = datetime.datetime.now()
        logging.info("Started listening at %s.", self.start_time.strftime("%d.%m.%Y. %H:%M:%S"))
        logging.info("Saving data to: %s", self.file_path)
        last_csv_time = datetime.datetime.now()
        last_info_time = datetime.datetime.now()
        
        while True:
            header, payload = self.sub.receive()
            sender = header['name']
            msg_type = header['msg_type']

            logging.debug("Incoming data from node %s", sender)

            # MU data header
            if msg_type == 0:
                payload = payload.split('\r\n')
                logging.info("Measurement started on node %s at %s", sender, payload[2].split()[1])
                logging.info("Measurement unit ID: %s", payload[3].split()[1])
            # MU data
            elif msg_type == 1:
                self.save_data(sender, payload)
                self.msg_counter[sender] += 1
            # MU data/ID/measurement mode
            elif msg_type == 2:
                self.save_data(sender, payload[:-2])
                logging.info("Node %s reporting: MU ID is %s, current measurement mode is: %s",
                             sender, payload[-2], payload[-1])
            # Unknown
            else:
                logging.warning("Unknown message type: %d. Payload:\n%s", msg_type, payload)

            current_time = datetime.datetime.now()

            # Print out a status message every 30 mins
            elapsed = current_time - last_info_time
            if elapsed.seconds > 1800:
                td = current_time - self.start_time
                duration = f"{td.seconds // 3600 :02}:{td.seconds // 60 % 60 :02}:{td.seconds % 60 :02} [HH:MM:SS]"
                logging.info("I am measuring for %s and I collected the following number of datapoints:\n%s", 
                             duration, "\n".join([f"{key}: {val}" for key, val in self.msg_counter.items()]))
                last_info_time = current_time


            # Create new csv files at midnight.
            if current_time.hour in {0, 6, 12, 18} and current_time.hour != last_csv_time.hour:
                logging.info("Creating new csv files.")
                for node in self.csv_objects:
                    self.csv_objects[node].close_file()
                    file_name = f"{node}_{current_time.strftime('%d_%m_%Y-%H_%M_%S')}.csv"
                    self.csv_objects[node] = data2csv(self.file_path  + node + '/', file_name)
                last_csv_time = current_time


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