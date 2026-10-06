import cv2
import matplotlib.pyplot as plt  

# 1. Baca citra dan ubah ke Grayscale
img = cv2.imread("gpsimg.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Penerapan Thresholding Manual & Otsu
_, thresh_binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
_, thresh_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY +
cv2.THRESH_OTSU)

# 3. Visualisasi Hasil
plt.figure(figsize=(10, 4))
plt.subplot(1, 3, 1)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Asli")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(thresh_binary, cmap="gray")
plt.title("Binary Threshold (T=127)")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(thresh_otsu, cmap="gray")
plt.title("Otsu Thresholding")
plt.axis("off")
plt.tight_layout()
plt.show()