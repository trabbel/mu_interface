#!/usr/bin/env python3
from cybres_main import Cybres_MU
from datetime import datetime
from pathlib import Path

def make_file():
    file_path = '/tmp/watchplant/'
    Path(file_path).mkdir(parents=True, exist_ok=True) # make new directory
    file_name = datetime.now().strftime('%H:%M:%S_%d-%m-%Y') + '.txt'
    f = open(file_path + file_name, 'w')
    return f

if __name__ == "__main__":

    # on my laptop MU was usually connected as ACM1 or ACM2
    # change this if needed
    try:
        mu = Cybres_MU('/dev/ttyACM1')
    except:
        mu = Cybres_MU('/dev/ttyACM2')

    while True:
        command = input('''\n\nmeasure      -> start measurement and saves it in a file until 'ctrl+c' is pressed
start        -> starts measurement and prints it in terminal until 'ctrl+c' is pressed
stop         -> stops measurement
status       -> show all parameters, initial messages
reset_buffer -> reset input/output buffers of serial input
reset_MU     -> resets MU
open         -> open serial port
close        -> close serial port
exit         -> exit script
-----------------------------------------------------------------------------
write your command: ''')

        if command == 'measure':
            '''
            This mode collects data from sensors and saves it in a file.
            To stop measuring you need to press 'ctrl+c'. This is not 
            a good method to stop because we don't read everything but
            for testing purpose is good enough.
            '''
            print("press 'crtl+c' to stop measuring.")
            mu.start_measurement()
            f = make_file()
            try:
                while True:
                    f.write(mu.return_serial())
            except KeyboardInterrupt:
                f.close()
                print('Stop measurement.')
            mu.stop_measurement()

        elif command == 'start':
            '''
            Similar to mode 'measure', in this mode you start measuring
            and it will be printed in the terminal. If you want to stop PRINTING
            data in terminal, click 'ctrl+c', but this doesn't stop measuring.
            '''
            print("press 'crtl+c' to stop printing measurements.")
            mu.start_measurement()
            try:
                while True:
                    mu.print_serial()
            except KeyboardInterrupt:
                pass

        elif command == 'stop':
            '''
            with this command you stop measuring started with mode 'start'
            '''
            mu.stop_measurement()
            mu.print_serial()

        elif command == 'status':
            mu.show_all_params()
            mu.print_serial()
        
        elif command == 'reset_buffer':
            mu.reset_buffer()
        
        elif command == 'reset_MU':
            mu.restart_MU()

        elif command == 'open':
            mu.serial_open()
        
        elif command == 'close':
            mu.serial_close()
        
        elif command == 'exit':
            # before exiting from script we should restart MU
            mu.restart_MU()
            break