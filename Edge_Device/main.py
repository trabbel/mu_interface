#!/usr/bin/env python3
import os
import sys
import logging
import argparse

from edge_device import Edge_Device

sys.path.append("..") # Adds higher directory to python modules path.
from Utilities.log_formatter import ColoredFormatter, setup_logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for the sensor node.")
    parser.add_argument('--dir', action='store', default='/home/' + os.getenv('USER') + '/measurements/' )
    args = parser.parse_args()

    setup_logger()
    logging.info("Starting edge node.")

    csv_dir = args.dir
    if csv_dir[-1] != '/':
        csv_dir += '/'

    ED = Edge_Device(csv_dir)
    while True:
        try:
            ED.start()
        except KeyboardInterrupt:
            ED.stop()
            
            next_command = input('\nEnter a command:\n\tnew --> start new measurement\n\texit --> exit from the script\n> ')
            if next_command != 'new':
                if next_command != 'exit':
                    print("Unknow command. Exiting.")
                ED.shutdown()
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)    