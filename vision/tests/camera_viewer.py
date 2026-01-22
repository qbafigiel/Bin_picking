# vision/tests/camera_viewer.py

import sys
import os
import time
import cv2

# Dodajemy folder 'vision' do sys.path, żeby import działał w VS Code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera
from camera.orbbec_camera_detection import detect_cameras


def main():
    # === Sprawdzamy, czy są podłączone kamery ===
    devices = detect_cameras()
    if not devices:
        print("❌ No Orbbec cameras detected! Connect a camera and try again.")
        return

    # Wybieramy pierwszą kamerę
    print(f"✅ Detected {len(devices)} camera(s). Using the first one.")

    cam = OrbbecCamera()
    cam.start()
    print("Camera started successfully. Press Q to quit.")

    frame_count = 0
    start_time = time.time()

    try:
        while True:
            frame_data = cam.get_frame()
            if frame_data is None:
                continue

            rgb = frame_data.get("rgb")
            timestamp = frame_data.get("timestamp")

            frame_count += 1
            elapsed = time.time() - start_time
            avg_fps = frame_count / elapsed if elapsed > 0 else 0

            # Wyświetlamy FPS, liczbę klatek i czas w trzech liniach
            y0 = 30  # początkowa pozycja Y
            dy = 30  # odstęp między liniami
            texts = [
                f"Elapsed: {elapsed:.2f} s",
                f"Frames: {frame_count}",
                f"Avg FPS: {avg_fps:.2f}"
            ]
            for i, text in enumerate(texts):
                y = y0 + i * dy
                cv2.putText(rgb, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Camera Viewer", rgb)

            # Wyjście po naciśnięciu 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Minimalna przerwa dla CPU
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nTest interrupted by user.")

    finally:
        cam.stop()
        cv2.destroyAllWindows()
        elapsed = time.time() - start_time
        avg_fps = frame_count / elapsed if elapsed > 0 else 0
        print("\n=== TEST SUMMARY ===")
        print(f"Frames received: {frame_count}")
        print(f"Elapsed time:   {elapsed:.2f} s")
        print(f"Average FPS:    {avg_fps:.2f}")


if __name__ == "__main__":
    main()
