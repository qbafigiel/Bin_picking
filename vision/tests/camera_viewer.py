# vision/tests/camera_viewer.py

import time
import cv2
import sys
import os

# Dodajemy folder vision do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from camera.orbbec_camera import OrbbecCamera

def main():
    cam = OrbbecCamera()
    cam.start()
    print("Camera started. Press Q to quit.")

    frame_count = 0
    total_frames = 0
    start_time = time.time()
    fps_update_time = start_time
    avg_fps = 0

    while True:
        frame_data = cam.get_frame()
        if frame_data is None:
            continue

        rgb = frame_data.get("rgb")
        if rgb is None:
            continue

        frame_count += 1
        total_frames += 1

        elapsed_total = time.time() - start_time
        elapsed_fps = time.time() - fps_update_time

        # Wyliczenie FPS co 1 sekundę
        if elapsed_fps >= 1.0:
            avg_fps = frame_count / elapsed_fps
            frame_count = 0
            fps_update_time = time.time()

        # Dodanie informacji na obrazie
        display = rgb.copy()
        cv2.putText(display, f"Elapsed: {elapsed_total:.2f} s", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(display, f"FPS: {avg_fps:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(display, f"Total frames: {total_frames}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Camera Viewer", display)

        # Klawisz Q kończy test
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Sprzątanie
    cam.stop()
    cv2.destroyAllWindows()
    total_elapsed = time.time() - start_time
    print("\n=== TEST SUMMARY ===")
    print(f"Frames received: {total_frames}")
    print(f"Elapsed time:   {total_elapsed:.2f} s")
    print(f"Average FPS:    {total_frames / total_elapsed:.2f}")

if __name__ == "__main__":
    main()
