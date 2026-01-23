import sys
import os
import time
import cv2
import numpy as np

# Umożliwia import z vision/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera
from camera.orbbec_camera_detection import detect_cameras


def main():
    # === DETEKCJA KAMERY ===
    devices = detect_cameras()
    if not devices:
        print("❌ No Orbbec cameras detected.")
        return

    print(f"✅ Detected {len(devices)} camera(s). Using the first one.")

    # === START KAMERY ===
    cam = OrbbecCamera(enable_depth=True)
    cam.start()
    print("Camera started (RGB + Depth). Press Q to quit.")

    # === LICZNIKI DIAGNOSTYCZNE ===
    frame_count = 0
    start_time = time.time()

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                continue

            frame_count += 1
            elapsed = time.time() - start_time
            avg_fps = frame_count / elapsed if elapsed > 0 else 0

            # =========================
            # RGB VIEW
            # =========================
            if "rgb" in frame:
                rgb = frame["rgb"]
                h_rgb, w_rgb, _ = rgb.shape

                y0, dy = 30, 30
                cv2.putText(rgb, f"Elapsed: {elapsed:.2f} s", (10, y0),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(rgb, f"Frames: {frame_count}", (10, y0 + dy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(rgb, f"Avg FPS: {avg_fps:.2f}", (10, y0 + 2 * dy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(rgb, f"Resolution: {w_rgb}x{h_rgb}", (10, y0 + 3 * dy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow("RGB", rgb)

            # =========================
            # DEPTH VIEW
            # =========================
            if "depth" in frame:
                depth = frame["depth"]
                h_d, w_d = depth.shape

                # Odległość w centrum obrazu
                center_distance = depth[h_d // 2, w_d // 2]

                # Wizualizacja depth
                depth_vis = np.clip(depth, 200, 3000)
                depth_vis = cv2.normalize(
                    depth_vis, None, 0, 255, cv2.NORM_MINMAX
                ).astype(np.uint8)
                depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

                y0, dy = 30, 30
                cv2.putText(depth_vis, f"Avg FPS: {avg_fps:.2f}", (10, y0),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(depth_vis, f"Resolution: {w_d}x{h_d}", (10, y0 + dy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(depth_vis, f"Center depth: {int(center_distance)} mm",
                            (10, y0 + 2 * dy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                cv2.imshow("Depth", depth_vis)

            # === WYJŚCIE ===
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

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
