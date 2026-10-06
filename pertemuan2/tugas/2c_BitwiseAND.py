import cv2 as cv
import numpy as np

img1 = cv.imread("tugas 1.jpeg")
img2 = cv.imread("tugas 2.jpeg")

# Bitwise AND
hasil_12 = cv.bitwise_and(img1, img2)
hasil_21 = cv.bitwise_and(img2, img1)

# Membandingkan kedua hasil
sama = np.array_equal(hasil_12, hasil_21)
print(
    "Apakah hasil Bitwise AND Image 1 dan Image 2 sama dengan Image 2 dan"
    " Image 1?"
)
print(sama)

cv.imshow("Image 1", img1)
cv.imshow("Image 2", img2)
cv.imshow("Image 1 AND Image 2", hasil_12)
cv.imshow("Image 2 AND Image 1", hasil_21)

cv.waitKey(0)
cv.destroyAllWindows()
