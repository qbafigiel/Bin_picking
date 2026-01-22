# vision/camera/orbbec_camera.py

import time
from pyorbbecsdk import *
from .frame_utils import color_frame_to_bgr


class OrbbecCamera:
    def __init__(self, width=640, fps=30):
        self.width = width
        self.fps = fps
        self.pipeline = Pipeline()
        self.config = Config()
        self.started = False

    def start(self):
        """
        Uruchamia pipeline kamery i stream RGB.
        """
        # Pobranie listy profili streamów dla sensora RGB
        profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)

        try:
            # Staramy się wybrać profil o zadanej szerokości i fps
            color_profile = profile_list.get_video_stream_profile(self.width, 0, OBFormat.RGB, self.fps)
        except OBError:
            # W razie problemu wybieramy profil domyślny
            color_profile = profile_list.get_default_video_stream_profile()

        # Włączamy strumień i startujemy pipeline
        self.config.enable_stream(color_profile)
        self.pipeline.start(self.config)
        self.started = True

    def get_frame(self, timeout_ms=100):
        """
        Pobiera jedną klatkę z kamery.
        Zwraca słownik: {"rgb": <numpy array>, "timestamp": <czas>}
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

        return {
            "rgb": color_image,
            "timestamp": time.time(),
        }

    def stop(self):
        """
        Zatrzymuje pipeline kamery.
        """
        if self.started:
            self.pipeline.stop()
            self.started = False
