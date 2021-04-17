#!/usr/bin/env python3
from edge_device import Edge_Device
import sys, os

if __name__ == "__main__":
    ED = Edge_Device()
    try:
        ED.start()
    except KeyboardInterrupt:
        ED.stop()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)