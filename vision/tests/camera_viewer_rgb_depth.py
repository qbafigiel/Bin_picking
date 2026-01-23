# vision/tests/camera_viewer_rgb_depth.py

import sys
import os
import time
import cv2
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera
from camera.orbbec_camera_detection import detect_cameras


def main():
    devices = detect_cameras()
    if not devices:
        print("❌ No Orbbec cameras detected.")
        return

    cam = OrbbecCamera(enable_depth=True)
    cam.start()
    print("Camera started (RGB + Depth). Press Q to quit.")

    frame_count = 0
    start_time = time.time()

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                continue

            frame_count += 1
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0

            # === RGB ===
            if "rgb" in frame:
                rgb = frame["rgb"]
                cv2.putText(
                    rgb, f"FPS: {fps:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
                )
                cv2.imshow("RGB", rgb)

            # === DEPTH ===
            if "depth" in frame:
                depth = frame["depth"]

                depth_vis = np.clip(depth, 200, 3000)
                depth_vis = cv2.normalize(
                    depth_vis, None, 0, 255, cv2.NORM_MINMAX
                ).astype(np.uint8)

                depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
                cv2.imshow("Depth", depth_vis)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cam.stop()
        cv2.destroyAllWindows()
        print("Stopped.")


if __name__ == "__main__":
    main()
