import cv2
import numpy as np
from pyorbbecsdk import *

def main():
    # 🤖 Inicjalizacja urządzenia (Device)
    ctx = Context()            # Kontekst SDK
    device_list = ctx.get_device_list()
    if len(device_list) == 0:
        print("❌ Nie znaleziono żadnego urządzenia!")
        return
    device = device_list[0]     # wybieramy pierwsze urządzenie

    print("✅ Urządzenie wykryte:", device.get_device_info().get_name())

    # 🎥 Konfiguracja pipeline
    pipeline = Pipeline()
    config = Config()

    # Wybieramy profile strumieni (Color i Depth)
    color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
    depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)

    # Włączamy pierwszy profile RGB
    if color_profiles and color_profiles.get_count() > 0:
        color_profile = color_profiles.get_stream_profile_by_index(0)
        config.enable_stream(color_profile)
    else:
        print("⚠️ Brak profilu RGB!")
    
    # Włączamy pierwszy profil Depth
    if depth_profiles and depth_profiles.get_count() > 0:
        depth_profile = depth_profiles.get_stream_profile_by_index(0)
        config.enable_stream(depth_profile)
    else:
        print("⚠️ Brak profilu Depth!")

    # Start strumieni danych
    pipeline.start(config)

    # 🌀 Pętla główna
    while True:
        frames = pipeline.wait_for_frames(1000)
        if frames is None:
            print("⏱ Brak klatek, spróbuj ponownie...")
            continue

        # Pobranie klatki RGB
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        # Jeżeli brak klatki
        if color_frame is None or depth_frame is None:
            continue

        # Konwersja danych do numpy
        color_image = np.array(color_frame.to_numpy_array())
        depth_image = np.array(depth_frame.to_numpy_array())

        # Normalizacja obrazu głębokości do 0–255
        depth_norm = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX)
        depth_uint8 = depth_norm.astype(np.uint8)
        depth_colored = cv2.applyColorMap(depth_uint8, cv2.COLORMAP_JET)

        # Wyświetlenie obrazów
        cv2.imshow("RGB Camera", color_image)
        cv2.imshow("Depth Camera (colormap)", depth_colored)

        # Klawisz 'q' kończy działanie
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 🛑 Zatrzymanie i sprzątanie
    pipeline.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
