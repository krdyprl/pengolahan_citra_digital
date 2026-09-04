import cv2 as cv

#membaca citra grayscale
image_grayscale= cv.imread('hacker.jpg', cv.IMREAD_GRAYSCALE)

#threshold
_, image_binary = cv.threshold(image_grayscale, 128, 255, cv. THRESH_BINARY)

#menampilkan citra
cv. imshow('Citra Binary', image_binary)

cv.waitKey(0)
cv.destroyAllWindows ()