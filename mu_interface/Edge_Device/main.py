#!/usr/bin/env python3
import os
import sys
import logging
import argparse
from pathlib import Path

from edge_device import Edge_Device
from mu_interface.Utilities.log_formatter import setup_logger

def main(csv_dir):
    setup_logger("rock")
    logging.info("Starting edge node.")

    csv_dir = Path(csv_dir)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for the sensor node.")
    parser.add_argument('--dir', action='store', default=Path.home() / 'measurements')
    args = parser.parse_args()

    main(args.dir)
    