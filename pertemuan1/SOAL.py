import cv2 as cv

#Membaca citra berwarna
img_rgb = cv.imread('hacker.jpg', cv.IMREAD_COLOR)

#Membaca citra grayscale
img_gray = cv.imread('hacker.jpg', cv.IMREAD_GRAYSCALE)

#Membaca citra biner
_,img_binary = cv.threshold(img_gray, 150, 255, cv.THRESH_BINARY)

# Menyimpan hasil grayscale
cv.imwrite('Hacker_Pose_grayscale.jpg', img_gray)

#Menyimpan hasil citra biner
cv.imwrite('Hacker_Pose_binary.jpg', img_binary)

#Menampilkan citra
cv.imshow('Citra Berwarna', img_rgb)
cv.imshow('Citra Grayscale', img_gray)
cv.imshow('Citra Biner', img_binary)

cv.waitKey(0)
cv.destroyAllWindows()