#!/usr/bin/env python3
from sensor_node import Sensor_Node

if __name__ == "__main__":
    SN = Sensor_Node()
    # SN.mu.restart() TODO: restarting breaks the program, why?
    try:
        while True:
            SN.start()
    except KeyboardInterrupt:
        SN.stop()
    # TODO: Fix the keyboard interrupt, it's buggy