import time
import numpy as np
from pyorbbecsdk import *
from .frame_utils import color_frame_to_bgr

class OrbbecCamera:
    def __init__(self, width=640, fps=30):
        self.width = width
        self.fps = fps
        self.pipeline = Pipeline()
        self.config = Config()
        self.started = False
        self.ctx = Context()  # kontekst SDK przypisany do obiektu

    def start(self):
        """
        Uruchamia pipeline kamery i stream RGB.
        Zwraca True jeśli kamera działa, False jeśli brak urządzenia.
        """
        device_list = self.ctx.query_devices()
        if device_list.get_count() == 0:
            print("❌ No Orbbec camera detected! Check USB connection.")
            return False

        profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        try:
            color_profile = profile_list.get_video_stream_profile(self.width, 0, OBFormat.RGB, self.fps)
        except OBError:
            color_profile = profile_list.get_default_video_stream_profile()

        self.config.enable_stream(color_profile)
        self.pipeline.start(self.config)
        self.started = True
        print("✅ Camera started successfully.")
        return True

    def get_frame(self, timeout_ms=100):
        if not self.started:
            return None

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
        if self.started:
            self.pipeline.stop()
            self.started = False
