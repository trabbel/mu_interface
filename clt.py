import time
import serial
from sys import platform

if platform == 'win32':  # todo can we generalize this
    p = 'COM5'
elif platform == 'linux':
    p = '/dev/ttyACM0',
else:
    print("cannot determine OS!")
    print(platform)
    exit()



ser = serial.Serial(
    port=p,
    baudrate=460800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

inp = 1
while 1:
    inp = input(">> ")
    if inp == 'exit':
        ser.close()
        exit()
    else:
        ser.write(inp.encode())
        out = []
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out.append(ser.read(1))

        if out != '':
            print(">>" + str(b''.join(out).decode('ascii')))
