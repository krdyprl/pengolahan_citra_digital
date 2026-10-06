import os

import cv2
import matplotlib.pyplot as plt

# 1. Baca citra dan ubah ke Grayscale
image_path = "gambar.png"
if not os.path.exists(image_path):
    image_path = "gpsimg.jpg"

img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Penerapan tiga pemrosesan lanjutan
_, thresh_inv = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
negatif = cv2.bitwise_not(gray)
rotasi = cv2.rotate(gray, cv2.ROTATE_90_CLOCKWISE)

# 3. Visualisasi hasil dalam grid 2 x 2
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale Asli")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(thresh_inv, cmap="gray", vmin=0, vmax=255)
plt.title("Binary Inverted (T=120)")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(negatif, cmap="gray", vmin=0, vmax=255)
plt.title("Citra Negatif")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(rotasi, cmap="gray", vmin=0, vmax=255)
plt.title("Rotasi 90° Searah Jarum Jam")
plt.axis("off")

plt.tight_layout()
plt.show()
