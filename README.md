# UzL WatchPlant setup

This is the planned structure for the WatchPlant data collection setup at UzL. The scripts in the folder Edge_Device will run on one RPi to collect data, the scripts in the folder Sensor will run on RPis connected to a Cybres MU (works only with one Sensor right now, support for multiple sensors will be added). On both the Edge_Device and Sensor is one main.py file. They are the starting point and the only files that must be executed.

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


