import cv2 as cv
import numpy as np

img1 = cv.imread("tugas 1.jpeg")
img2 = cv.imread("tugas 2.jpeg")



# Image Addition
hasil_12 = cv.add(img1, img2)
hasil_21 = cv.add(img2, img1)

# Membandingkan kedua hasil
sama = np.array_equal(hasil_12, hasil_21)
print("Apakah hasil Image 1 + Image 2 sama dengan Image 2 + Image 1?")
print(sama)

cv.imshow("Image 1", img1)
cv.imshow("Image 2", img2)
cv.imshow("Image 1 + Image 2", hasil_12)
cv.imshow("Image 2 + Image 1", hasil_21)

cv.waitKey(0)
cv.destroyAllWindows()
