import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("image.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Contrast Stretching manual:
# g(x,y) = (f(x,y) - fmin) / (fmax - fmin) * 255
fmin, fmax = gray.min(), gray.max()
if fmax == fmin:
    # Hindari pembagian nol bila citra seragam (nilai min = max)
    stretched = gray.copy()
else:
    stretched = (gray.astype(np.float32) - fmin) / (fmax - fmin) * 255
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Asli")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(stretched, cmap="gray")
plt.title("Hasil Contrast Stretching")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.hist(gray.ravel(), 256, (0, 256), color='k')
plt.title("Histogram Sebelum")

plt.subplot(2, 2, 4)
plt.hist(stretched.ravel(), 256, (0, 256), color='k')
plt.title("Histogram Sesudah (Stretching)")

plt.tight_layout()
plt.show()
