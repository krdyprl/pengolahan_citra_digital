import cv2
import matplotlib.pyplot as plt

# 1. Baca citra berwarna lalu konversi ke grayscale
img = cv2.imread("image.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Terapkan histogram equalization
equ = cv2.equalizeHist(gray)

# 3. Tampilkan dalam grid 2 x 2
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("1. Citra Grayscale Asli")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.hist(gray.ravel(), 256, (0, 256), color='k')
plt.title("2. Histogram Grayscale Asli")
plt.xlabel("Intensitas Piksel")
plt.ylabel("Frekuensi")
plt.xlim([0, 256])

plt.subplot(2, 2, 3)
plt.imshow(equ, cmap="gray")
plt.title("3. Citra Hasil Equalization")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.hist(equ.ravel(), 256, (0, 256), color='k')
plt.title("4. Histogram Hasil Equalization")
plt.xlabel("Intensitas Piksel")
plt.ylabel("Frekuensi")
plt.xlim([0, 256])

plt.tight_layout()
plt.show()
