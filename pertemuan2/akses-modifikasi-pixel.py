import numpy as np
import cv2 as cv

# 1. Membaca gambar dalam mode BGR dan Grayscale
imgRgb = cv.imread('gambar1.jpeg', cv.IMREAD_COLOR)
imgGrayscale = cv.imread('gambar1.jpeg', cv.IMREAD_GRAYSCALE)

# 2. Mengakses dan memodifikasi nilai piksel
pxRgb = imgRgb[10, 10]
print(pxRgb)
blue = imgRgb[10, 10, 0] # Indeks 0 adalah kanal Blue
print(blue)
imgRgb[10, 10] = [10, 10, 10]
print(imgRgb[10, 10])
pxGrayscale = imgGrayscale[10, 10]
print(pxGrayscale)
imgGrayscale[10, 10] = 10
print(imgGrayscale[10, 10])

# 3. Mencetak nilai ke terminal

# 4. Operasi Pemisahan dan Penggabungan Kanal (Format BGR)
b, g, r = cv.split(imgRgb)
imgRgbMerge = cv.merge((b, g, r))

b_slice = imgRgb[:, :, 0] # Indeks 0 = Blue
imgRgb[:, :, 2] = 0       # Indeks 2 = Red (Mengosongkan kanal Red), Indeks 1 = Green (Membiarkan kanal Green tetap ada), Indeks 0 = Blue (Membiarkan kanal Blue tetap ada)

# 5. Menampilkan hasil visual
window_blue = 'Image imgRgb Layer Blue'
window_no_red = 'Image imgRgb dengan Layer Red = 0'

cv.namedWindow(window_blue, cv.WINDOW_NORMAL)
cv.imshow(window_blue, b)

cv.namedWindow(window_no_red, cv.WINDOW_NORMAL)
cv.imshow(window_no_red, imgRgb)

cv.waitKey(0)
cv.destroyAllWindows()