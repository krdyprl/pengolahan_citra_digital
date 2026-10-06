import cv2 as cv 
import numpy as np 
 
# 1. Membaca dua gambar 
img1 = cv.imread('nu.png') 
img2 = cv.imread('gambar2.jpg') 
 
# 2. Memastikan ukuran kedua gambar sama (syarat operasi aritmatika matriks) 
# Mengubah ukuran img2 agar sama persis dengan img1 
h, w, c = img1.shape 
img2 = cv.resize(img2, (w, h)) 
 
# 3. Operasi Image Addition dengan NumPy (Modulo Addition) 
res_numpy = img1 + img2 
 
# 4. Operasi Image Addition dengan OpenCV (Saturated Addition) 
res_opencv = cv.add(img1, img2) 
 
# 5. Menampilkan hasil 
cv.imshow('Gambar 1 Asli', img1) 
cv.imshow('Gambar 2 Asli', img2) 
cv.imshow('Hasil NumPy (img1 + img2)', res_numpy) 
cv.imshow('Hasil OpenCV (cv.add)', res_opencv) 
 
cv.waitKey(0) 
cv.destroyAllWindows() 