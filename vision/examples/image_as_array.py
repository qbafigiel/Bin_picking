import numpy as np

# "obraz" 3x3 piksele, każdy piksel ma 3 kanały (RGB)
image = np.array([
    [[255, 0, 0],   [0, 255, 0],   [0, 0, 255]],
    [[255, 255, 0], [0, 255, 255], [255, 0, 255]],
    [[128, 128, 128],[50, 50, 50], [200, 200, 200]]
])

print(image)
print("Shape:", image.shape)
pixel = image[0, 0]
print("Pixel (0,0):", pixel)
