import cv2 as cv 
import numpy as np 
 
# 1. Membaca citra utama dan citra logo 
img1 = cv.imread('gambar1.jpeg') 
img2 = cv.imread('gambar2.jpg') 
 
if img1 is None or img2 is None: 
    raise FileNotFoundError("Gambar tidak ditemukan") 
 
# ----------------------------- 
# RESIZE LOGO 
# ----------------------------- 
# Menyesuaikan ukuran logo menjadi 1/4 lebar citra utama 
max_w = img1.shape[1] // 2 
scale = max_w / img2.shape[1] 
 
img2 = cv.resize( 
    img2,  (int(img2.shape[1] * scale), int(img2.shape[0] * scale)) 
) 
 
rows, cols, _ = img2.shape 
 
# ----------------------------- 
# ROI (Pojok Kiri Atas) 
# ----------------------------- 
# Mengambil wilayah ROI pada citra utama sebesar ukuran logo 
roi = img1[0:rows, 0:cols] 
 
# ----------------------------- 
# MASKING & PENGGABUNGAN 
# ----------------------------- 
# Konversi logo ke grayscale untuk membuat masker biner 
gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY) 
_, mask = cv.threshold(gray, 10, 255, cv.THRESH_BINARY_INV) 
mask_inv = cv.bitwise_not(mask) #bitwise_not 
 
# Isolasi latar belakang pada area ROI (melubangi tempat logo) 
img_bg = cv.bitwise_and(roi, roi, mask=mask) 
 
# Isolasi objek logo saja (tanpa latar belakangnya) 
img_fg = cv.bitwise_and(img2, img2, mask=mask_inv) #bitwise and 
 
# Gabungkan logo dengan latar belakang ROI 
dst = cv.add(img_bg, img_fg) #cv.add 
 
# Tempelkan kembali hasil gabungan ke pojok kiri atas citra utama 
img1[0:rows, 0:cols] = dst 
 
# Menampilkan hasil 
cv.imshow("Hasil Penggabungan Logo", img1) 
cv.waitKey(0) 
cv.destroyAllWindows() 