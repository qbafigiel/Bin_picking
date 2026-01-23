# vision/camera/orbbec_camera.py

import time
import numpy as np
from pyorbbecsdk import (
    Pipeline,
    Config,
    Context,
    OBSensorType,
    OBFormat,
    OBError,
)
from .frame_utils import color_frame_to_bgr


class OrbbecCamera:
    def __init__(self, width=640, height=480, fps=30, enable_depth=False):
        """
        Driver Orbbec Camera.
        RGB: width, height, fps
        Depth: opcjonalny (enable_depth)
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.enable_depth = enable_depth

        self.pipeline = Pipeline()
        self.config = Config()
        self.ctx = Context()

        self.started = False

    def start(self):
        """
        Start pipeline kamery.
        """
        # === RGB ===
        profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        try:
            color_profile = profile_list.get_video_stream_profile(
                self.width, self.height, OBFormat.RGB, self.fps
            )
        except OBError:
            color_profile = profile_list.get_default_video_stream_profile()

        self.config.enable_stream(color_profile)

        # === DEPTH (1:1 jak u producenta) ===
        if self.enable_depth:
            depth_profiles = self.pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            depth_profile = depth_profiles.get_default_video_stream_profile()
            self.config.enable_stream(depth_profile)

        self.pipeline.start(self.config)
        self.started = True

    def get_frame(self, timeout_ms=100):
        """
        Zwraca:
        {
            "rgb": np.ndarray,
            "depth": np.ndarray (mm),
            "timestamp": float
        }
        """
        if not self.started:
            raise RuntimeError("Camera not started")

        frames = self.pipeline.wait_for_frames(timeout_ms)
        if frames is None:
            return None

        data = {"timestamp": time.time()}

        # === RGB ===
        color_frame = frames.get_color_frame()
        if color_frame:
            rgb = color_frame_to_bgr(color_frame)
            if rgb is not None:
                data["rgb"] = rgb

        # === DEPTH ===
        if self.enable_depth:
            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                return None

            if depth_frame.get_format() != OBFormat.Y16:
                return None

            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            depth = np.frombuffer(
                depth_frame.get_data(), dtype=np.uint16
            ).reshape((height, width))

            depth = depth.astype(np.float32) * scale  # mm
            data["depth"] = depth

        return data

    def stop(self):
        if self.started:
            self.pipeline.stop()
            self.started = False
