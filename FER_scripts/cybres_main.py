#!/usr/bin/env python3
import serial
import time


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


    def serial_open(self):
        try:
            self.ser.open()
        except:
            print('Serial port is already open.')

    def is_Open(self):
        print(self.ser.isOpen())

    def serial_close(self):
        # if you close serial port with this method MU needs restart --> BAD
        self.ser.flushInput()
        time.sleep(1)
        self.reset_buffer()
        time.sleep(1)
        self.ser.close()

    def reset_buffer(self):
        self.ser.reset_input_buffer()
        time.sleep(1)
        self.ser.reset_output_buffer()
        time.sleep(1)
        self.ser.write(b',') # reset input/output buffer of serial input --> MU command
    
    def print_serial(self):
        print(self.ser.read(100).decode('ascii'))
    
    def return_serial(self):
        return self.ser.read(100).decode('ascii')

    # documentation functions from MU-EIS_Manual_en.pdf Table 4
    # TODO put everything in "try-except" 

    def show_all_params(self):
        # show all parameters
        self.ser.write(b'ss*')
        print('All parameters:', self.ser.read(size=100).decode('ascii'))

    def restart_MU(self):
        # restart MU
        self.ser.write(b'sr*')

    def start_measurement(self):
        # start measurement
        self.ser.write(b'ms*')
        
    def stop_measurement(self):
        # stop measurement
        self.ser.write(b'mp*')

    def threads(self):
        pass