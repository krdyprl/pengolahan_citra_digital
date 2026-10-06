import cv2 as cv 
import numpy as np 
 
# 1. Membaca dua gambar berekstensi jpg dan jpeg
img1 = cv.imread('nu.png') 
img2 = cv.imread('gambar2.jpg') 
 
# 2. Menyamakan ukuran (resolusi) img2 dengan img1 
# h (tinggi), w (lebar), c (channel/warna) diambil otomatis oleh Python 
h, w, c = img1.shape 
img2 = cv.resize(img2, (w, h)) 
 
# 3. Image Subtraction menggunakan OpenCV (cv.subtract) 
# Sifat: Saturated -> jika hasil kurang dari 0, nilainya mentok di 0 (hitam) 
res_opencv = cv.subtract(img1, img2) 
 
# 4. Image Subtraction menggunakan NumPy (img1 - img2) 
# Sifat: Modulo -> jika hasil negatif, akan berputar ke angka mendekati 255 
res_numpy = img1 - img2 
 
# 5. Menampilkan hasil 
cv.imshow('Gambar 1 Asli', img1) 
cv.imshow('Gambar 2 Asli', img2) 
cv.imshow('Hasil OpenCV (cv.subtract)', res_opencv) 
cv.imshow('Hasil NumPy (img1 - img2)', res_numpy) 
 
cv.waitKey(0) 
cv.destroyAllWindows()