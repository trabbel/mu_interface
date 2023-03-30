from subprocess import Popen
import sys

port = sys.argv[1]
addr = sys.argv[2]
filename = "main.py"
while True:
    print("\nStarting " + filename)
    p = Popen(f"python3 {filename} --port {port} --int 1000 --addr {addr}", shell=True)
    p.wait()
