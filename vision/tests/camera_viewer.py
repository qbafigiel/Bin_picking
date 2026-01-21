import sys
import os
import time
import cv2

# Dodajemy folder 'vision' do sys.path, żeby import działał w VS Code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera

def main():
    cam = OrbbecCamera()
    cam.start()
    print("Camera started. Press Q to quit.")

    frame_count = 0
    start_time = time.time()

    try:
        while True:
            frame_data = cam.get_frame()
            if frame_data is None:
                continue

            rgb = frame_data.get("rgb", None)
            if rgb is None:
                continue

            frame_count += 1
            cv2.imshow("Camera Viewer", rgb)

            # Klawisz Q kończy test
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            # Minimalna przerwa dla CPU
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Test interrupted by user.")

    finally:
        cam.stop()
        cv2.destroyAllWindows()
        elapsed = time.time() - start_time
        print(f"Frames received: {frame_count} in {elapsed:.2f} seconds")
        print(f"Average FPS: {frame_count / elapsed:.2f}")

if __name__ == "__main__":
    main()
