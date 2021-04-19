#!/usr/bin/env python3
import sys, os
import re
import socket
import logging
import argparse
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
    parser.add_argument('--dir', action='store', default='/home/' + os.getenv('USER') + '/measurements/' )
    args = parser.parse_args()

    setup_logger()
    logging.info('Starting sensor node.')
    
    hostname = socket.gethostname()

    SN = Sensor_Node(hostname, args.port, args.baud, args.int, args.dir)
    ############################################################
    # SN.mu.restart() TODO: restarting breaks the program, why?
    # After this script gets terminated, the MU has to be 
    # manually restartet!
    ############################################################
    while True:
        try:
            SN.start()
        except KeyboardInterrupt:
            logging.info("Interrupted!")
            SN.stop()

            next_command = input('\nEnter a command:\n\tnew --> start new measurement\n\texit --> exit from the script\n> ')
            if next_command != 'new':
                if next_command != 'exit':
                    print("Unknow command. Exiting.")
                SN.shutdown()
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)                    
            