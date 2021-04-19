from Sensor.zmq_publisher import ZMQ_Publisher
from Sensor.cybres_mu import Cybres_MU
import numpy as np

Pub = ZMQ_Publisher()
header = np.array([1, 1])
payload1 = "hallo"
payload2 = np.array([1, 1, 3, 4, 5])
mu = Cybres_MU('/dev/ttyACM0')

mu.start_measurement()
while True:
    #Pub.publish(header, payload2)
    print(mu.return_serial())