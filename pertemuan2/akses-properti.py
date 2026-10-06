import numpy as np
import cv2 as cv

# Membaca citra format BGR dan Grayscale
imgRgb = cv.imread ('gambar1.jpeg', cv.IMREAD_COLOR)
imgGrayscale = cv.imread('gambar1.jpeg', cv.IMREAD_GRAYSCALE)

# Menampilkan properti citra BGR/RGB
print ("\nRGB Image")
print (imgRgb.shape)
print (imgRgb.size)
print (imgRgb.dtype)

# Menampilkan properti citra Grayscale
print ("\nGrayscale Image")
print (imgGrayscale.shape)
print (imgGrayscale.size)
print (imgGrayscale.dtype)