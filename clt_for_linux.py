import time
import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=460800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# 1. start MU
# 2. start measuring at MU
# 3. cross fingers then start this program and pray
# 4. open the same port with cutecom (repeat until you get output -> takes me 2 to 3 times)
# 5. if there is some output press crtl + c in the terminal
# 6. use as normal ctl

# (to restart any application you have to turn everything of and start over again!)

try:
    while 1:
        print(ser.read(1))

except KeyboardInterrupt:
    # reset buffers -> idk if necessary?
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