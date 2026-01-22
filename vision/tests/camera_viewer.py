# vision/tests/camera_viewer.py

import sys
import os
import time
import cv2

# Dodajemy folder 'vision' do sys.path, żeby import działał w VS Code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera
from camera.orbbec_camera_detection import detect_cameras


def main(width=424, height=240, fps=60):
    # === Sprawdzamy, czy są podłączone kamery ===
    devices = detect_cameras()
    if not devices:
        print("❌ No Orbbec cameras detected! Connect a camera and try again.")
        return

    print(f"✅ Detected {len(devices)} camera(s). Using the first one.")

    cam = OrbbecCamera(width=width, height=height, fps=fps)
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

            # Wyświetlamy FPS i czas w liniach jeden pod drugim
            y0, dy = 30, 30
            cv2.putText(rgb, f"Elapsed: {elapsed:.2f} s", (10, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(rgb, f"Frames: {frame_count}", (10, y0 + dy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(rgb, f"Avg FPS: {avg_fps:.2f}", (10, y0 + 2*dy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Camera Viewer", rgb)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

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
