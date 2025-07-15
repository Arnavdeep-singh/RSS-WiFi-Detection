import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import subprocess


# change "wlo1" with your wifi interface.
wifiInt = "wlo1"
log = {}

try:

    while True:
        rawData = subprocess.check_output(["iwconfig", wifiInt], text=True)
        lines = rawData.split('\n')
        for line in lines:
            if "Signal level=" in line:
                parts = line.strip().split("Signal level=")
                if len(parts) > 1:
                    signalLevel = parts[1].split(' ')[0]
                    time = datetime.datetime.now()
                    log[f"{time}"] = signalLevel

except KeyboardInterrupt:
    print("Logging stopped. Plotting...")
    plt.plot(*zip(*sorted(log.items())))
    plt.show()

    
except subprocess.CalledProcessError as e:
    print(f"Command failed with retun code {e.returncode}")
