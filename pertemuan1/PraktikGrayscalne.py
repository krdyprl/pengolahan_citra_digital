import cv2 as cv

#membaca citra grayscale
image_grayscale = cv.imread('hacker.jpg', cv.IMREAD_GRAYSCALE)

#menampilkan citra
cv. imshow('Citra Grayscale', image_grayscale)

cv.waitKey(0)
cv.destroyAllWindows ()