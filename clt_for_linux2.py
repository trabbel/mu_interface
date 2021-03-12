import time
import serial

# you have to wait a few seconds between each step
# 1. turn on MU3 
# 2. start measuring 
# 3. run this script 


ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=460800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1
)

while 1:
    #read(print.ser(1))
    if ser.read(1):
        print("connected")
        break
    ser.reset_input_buffer()
    ser.reset_output_buffer()    
    ser.close()
    ser.open()
    ser.reset_input_buffer()
    ser.reset_output_buffer()    
    print("try connecting ...")
    time.sleep(1)
        

ser.reset_input_buffer()
ser.reset_output_buffer()

inp = "mp*"  # stop measuring command see user maual
ser.write([ord(e) for e in inp])

# reset buffers -> idk if necessary?
ser.reset_input_buffer()
ser.reset_output_buffer()

# normal control loop
print('Enter your commands below.\r\nInsert "exit" to leave the application.')
while 1:
    inp = input(">> ")
    if inp == 'exit':
        ser.close()
        exit()
    else:
        ser.write([ord(e) for e in inp])
        out = []
        time.sleep(1)
        while ser.inWaiting() > 0:
            out.append(ser.read(1))

        print(">> " + str(b''.join(out).decode('ascii')))
