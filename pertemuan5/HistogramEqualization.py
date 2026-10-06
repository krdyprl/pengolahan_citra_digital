import cv2
import matplotlib.pyplot as plt

img = cv2.imread("image.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

equ = cv2.equalizeHist(gray)

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Asli")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(equ, cmap="gray")
plt.title("Hasil Histogram Equalization")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.hist(gray.ravel(), 256, (0, 256), color='k')
plt.title("Histogram Sebelum")

plt.subplot(2, 2, 4)
plt.hist(equ.ravel(), 256, (0, 256), color='k')
plt.title("Histogram Sesudah (Equalization)")

plt.tight_layout()
plt.show()
