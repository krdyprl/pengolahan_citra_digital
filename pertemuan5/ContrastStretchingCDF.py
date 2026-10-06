import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('image.jpeg', 0)
hist, bins = np.histogram(img.flatten(), 256, [0, 256])
cdf = hist.cumsum()

# Proses stretching melalui normalisasi CDF
cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype('uint8')
img2 = cdf[img]

plt.subplot(2, 1, 1)
plt.hist(img.flatten(), 256, [0, 256])
plt.title('Histogram Sebelum Stretching')

plt.subplot(2, 1, 2)
plt.hist(img2.flatten(), 256, [0, 256])
plt.title('Histogram Setelah Stretching')

plt.tight_layout()
plt.show()
