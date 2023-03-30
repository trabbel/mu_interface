from subprocess import Popen
import sys

port = sys.argv[1]
filename = "main.py"
while True:
    print("\nStarting " + filename)
    p = Popen(f"python3 {filename} --port {port} --int 1000", shell=True)
    p.wait()