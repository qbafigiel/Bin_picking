import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera
import time

cam = OrbbecCamera()

try:
    cam.start()
    print("✅ Camera started successfully.")

    # próbujemy pobrać kilka klatek
    for _ in range(10):
        frame = cam.get_frame()
        if frame is None:
            print("⚠️ No frame received. Retrying...")
            time.sleep(0.1)
            continue

        print("Frame received:", frame["rgb"].shape, frame["timestamp"])
        break  # jeśli dostaliśmy klatkę, przerywamy

finally:
    cam.stop()
    print("Camera stopped.")
