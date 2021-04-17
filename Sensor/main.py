#!/usr/bin/env python3
from sensor_node import Sensor_Node
import sys, os

if __name__ == "__main__":
    SN = Sensor_Node(0)
    ############################################################
    # SN.mu.restart() TODO: restarting breaks the program, why?
    # After this script gets terminated, the MU has to be 
    # manually restartet!
    ############################################################
    try:
        SN.start()
    except KeyboardInterrupt:
        SN.stop()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)