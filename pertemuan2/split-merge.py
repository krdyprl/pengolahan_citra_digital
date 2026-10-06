import cv2 as cv 
from pathlib import Path 
 
# 1. Membaca citra utama dan citra logo 
imgRgb = cv.imread('gambar1.jpeg') 
 
if imgRgb is None: 
    raise FileNotFoundError("Gambar tidak ditemukan") 
 
# --------------------------------- 
# 1. Memecah channel BGR 
# --------------------------------- 
b, g, r = cv.split(imgRgb) 
 
# --------------------------------- 
# 2. Menggabungkan kembali channel 
# --------------------------------- 
imgMerge = cv.merge((b, g, r)) 
 
# --------------------------------- 
# 3. Mengosongkan channel Red 
# --------------------------------- 
imgRedZero = imgRgb.copy() 
imgRedZero[:, :, 0] = 0 
 
# --------------------------------- 
# 4. Menampilkan hasil 
# --------------------------------- 
cv.imshow("Citra Asli", imgRgb) 
cv.imshow("Channel Blue", b) 
cv.imshow("Channel Green", g) 
cv.imshow("Channel Red", r) 
cv.imshow("Hasil Merging", imgMerge) 
cv.imshow("Channel Red = 0", imgRedZero) 
 
cv.waitKey(0) 
cv.destroyAllWindows()