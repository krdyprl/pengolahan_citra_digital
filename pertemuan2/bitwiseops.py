import cv2 as cv
import numpy as np

# 1. Membaca dua gambar
img1 = cv.imread ('gambar1.jpeg')
img2= cv.imread ('gambar2.jpg')

# 2. Menyamakan ukuran img2 dengan img1
h, w, c = img1.shape
img2 = cv.resize(img2, (w, h))

# 3. Eksekusi 4 Operasi Bitwise
# a. Bitwise AND

res_and = cv.bitwise_and(img1, img2)

# b. Bitwise OR

res_or = cv.bitwise_or(img1, img2)

# c. Bitwise XOR

res_xor = cv.bitwise_xor(img1, img2)

# d. Bitwise NOT (Inversi pada img1)
res_not = cv.bitwise_not (img1)

# 4. Menampilkan hasil

cv.imshow ('Gambar 1 Asli', img1)
cv.imshow ('Gambar 2 Asli', img2)
cv. imshow ('Bitwise AND', res_and)

cv. imshow('Bitwise OR', res_or)

cv. imshow ('Bitwise XOR', res_xor)
cv. imshow ('Bitwise NOT (Gambar 1)', res_not)
cv.waitKey(0) 
cv.destroyAllWindows() 