import sys
import os
import time
import cv2
import numpy as np

# Umożliwia import z vision/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera
from camera.orbbec_camera_detection import detect_cameras


# =========================
# GLOBAL STATE – DEPTH PROBE
# =========================
probe_x = None
probe_y = None


def on_mouse_depth(event, x, y, flags, param):
    global probe_x, probe_y
    if event == cv2.EVENT_LBUTTONDOWN:
        probe_x = x
        probe_y = y
        print(f"[DEPTH PROBE] Click at pixel: x={x}, y={y}")


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

    cv2.namedWindow("Depth")
    cv2.setMouseCallback("Depth", on_mouse_depth)

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
                h, w, _ = rgb.shape

                cv2.putText(rgb, f"FPS: {avg_fps:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(rgb, f"Resolution: {w}x{h}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow("RGB", rgb)

            # =========================
            # DEPTH VIEW + PROBE
            # =========================
            if "depth" in frame:
                depth = frame["depth"]
                h_d, w_d = depth.shape

                # Wizualizacja depth
                depth_vis = np.clip(depth, 200, 3000)
                depth_vis = cv2.normalize(depth_vis, None, 0, 255, cv2.NORM_MINMAX)
                depth_vis = depth_vis.astype(np.uint8)
                depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

                cv2.putText(depth_vis, f"FPS: {avg_fps:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(depth_vis, f"Resolution: {w_d}x{h_d}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # === DEPTH PROBE ===
                if probe_x is not None and probe_y is not None:
                    if 0 <= probe_x < w_d and 0 <= probe_y < h_d:
                        center_depth = depth[probe_y, probe_x]

                        # ROI 5x5
                        r = 2
                        x0 = max(0, probe_x - r)
                        x1 = min(w_d, probe_x + r + 1)
                        y0 = max(0, probe_y - r)
                        y1 = min(h_d, probe_y + r + 1)

                        roi = depth[y0:y1, x0:x1]
                        valid = roi[roi > 0]

                        median_depth = int(np.median(valid)) if valid.size > 0 else 0

                        # Krzyżyk
                        cv2.drawMarker(
                            depth_vis,
                            (probe_x, probe_y),
                            (255, 255, 255),
                            markerType=cv2.MARKER_CROSS,
                            markerSize=20,
                            thickness=2,
                        )

                        # Overlay tekstu
                        cv2.putText(
                            depth_vis,
                            f"Pixel: ({probe_x}, {probe_y})",
                            (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 255),
                            2,
                        )
                        cv2.putText(
                            depth_vis,
                            f"Depth (center): {int(center_depth)} mm",
                            (10, 130),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 255),
                            2,
                        )
                        cv2.putText(
                            depth_vis,
                            f"Depth (median 5x5): {median_depth} mm",
                            (10, 160),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 255),
                            2,
                        )

                cv2.imshow("Depth", depth_vis)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cam.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
