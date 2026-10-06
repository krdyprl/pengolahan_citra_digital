import cv2
import matplotlib.pyplot as plt

# 1. Baca citra dan ubah ke Grayscale
img = cv2.imread("image.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Hitung histogram dengan OpenCV
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

# 3. Visualisasi
plt.subplot(1, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("Citra Grayscale")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.plot(hist, color='k')
plt.title("Histogram Citra Grayscale")
plt.xlabel("Intensitas Piksel")
plt.ylabel("Frekuensi")
plt.xlim([0, 256])

plt.tight_layout()
plt.show()
