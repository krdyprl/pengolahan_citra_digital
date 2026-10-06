import cv2
import matplotlib.pyplot as plt

img = cv2.imread("image.jpeg")  # ganti sesuai nama file gambar kalian

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Citra Berwarna Asli")
plt.axis("off")

plt.subplot(1, 2, 2)
warna = ('b', 'g', 'r')
label = ('Biru', 'Hijau', 'Merah')
for i, col in enumerate(warna):
    hist = cv2.calcHist([img], [i], None, [256], [0, 256])
    plt.plot(hist, color=col, label=label[i])
plt.title("Histogram Warna (RGB Channel)")
plt.xlabel("Intensitas Piksel")
plt.ylabel("Frekuensi")
plt.xlim([0, 256])
plt.legend()

plt.tight_layout()
plt.show()
