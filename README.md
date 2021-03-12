# Linux
## For setting up the sensor 
1. Turn on the sensor (wait till it beeps).
2. Type (in order to get rit of the error access denied): 
    ```sh
    sudo chmod 666 /dev/ttyACM0
    ```
3. Run the scripts with 
   ```bash
   python3 <scriptName>.py
   ```
   
   ## Thoughts on the linux scripts 
   For some reason the connection with linux is a hack around.

   to interact with the MU... there is a script (ctl_for_linux) which works sometimes. Description on how it works you find in the source code. 

   <br>
   <br>

   Tested the clt_for_linux on my virtual machine seems to work fine. If you start everything for the first time you do not need cutecom.. but doesnt work a second time it seems?!? -> for second time you need cutecom and then it works fine again

   <br>
   <br>

   clt_for_linux2.py works fine (tested on RP4; Linux 20.04). IMPORTANT: You have to follow the instructions inside the source code. (The MU3 needs to be restarted before each try).

   
   
# Windows 
1. Turn on sensor (wait till it beeps).
2. Go to directory where your code is 
3. run script
    ```cmd
   py <scriptname>.py
   ```
   For running the command line tool: 
   ```cmd
   py clt.py
   ```
# Sensor information (MU3)
Baud: 460800 <br>
Parity: None <br>
Data Bits: 8 <br>
Stop Bits: 1 <br>
Flow Control: None <br>
<br>
It seems that the sensor has to be restarted everytime you want to start a new connection. 

## For linux
Port: /dev/ttyACM0 (findet man mit tree /dev) <br>
<br>
get output from sensor in cutecom :
1. turn on sensor 
2. start measuring 
3. connect in cutecom

if it does not work just try to connect/disconnect a few times sometimes it works?

## For windows
Port: COM5 (findet man mit device manager) 

# clt.py
This is a command line tool, where you can send a comment (see user manual) and receive the corresponding response. 

# TODO List

Please try the script clt_for_linux2.py. (Follow the instruction inside the script closely. If you do not wait a few seconds/long enough it do not work but idk why!)
