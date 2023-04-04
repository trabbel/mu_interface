#!/usr/bin/env python3
import sys, os
import re
import socket
import logging
import argparse
import serial
import time
from sensor_node import Sensor_Node

sys.path.append("..") # Adds higher directory to python modules path.
from Utilities.log_formatter import ColoredFormatter, setup_logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for the sensor node.")
    parser.add_argument('--port', action='store', default='/dev/ttyACM0',
        help="Port where the measurement unit is connected.")
    parser.add_argument('--baud', action='store', type=int, default=460800,
        help="Baudrate for communicating with the measurement unit.")
    parser.add_argument('--int', action='store', type=int, default=10000,
        help="Time interval between two measurements (in miliseconds).")
    parser.add_argument('--addr', action='store', default='localhost',
        help='Address of the MQTT subscriber. Can be IP, localhost, *.local, etc.')
    parser.add_argument('--dir', action='store', default='/home/' + os.getenv('USER') + '/measurements/' )
  #  parser.add_argument('--multi', action='store', type=bool, default=False,
   #     help="If multiple MU sensors are connected to one device")
    args = parser.parse_args()

    multi = True

    if args.addr == 'localhost':
        hostname = args.port.split('/')[-1]
    elif multi:
        hostname = f"{socket.gethostname()}_" + args.port.split('/')[-1]
    else:
        hostname = socket.gethostname()

    setup_logger(hostname)
    logging.info('Starting sensor node.')

    csv_dir = args.dir
    if csv_dir[-1] != '/':
        csv_dir += '/'

    connected = False
    while True:
        while not connected:
            try:
                SN = Sensor_Node(hostname, args.port, args.baud, args.int, args.addr, csv_dir)
                connected = True
                logging.info("Connected!")
            except serial.serialutil.SerialException:
                print("Waiting for connection...")
                time.sleep(5)

        try:
            SN.start()
        except KeyboardInterrupt:
            logging.warning("Interrupted! Wait for the program to exit.")
            connected = False
            SN.stop()
            time.sleep(1)
            SN.shutdown()
            time.sleep(5.0)
            sys.exit(0)
        except (serial.serialutil.PortNotOpenError, serial.serialutil.SerialException):
            logging.error("Port forcefully closed!")
            connected = False
            SN.close()