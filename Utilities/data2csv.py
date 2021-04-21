#!/usr/bin/env python3
import csv
from datetime import datetime
from pathlib import Path
from operator import methodcaller


class data2csv:

    def __init__(self, file_path, file_name):

        Path(file_path).mkdir(parents=True, exist_ok=True) # make new directory
        
        self.csvfile = open(file_path + file_name, 'w')
        self.csvwriter = csv.writer(self.csvfile)

        fields = ['date',
                   'time',
                   'sweep_freq',
                   # channel 1
                   'VImax_CH1',
                   'VImin_CH1',
                   'RMS_CH1',
                   'Phas_CH1',
                   'VVmax_CH1',
                   'VVmin_CH1',
                   'Corr_CH1',
                   # channel 2
                   'VImax_CHL2',
                   'VImin_CH2',
                   'RMS_CH2',
                   'Phas_CH2',
                   'VVmax_CH2',
                   'VVmin_CH2',
                   'Corr_CH2',
                   # system data
                   'temp-PCB',
                   'temp-thermostat',
                   # magnetometer and accelerometer data
                   'mag_X', 'mag_Y', 'mag_Z',
                   'acc_X', 'acc_Y', 'acc_Z',
                   # external sensors
                   'temp-external',
                   'light-external',
                   'humidity-external',
                   'differential_potential_CH1',
                   'differential_potential_CH2',
                   'RF_power_emission',
                   'transpiration',
                   'sap_flow',
                   'air_pressure',
                   'soil_moisture',
                   'soil_temperature',
                   'ambient_light',
                   'empty1',
                   'empty2',
                   'empty3',
                   'empty4',
                   'empty5',
                   'empty6',
                   'empty7',
                   'reserved1',
                   'reserved2']

        self.csvwriter.writerow(fields)

    def close_file(self):
        self.csvfile.close()

    def write2csv(self, data):
        try:
            d = data.split()
            d_data = list(map(int, d[1:]))
            # MU has different timezone
            time = datetime.now().strftime('%H:%M:%S')
            date = datetime.now().strftime('%d/%m/%Y')
            data4csv = [date, time] + d_data

            self.csvwriter.writerow(data4csv)

        except Exception as e:
            return e
