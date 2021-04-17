# UzL WatchPlant setup

This is the planned structure for the WatchPlant data collection setup at UzL. The scripts in the folder Edge_Device will run on one RPi to collect data, the scripts in the folder Sensor will run on RPis connected to a Cybres MU (works only with one Sensor right now, support for multiple sensors will be added). On both the Edge_Device and Sensor is one *main.py* file. They are the starting point and the only files that must be executed.

## Regarding ZMQ
### Sending data
The files are only tested locally until now, to send data from and to the exact same device. To use ZMQ for wireless network communication, the addresses in the classes *ZMQ_Publisher* and *ZMQ_Subscriber* must be changed. Refer to [the ZMQ documentation](http://api.zeromq.org/3-2:zmq-tcp) for more information.
### Message format
ZMQ allows to send custom message formats using [multipart messages](http://api.zeromq.org/3-2:zmq-send). Every message send to the edge device consists of two parts: The header and the payload. The header is a numpy array with two integers, the first is the sensor number (can be given as parameter for the *Sensor_Node*), e.g. 0. The second is an integer between 0 and 3 and specifies the type of payload (the MU can send four different message types):
|Number|Message Type|Payload|
|---|---|---|  
| 0 | MU data header | String|
| 1 | Device ID | numpy array with one field|
| 2 | Measurement Mode | numpy array with one field|
| 3 | Measurement Data | numpy array |

The measurement data array consists of the split string from the MU. The first 6 fields are the timestamp, after that follow 44 fields with data. If the timestamp should be generated on the edge device, uncomment line 56 and comment line 57 in *sensor_node.py*. Then the array will only consist of 44 data fields without timestamp.

## Sensor
### sensor_node.py
Contains the main class *Sensor_Node*, which handles the program logic of the sensor.
### cybres_mu.py
Contains the class *Cybres_MU*, a minimal variant of the FER script for accessing the Cybres MU.
### zmq_publisher.py
Contains the class *ZMQ_Publisher* for wireless communication between sensor and edge device using [ZeroMQ](https://zeromq.org). It will send the data from the Cybres MU.

## Edge_Device 
### edge_device.py
Contains the main class *Edge_Device*, which handles the program logic of the edge device.
### zmq_subscriber.py
Contains the class *ZMQ_Subscriber* for wireless communication between sensor and edge device using [ZeroMQ](https://zeromq.org). It will receive the data from the Cybres MU

## TODO
- [x] Specify a data format of Cybres MU messages for ZMQ communication. At the moment it's sent as string object.
- [ ] Write a visualization class to output diagrams with [GNUplot](http://gnuplot.info) or [Matplotlib](https://matplotlib.org/)
- [ ] Built setup at the UzL biohybrid lab
- [ ] Save data in a file. Right now the edge device prints it in terminal because the final storage location is not clear yet.
- [ ] Modify the scripts to use multiple sensors


