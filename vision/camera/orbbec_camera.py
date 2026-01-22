# vision/camera/orbbec_camera.py

import time
import numpy as np
from pyorbbecsdk import Pipeline, Config, Context, OBSensorType, OBFormat, OBError
from .frame_utils import color_frame_to_bgr


class OrbbecCamera:
    def __init__(self, width=640, height=480, fps=30):
        """
        Driver Orbbec Camera.
        width, height, fps - parametry streamu RGB.
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.pipeline = Pipeline()
        self.config = Config()
        self.started = False
        self.ctx = Context()  # kontekst SDK

    def start(self):
        """
        Startuje pipeline kamery.
        """
        profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)

        try:
            color_profile = profile_list.get_video_stream_profile(
                self.width, self.height, OBFormat.RGB, self.fps
            )
        except OBError:
            color_profile = profile_list.get_default_video_stream_profile()

        self.config.enable_stream(color_profile)
        self.pipeline.start(self.config)
        self.started = True

    def get_frame(self, timeout_ms=100):
        """
        Pobiera jedną klatkę RGB.
        Zwraca słownik {"rgb": np.array, "timestamp": float}
        """
        if not self.started:
            raise RuntimeError("Camera not started")

        frames = self.pipeline.wait_for_frames(timeout_ms)
        if frames is None:
            return None

        color_frame = frames.get_color_frame()
        if color_frame is None:
            return None

        color_image = color_frame_to_bgr(color_frame)
        if color_image is None:
            return None

        return {"rgb": color_image, "timestamp": time.time()}

    def stop(self):
        """
        Zatrzymuje pipeline kamery.
        """
        if self.started:
            self.pipeline.stop()
            self.started = False
