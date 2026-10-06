import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Membaca citra berwarna
img = cv2.imread("image.jpeg")

# 2. Konversi ke Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Contrast Stretching pada citra grayscale
fmin, fmax = gray.min(), gray.max()
if fmax == fmin:
    # Hindari pembagian nol bila citra seragam (nilai min = max)
    stretched = gray.copy()
else:
    stretched = (gray.astype(np.float32) - fmin) / (fmax - fmin) * 255
    stretched = np.clip(stretched, 0, 255).astype(np.uint8)

# 4. Visualisasi Hasil Latihan
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("1. Citra Berwarna Asli")
plt.axis("off")

plt.subplot(2, 2, 2)
warna = ('b', 'g', 'r')
for i, col in enumerate(warna):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(hist, color=col)
plt.title("2. Histogram Warna (RGB)")
plt.xlabel("Intensitas Piksel")
plt.ylabel("Frekuensi")
plt.xlim([0, 256])

plt.subplot(2, 2, 3)
plt.imshow(gray, cmap="gray")
plt.title("3. Grayscale Asli")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(stretched, cmap="gray")
plt.title("4. Hasil Contrast Stretching")
plt.axis("off")

plt.tight_layout()
plt.show()
