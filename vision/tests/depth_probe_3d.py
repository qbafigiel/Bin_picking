# depth_probe_3d.py
import sys
import os
import time
import cv2
import numpy as np

# Umożliwia import z vision/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera

def pixel_to_point(u, v, depth_value, intrinsics):
    """
    Zamienia piksel (u,v) i wartość głębi na współrzędne 3D w mm.
    intrinsics: dict z polami fx, fy, ppx, ppy
    """
    fx, fy = intrinsics['fx'], intrinsics['fy']
    ppx, ppy = intrinsics['ppx'], intrinsics['ppy']

    # Depth w mm
    Z = depth_value
    X = (u - ppx) * Z / fx
    Y = (v - ppy) * Z / fy
    return X, Y, Z

def main():
    cam = OrbbecCamera(enable_depth=True)
    cam.start()
    print("Camera started. Press Q to quit.")

    # Przybliżone intrinsics, jeśli nie mamy get_intrinsics():
    intrinsics = {
        'fx': 600.0,  # przykładowa wartość
        'fy': 600.0,
        'ppx': cam.width / 2,
        'ppy': cam.height / 2
    }

    try:
        while True:
            frame = cam.get_frame()
            if frame is None or 'depth' not in frame:
                continue

            depth = frame['depth']
            h, w = depth.shape

            # Środek obrazu
            u, v = w // 2, h // 2
            depth_value = depth[v, u]  # w mm

            X, Y, Z = pixel_to_point(u, v, depth_value, intrinsics)

            # Wyświetlanie depth w colormap
            depth_vis = np.clip(depth, 200, 3000)
            depth_vis = cv2.normalize(depth_vis, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

            # Krzyżyk w środku
            cv2.drawMarker(depth_vis, (u, v), (0, 0, 0), cv2.MARKER_CROSS, 20, 2)
            cv2.putText(depth_vis, f"Pixel: ({u},{v}) Depth: {int(depth_value)}mm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(depth_vis, f"3D Point: X={X:.1f} Y={Y:.1f} Z={Z:.1f} mm", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            cv2.imshow("Depth 3D Probe", depth_vis)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cam.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
