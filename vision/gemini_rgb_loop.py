# gemini_rgb_loop.py
import time
import cv2
import numpy as np
from pyorbbecsdk import Context

print("Creating Orbbec context...")
ctx = Context()

device_list = ctx.query_devices()
if device_list.get_count() == 0:
    print("No devices found.")
    exit(1)

device = device_list[0]

# Pobieramy listę sensorów i wybieramy pierwszy (zakładamy RGB)
sensors = device.get_sensor_list()
rgb_sensor = sensors[0]  # w Twoim przypadku sensor 0

print("Starting camera loop. Press 'q' to quit.")

frame_count = 0
start_time = time.time()

while True:
    frame = rgb_sensor.get_frame()
    if frame is None:
        continue

    image = np.array(frame)

    cv2.imshow("RGB Camera", image)

    frame_count += 1
    elapsed = time.time() - start_time
    if elapsed >= 1.0:
        print(f"FPS: {frame_count}")
        frame_count = 0
        start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
