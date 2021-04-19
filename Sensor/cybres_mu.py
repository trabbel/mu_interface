#!/usr/bin/env python3
import serial


class Cybres_MU:

    def __init__(self, port_name, baudrate=460800):
        self.ser = serial.Serial(
            port=port_name,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            xonxoff=False,
            rtscts=True,
            dsrdtr=True
        )
        
        self.ser.flushInput()
        self.ser.close()
        self.ser.open()


    def return_serial(self):
        return self.ser.readline().decode('ascii')


    def restart(self):
        # restart MU
        self.ser.write(b'sr*')


    def start_measurement(self):
        # start measurement
        self.ser.write(b'ms*')
        

    def stop_measurement(self):
        # stop measurement
        self.ser.write(b'mp*')

    
    def set_measurement_interval(self, interval):
        # set interval between measurements
        set_interval = 'mi{:05}*'.format(interval)
        self.ser.write(set_interval.encode())

