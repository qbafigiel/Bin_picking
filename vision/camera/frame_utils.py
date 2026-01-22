# vision/camera/frame_utils.py

import numpy as np
import cv2
from pyorbbecsdk import OBFormat


def color_frame_to_bgr(color_frame):
    """
    Konwertuje klatkę kolorową z Orbbec SDK do obrazu BGR (OpenCV).
    Obsługuje: RGB, BGR, MJPG
    """
    if color_frame is None:
        return None

    fmt = color_frame.get_format()
    width = color_frame.get_width()
    height = color_frame.get_height()
    data = np.frombuffer(color_frame.get_data(), dtype=np.uint8)

    # ===== RGB =====
    if fmt == OBFormat.RGB:
        image = data.reshape((height, width, 3))
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # ===== BGR =====
    if fmt == OBFormat.BGR:
        return data.reshape((height, width, 3))

    # ===== MJPG =====
    if fmt == OBFormat.MJPG:
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return image

    # ===== NIEOBSŁUGIWANY FORMAT =====
    raise RuntimeError(f"Unsupported color format: {fmt}")
