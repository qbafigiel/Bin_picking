import sys
import os
import cv2
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera.orbbec_camera import OrbbecCamera

# ====== GLOBAL ======
clicked_points = []   # lista punktów 3D
pixel_points = []     # lista pikseli
depth_frame_global = None

# ====== PARAMETRY KAMERY (PRZYBLIŻONE – później z intrinsics) ======
FX = 600.0
FY = 600.0
CX = 424.0
CY = 240.0


def depth_to_xyz(x, y, depth):
    """Konwersja piksel -> punkt 3D"""
    Z = depth
    X = (x - CX) * Z / FX
    Y = (y - CY) * Z / FY
    return X, Y, Z


def mouse_callback(event, x, y, flags, param):
    global depth_frame_global

    if event == cv2.EVENT_LBUTTONDOWN and depth_frame_global is not None:
        depth = depth_frame_global[y, x]

        if depth == 0:
            print("Brak danych depth w tym pikselu")
            return

        X, Y, Z = depth_to_xyz(x, y, depth)

        clicked_points.append((X, Y, Z))
        pixel_points.append((x, y))

        print(f"\nPunkt {len(clicked_points)}")
        print(f"Pixel: ({x}, {y})")
        print(f"3D: X={X:.1f} Y={Y:.1f} Z={Z:.1f} mm")

        # pomiar odległości między dwoma ostatnimi punktami
        if len(clicked_points) >= 2:
            p1 = np.array(clicked_points[-2])
            p2 = np.array(clicked_points[-1])
            dist = np.linalg.norm(p1 - p2)
            print(f"Odległość P{len(clicked_points)-1} -> P{len(clicked_points)} = {dist:.1f} mm")


def main():
    global depth_frame_global

    cam = OrbbecCamera(enable_depth=True)
    cam.start()

    cv2.namedWindow("Depth Probe")
    cv2.setMouseCallback("Depth Probe", mouse_callback)

    print("Klikaj w obraz depth. Q = wyjście")

    while True:
        frame = cam.get_frame()
        if frame is None or "depth" not in frame:
            continue

        depth = frame["depth"]
        depth_frame_global = depth.copy()

        # wizualizacja
        depth_vis = np.clip(depth, 200, 3000)
        depth_vis = cv2.normalize(depth_vis, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

        # rysowanie klikniętych punktów
        for i, (px, py) in enumerate(pixel_points):
            cv2.circle(depth_vis, (px, py), 5, (255, 255, 255), -1)
            cv2.putText(depth_vis, f"P{i+1}", (px+5, py-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        cv2.imshow("Depth Probe", depth_vis)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
