# import library
import cv2
import numpy as np

# - "image.jpeg" adalah ALAMAT (path/nama file) dari gambar yang akan diolah.
# - Angka 0 adalah FLAG (mode pembacaan gambar) untuk fungsi cv2.imread.
#   0 sama dengan cv2.IMREAD_GRAYSCALE, artinya gambar dibaca dalam mode
#   grayscale (hitam-putih / 1 channel), bukan berwarna (BGR / 3 channel).
#   Mode grayscale dipakai di sini supaya citra langsung berbentuk 1 channel,
#   sehingga lebih ringan dan cocok untuk perhitungan histogram di bawah.
#   (Sebagai perbandingan: 1 = berwarna/BGR, -1 = apa adanya/termasuk alpha)

img = cv2.imread("image.jpeg", 0)

# Perhitungan histogram menggunakan OpenCV
hist_cv = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_cv = hist_cv.flatten()  # pastikan jadi array 1 dimensi

# Perhitungan histogram menggunakan NumPy
hist_np, bins = np.histogram(img.ravel(), 256, [0, 256])

# Cetak hasil hanya pada intensitas kelipatan 20
print(f"{'Intensitas':>10} | {'OpenCV':>10} | {'NumPy':>10}")
print("-" * 38)
for i in range(0, 256, 20):
    print(f"{i:>10} | {int(hist_cv[i]):>10} | {int(hist_np[i]):>10}")
