import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.animation as animation
import time
import datetime
import subprocess
import scipy.ndimage

# change "wlo1" with your wifi interface.
wifiInt = "wlo1"

# init arrays
times = []
values = []
smoothed_values =[]

# Graph config
fig = plt.figure() 
line_raw= fig.add_subplot(1,1,1,label="raw")
fig.set_size_inches(10,4)
line_raw.set_title("RSS over Time")
line_raw.set_xlabel("Time")
line_raw.set_ylabel("Signal Level (dBm)")
plt.tight_layout()


def update(frame):
    try:
        rawData = subprocess.check_output(["iwconfig", wifiInt], text=True)
        lines = rawData.split('\n')
        for line in lines:
            if "Signal level=" in line:
                parts = line.strip().split("Signal level=")
                if len(parts) > 1:
                    # get Signal level and time
                    signalLevel = parts[1].split(' ')[0]
                    now = datetime.datetime.now()
                    # add values to log
                    values.append(int(signalLevel))
                    times.append(now)
                    #Update plot
                    line_raw.plot(times, values)

    except KeyboardInterrupt:
        print("Logging stopped")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with retun code {e.returncode}")

def plot(sm):
    plt.figure()
    plt.plot(times, values, label = "raw", alpha=0.4)
    plt.plot(times, sm, label="smoothed",linewidth=2)

    plt.title("RSS over Time (smoothed)")
    plt.xlabel("Time")
    plt.ylabel("Signal Level (dBm)")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # animation
    anim = animation.FuncAnimation(fig, update, interval = 100, cache_frame_data=False)
    plt.show()

    # Show smoothed graph animation ends.
    if times and values:
        smoothed = scipy.ndimage.gaussian_filter1d(values, sigma=2)
        plot(smoothed)

if __name__ == "__main__":
    main()
