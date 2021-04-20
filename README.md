# WatchPlant data collection setup

This is the planned structure for the WatchPlant data collection setup. The scripts in the folder Edge_Device will run on one RPi to collect data, the scripts in the folder Sensor will run on RPis connected to a Cybres MU. *Utilities* are required by all RPis. On both the Edge Device and Sensor is one *main.py* file. They are the starting point and the only files that must be executed.

## Needed software
To run the scripts, a python 3 installation is needed. Also pip install the following packages: 
```bash
pip3 install pyserial numpy zmq
```
Note: Both the packages *zmq* and *pyzmq* work.
## File saving
The measured data gets saved as .csv file both on the Sensor Node and the Edge Device. Default location for the Sensor Node resp. Edge Device are ``/home/$USER/measurements`` resp. ``/home/$USER/measurements/hostname``, where ``hostname`` is the hostname of the Sensor Node which sent the data.
## Sending data
Edge Device and Sensor Nodes communicate wirelessly using [ZeroMQ](https://zeromq.org/). Depending on the local network setup, the addresses in the classes *ZMQ_Publisher* and *ZMQ_Subscriber* must be changed. Refer to [the ZMQ documentation](http://api.zeromq.org/3-2:zmq-tcp) for more information.

## Message format
ZMQ allows to send custom message formats using [multipart messages](http://api.zeromq.org/3-2:zmq-send). Every message send to the edge device consists of two parts: The header and the payload. The header is a python dictionary with two entries, the first is the Sensor Node's hostname. The second is an integer between 0 and 3 and specifies the type of payload (the MU can send four different message types):
|Number|Message Type|Payload|
|---|---|---|  
| 0 | MU data header | String|
| 1 | Device ID | numpy array with one field|
| 2 | Measurement Mode | numpy array with one field|
| 3 | Measurement Data | numpy array with 45 fields|

The measurement data array consists of the split string from the MU. 

The hostnames should be named as ``rpi[index]``, e.g.: ``rpi0``, ``rpi1``, ...


