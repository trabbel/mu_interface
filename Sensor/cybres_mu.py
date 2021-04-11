#!/usr/bin/env python3
import serial


class Cybres_MU:

    def __init__(self, port_name):
        # initialization of serial communication
        self.ser = serial.Serial(
            port=port_name,
            baudrate=460800,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            xonxoff=False,
            rtscts=True,
            dsrdtr=True
        )
        # here I clean buffer, close and then open serial port again
        # after these three commands little green blink on MU should be seen
        self.ser.flushInput()
        self.ser.close()
        self.ser.open()


    def return_serial(self):
        return self.ser.read(100).decode('ascii')


    def restart(self):
        # restart MU
        self.ser.write(b'sr*')


    def start_measurement(self):
        # start measurement
        self.ser.write(b'ms*')
        

    def stop_measurement(self):
        # stop measurement
        self.ser.write(b'mp*')
