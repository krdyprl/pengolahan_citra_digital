import cv2 as cv

# PARAMETER ROI (UBAH DI SINI)
x = 255  # posisi kiri (horizontal)
y = 255  # posisi atas (vertikal)
w = 160  # lebar ROI
h = 180  # tinggi ROI

# Load Image
img = cv.imread("gambar1.jpeg")
if img is None:
    raise FileNotFoundError("Gambar tidak ditemukan")

output = img.copy()

# Pastikan ROI tidak keluar dari batas gambar
H, W = img.shape[:2]
x = max(0, min(x, W - 1))
y = max(0, min(y, H - 1))
w = min(w, W - x)
h = min(h, H - y)

# Ambil ROI dari gambar asli (agar bersih dari garis hijau)
roi = img[y:y + h, x:x + w]

# Highlight ROI di gambar output
cv.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)

# Mengatur posisi teks agar tidak terpotong di batas atas gambar
text_y = y - 10 if y - 10 > 15 else y + 25
cv.putText(output, "ROI", (x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Menempelkan thumbnail ROI di pojok kiri atas GUI
rh, rw = roi.shape[:2]
output[10:10 + rh, 10:10 + rw] = roi

# Tampilkan GUI
cv.imshow("ROI Manual (Diatur di Kode)", output)
cv.waitKey(0)
cv.destroyAllWindows()