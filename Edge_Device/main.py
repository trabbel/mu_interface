#!/usr/bin/env python3
from edge_device import Edge_Device

if __name__ == "__main__":
    ED = Edge_Device()
    try:
        while True:
            ED.start()
    except KeyboardInterrupt:
        ED.stop()