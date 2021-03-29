import matplotlib.pyplot as plt
import glob
import os
from operator import methodcaller


if __name__ == "__main__":

    list_of_files = glob.glob('/tmp/watchplant/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    
    with open(latest_file, 'r') as meas_data:
        data = meas_data.readlines()[8:] # ignore header

    data = list(map(methodcaller("split", " "), data[1:-1])) # we ignore last measurement

    time = [i[0][11:] for i in data]
    temp = [int(i[24])/10000 for i in data]

    plt.figure(dpi=100)
    plt.plot(time, temp, marker='o')
    plt.grid(which='both')
    plt.title('Temperature from external sensor')
    plt.ylabel('Temperature in Celsius')
    plt.xlabel('Time, HH:MM:SS')
    plt.xticks(rotation=45)
    plt.show()
