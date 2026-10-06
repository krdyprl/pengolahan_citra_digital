import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('image.jpeg', cv.IMREAD_COLOR)

plt.subplot(1, 3, 1)
plt.hist(img[:, :, 0].ravel(), 256, [0, 256], color='b')
plt.title('Kanal Biru')
plt.xlabel('Intensitas Piksel')
plt.ylabel('Frekuensi')
plt.xlim([0, 256])

plt.subplot(1, 3, 2)
plt.hist(img[:, :, 1].ravel(), 256, [0, 256], color='g')
plt.title('Kanal Hijau')
plt.xlabel('Intensitas Piksel')
plt.ylabel('Frekuensi')
plt.xlim([0, 256])

plt.subplot(1, 3, 3)
plt.hist(img[:, :, 2].ravel(), 256, [0, 256], color='r')
plt.title('Kanal Merah')
plt.xlabel('Intensitas Piksel')
plt.ylabel('Frekuensi')
plt.xlim([0, 256])

plt.tight_layout()
plt.show()
