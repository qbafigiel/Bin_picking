# gemini_rgb_fps.py
import time
import cv2
import numpy as np
from pyorbbecsdk import Context

# 1. Tworzymy kontekst SDK
print("Creating Orbbec context...")
ctx = Context()

# 2. Pobieramy listę urządzeń
device_list = ctx.query_devices()
num_devices = device_list.get_count()
print(f"Devices count: {num_devices}")

if num_devices == 0:
    print("No Orbbec devices found.")
    exit(1)

# 3. Wybieramy pierwsze urządzenie
device = device_list[0]  # w v2, device_list zachowuje się jak lista

# 4. Sprawdzamy dostępne sensory
sensors = device.get_sensor_list()
print("Sensors available:")
for idx, sensor in enumerate(sensors):
    print(idx, sensor)

# 5. Wybieramy sensor RGB (zakładamy, że to sensor index 0 lub szukamy po typie)
rgb_sensor = sensors[0]  # uproszczenie; później można filtrować po typie

# 6. Pętla pobierania obrazu + liczenie FPS
frame_count = 0
start_time = time.time()

print("Starting camera loop. Press 'q' to quit.")
while True:
    frame = rgb_sensor.get_frame()  # pobiera jedną klatkę
    if frame is None:
        continue  # czasami może nie być klatki, pomijamy

    # Konwertujemy do formatu numpy (OpenCV)
    image = np.array(frame)

    # Wyświetlamy obraz
    cv2.imshow("RGB Camera", image)

    frame_count += 1
    elapsed = time.time() - start_time
    if elapsed >= 1.0:  # co sekundę wypisujemy FPS
        print(f"FPS: {frame_count}")
        frame_count = 0
        start_time = time.time()

    # Wyjście po naciśnięciu 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Sprzątanie
cv2.destroyAllWindows()
