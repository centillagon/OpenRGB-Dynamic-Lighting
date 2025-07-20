from openrgb import OpenRGBClient
from openrgb.utils import RGBColor
import mss
import numpy as np
import time

def get_average_screen_color():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        screenshot = np.array(sct.grab(monitor))[:, :, :3]
        avg_color = screenshot.mean(axis=(0, 1))
        return RGBColor(int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))

try:
    client = OpenRGBClient()
except TimeoutError:
    print("OpenRGB server not reachable. Make sure it's running with SDK support enabled.")
    exit(1)

client.clear()
devices = client.devices

print("Running screen ambient mode...")
try:
    while True:
        color = get_average_screen_color()
        for device in devices:
            device.set_color(color)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped.")
    client.clear()
