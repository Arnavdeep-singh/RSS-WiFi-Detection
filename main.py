import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time
import datetime
import subprocess
import scipy.ndimage

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
                    log[time] = int(signalLevel)*-1

except KeyboardInterrupt:
    print("Logging stopped. Plotting...")
    times, values = zip(*sorted(log.items()))
    smoothed = scipy.ndimage.gaussian_filter1d(values, sigma=5)
    plt.plot(times, values, label="Raw")
    plt.plot(times, smoothed, label="Smoothed", linewidth=2)
    plt.title("RSS over Time")
    plt.xlabel("Time")
    plt.ylabel("Signal Level (dBm)")
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.tight_layout()
    plt.show()

    
except subprocess.CalledProcessError as e:
    print(f"Command failed with retun code {e.returncode}")
