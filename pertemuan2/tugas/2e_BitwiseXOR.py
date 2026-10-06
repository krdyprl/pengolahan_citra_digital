import cv2 as cv
import numpy as np

img1 = cv.imread("tugas 1.jpeg")
img2 = cv.imread("tugas 2.jpeg")

# Bitwise XOR
hasil_12 = cv.bitwise_xor(img1, img2)
hasil_21 = cv.bitwise_xor(img2, img1)

sama = np.array_equal(hasil_12, hasil_21)
print(
    "Apakah hasil Bitwise XOR Image 1 dan Image 2 sama dengan Image 2 dan"
    " Image 1?"
)
print(sama)

cv.imshow("Image 1 XOR Image 2", hasil_12)
cv.imshow("Image 2 XOR Image 1", hasil_21)

cv.waitKey(0)
cv.destroyAllWindows()
