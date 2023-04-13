# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Sample code and test for adafruit_ina219"""

import time, socket
from datetime import datetime
import board
import busio
import numpy as np
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
from zmq_publisher import ZMQ_Publisher


i2c_bus = busio.I2C(board.SCL1, board.SDA1)  # uses board.SCL and board.SDA

ina219_solar = INA219(i2c_bus, addr=0x40)
ina219_battery = INA219(i2c_bus, addr=0x45)


MEASUREMENT_INTERVAL = 2
ADDRESS = "localhost"
HOSTNAME = socket.gethostname()
header = (HOSTNAME, 3, False)
pub = ZMQ_Publisher(ADDRESS)


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
    bus_voltage_solar = ina219_solar.bus_voltage  # voltage on V- (load side)
    current_solar = ina219_solar.current /1000 # current in mA
    bus_voltage_battery = ina219_battery.bus_voltage  # voltage on V- (load side)
    current_battery = ina219_battery.current  /1000# current in mA

    payload = np.array([int(datetime.now().timestamp()), bus_voltage_solar, current_solar, bus_voltage_battery, current_battery])
    pub.publish(header, False, payload)

    # Check internal calculations haven't overflowed (doesn't detect ADC overflows)
    if ina219_solar.overflow:
        print("Internal Math Overflow Detected!")
        print("")

    time.sleep(MEASUREMENT_INTERVAL)