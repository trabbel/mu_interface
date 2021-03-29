# wp_interface - FER Zagreb

Here are some scripts to test the work of MU. Each script will be briefly explained below. The scripts themselves are also commented on, so read the comments in the scripts before running.

### cybres_main.py
This script contains the class * Cybres_MU * which contains methods for MU programming. As you will see, the methods are clear and simple.
  

### commands_test.py
This script makes an object of class * Cybres_MU *. This opens a serial connection. The script has a somewhat ‘nice’ interface for testing the most important commands. The main thing with this is that you don’t have to run the measurement manually, it can be run by a script. Also, if you want to exit, the device with the script will restart, and then you need to wait a few seconds and hear a few beeps, after which the script of those beeps can restart without any problems.

Another feature of this script is the * measure * mode, which will save the measured data to a file. For now, the file is saved in the * / tmp / watch plant / * directory which was also created in this script. Feel free to change the place where you want it to be saved.
  
### plot_temperature.py
This script will plot the measured temperature. It is here to test the saved data from the * commands_test.py * script.

### TODO list
- put each method in a mode other than trying
- make threads for writing to files, remove * KeyboardInterrupt * exception.