#!/usr/bin/env python3
import sys, os
import logging
from edge_device import Edge_Device

sys.path.append("..") # Adds higher directory to python modules path.
from Utilities.log_formatter import ColoredFormatter, setup_logger


if __name__ == "__main__":
    setup_logger()
    logging.info("Starting edge node.")


    ED = Edge_Device()
    try:
        ED.start()
    except KeyboardInterrupt:
        ED.stop()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)