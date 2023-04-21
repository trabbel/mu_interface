import os
import argparse
import time
import socket
from datetime import datetime

import board
import busio
import numpy as np
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

from zmq_publisher import ZMQ_Publisher


i2c_bus = busio.I2C(board.SCL1, board.SDA1)  # uses board.SCL and board.SDA

ina219_solar = INA219(i2c_bus, addr=0x40)
ina219_battery = INA219(i2c_bus, addr=0x41)

parser = argparse.ArgumentParser(description="Arguments for the sensor node.")
parser.add_argument('--int', action='store', type=int, default=5,
    help="Time interval between two measurements (in seconds).")
parser.add_argument('--addr', action='store', default='localhost',
    help="Address of the MQTT subscriber. Can be IP, localhost, *.local, etc.")
parser.add_argument('--dir', action='store', default='/home/' + os.getenv('USER') + '/measurements/',
    help="Directory where measurement data is saved.")
args = parser.parse_args()


header = (socket.gethostname(), 3, False)
pub = ZMQ_Publisher(args.addr)


# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219_solar.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219_solar.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219_solar.bus_voltage_range = BusVoltageRange.RANGE_16V
# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219_battery.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219_battery.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219_battery.bus_voltage_range = BusVoltageRange.RANGE_16V

# measure and display loop
while True:
    bus_voltage_solar = ina219_solar.bus_voltage        # voltage on V- (load side)
    current_solar = ina219_solar.current                # current in mA
    bus_voltage_battery = ina219_battery.bus_voltage    # voltage on V- (load side)
    current_battery = ina219_battery.current            # current in mA

    payload = np.array([int(datetime.now().timestamp()), bus_voltage_solar, current_solar, bus_voltage_battery, current_battery])
    pub.publish(header, False, payload)
    
    # TODO: add some statistics to print out

    # Check internal calculations haven't overflowed (doesn't detect ADC overflows)
    if ina219_solar.overflow:
        print("Internal Math Overflow Detected!")
        print("")

    time.sleep(args.int)