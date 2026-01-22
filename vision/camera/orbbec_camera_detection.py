# vision/camera/orbbec_camera_detection.py

from pyorbbecsdk import Context

def detect_cameras():
    """
    Sprawdza podłączone kamery Orbbec.
    Zwraca listę urządzeń. Pusta lista = brak urządzeń.
    """
    ctx = Context()
    device_list = ctx.query_devices()
    
    if  device_list.get_count() == 0:
        return []
    return device_list
