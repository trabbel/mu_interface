# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Sample code and test for adafruit_ina219"""

import time
import board
import busio
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

i2c_bus = busio.I2C(board.SCL1, board.SDA1)  # uses board.SCL and board.SDA

ina219_solar = INA219(i2c_bus, addr=0x40)
ina219_battery = INA219(i2c_bus, addr=0x45)


MEASUREMENT_INTERVAL = 2


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
    current_solar = ina219_solar.current  # current in mA
    bus_voltage_battery = ina219_battery.bus_voltage  # voltage on V- (load side)
    current_battery = ina219_battery.current  # current in mA

    print("Voltage (VIN-) : {:6.3f}   V, {:6.3f}   V".format(bus_voltage_solar, bus_voltage_battery))
    print("Shunt Current  : {:7.4f}  A, {:7.4f}  A".format(current_solar / 1000, current_battery / 1000))
    print("")

    # Check internal calculations haven't overflowed (doesn't detect ADC overflows)
    if ina219_solar.overflow:
        print("Internal Math Overflow Detected!")
        print("")

    time.sleep(MEASUREMENT_INTERVAL)