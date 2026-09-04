import cv2 as cv

#membaca citra berwarna
image_rgb = cv.imread('hacker.jpg', cv. IMREAD_COLOR)

#menampilkan citra
cv. imshow('Citra Berwarna', image_rgb)

cv.waitKey(0)
cv.destroyAllWindows ()