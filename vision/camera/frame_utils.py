import numpy as np
import cv2
from pyorbbecsdk import OBFormat


def color_frame_to_bgr(color_frame):
    width = color_frame.get_width()
    height = color_frame.get_height()
    fmt = color_frame.get_format()
    data = color_frame.get_data()

    image = np.frombuffer(data, dtype=np.uint8)

    if fmt == OBFormat.RGB:
        image = image.reshape((height, width, 3))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image

    elif fmt == OBFormat.BGR:
        image = image.reshape((height, width, 3))
        return image

    else:
        raise RuntimeError(f"Unsupported color format: {fmt}")
