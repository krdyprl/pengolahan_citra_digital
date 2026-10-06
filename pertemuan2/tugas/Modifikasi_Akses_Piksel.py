import cv2 as cv
import numpy as np
import random

# Membaca gambar input
imgAsli = cv.imread("tugas.jpg")
h0, w0 = imgAsli.shape[:2]

# Deteksi orientasi gambar (landscape / portrait) dan sesuaikan ukurannya
lanskap = w0 >= h0
panjang_sisi = 800  # Sisi terpanjang setelah di-resize

if lanskap:
  w = panjang_sisi
  h = int(round(h0 * panjang_sisi / w0))
else:
  h = panjang_sisi
  w = int(round(w0 * panjang_sisi / h0))

imgRgb = cv.resize(imgAsli, (w, h), interpolation=cv.INTER_AREA)
imgAsli = imgRgb.copy()

# Rentang skala acak per area: gelap sekali, normal, atau terang sekali
skala_gelap = (0.05, 0.20)   # Mendekati hitam (piksel mendekati 0)
skala_normal = (0.80, 1.50)  # Sedikit berubah
skala_terang = (2.50, 4.00)  # Saturasi penuh (piksel menuju 255)

# Membentuk grid area target secara otomatis dari ukuran & orientasi gambar
if lanskap:
  cols, rows = 5, 4  # Gambar lanskap: lebih banyak kolom
else:
  cols, rows = 4, 5  # Gambar portrait: lebih banyak baris

ukuran = min(40, w // cols, h // rows)  # Ukuran area (ukuran x ukuran piksel)

koordinat = []
for r in range(rows):
  for c in range(cols):
    x0 = min(max(int((c + 0.5) * w / cols - ukuran / 2), 0), w - ukuran)
    y0 = min(max(int((r + 0.5) * h / rows - ukuran / 2), 0), h - ukuran)
    koordinat.append((x0, y0))

# Menentukan skala acak untuk setiap area (ada yang gelap sekali / terang sekali)
skala_acak = []
for _ in koordinat:
  jenis = random.choice(["gelap", "normal", "terang"])
  if jenis == "gelap":
    skala = random.uniform(*skala_gelap)
  elif jenis == "terang":
    skala = random.uniform(*skala_terang)
  else:
    skala = random.uniform(*skala_normal)
  skala_acak.append((jenis, skala))

# Transformasi intensitas piksel pada Region of Interest (ROI)
print(f"Gambar asli  : {w0} x {h0} piksel ({'lanskap' if lanskap else 'portrait'})")
print(f"Gambar proses: {w} x {h} piksel")
print(f"Ukuran area  : {ukuran} x {ukuran} piksel")
print(f"Jumlah area  : {len(koordinat)} ({cols} kolom x {rows} baris)")
print(f"Skala acak   : gelap {skala_gelap}, normal {skala_normal}, terang {skala_terang}")
print("Format nilai : [B, G, R] (urutan kanal OpenCV)")


# Perulangan rekursif per piksel dalam satu baris (kolom x naik)
def proses_piksel(x, y, x_akhir, skala):
  if x >= x_akhir:
    return

  sebelum = imgRgb[y, x].tolist()
  sesudah = []

  for k in range(3):
    # Perkalian skala dengan saturasi 8-bit: hasil dibatasi pada rentang 100 - 255
    P_input = int(imgRgb[y, x, k])
    P_output = max(100, min(255, round(P_input * skala)))
    imgRgb[y, x, k] = P_output
    sesudah.append(P_output)

  print(f"({x}, {y}) -> sebelum {sebelum} | sesudah {sesudah}")

  proses_piksel(x + 1, y, x_akhir, skala)


# Perulangan rekursif per baris (baris y naik) untuk satu area
def proses_baris(y, x0, y_akhir, skala):
  if y >= y_akhir:
    return

  proses_piksel(x0, y, x0 + ukuran, skala)
  proses_baris(y + 1, x0, y_akhir, skala)


# Memproses setiap area target secara rekursif
for (x0, y0), (jenis, skala) in zip(koordinat, skala_acak):
  print("\n========================")
  print(f"Area target: ({x0}, {y0})")
  print(f"Koordinat  : x = {x0}-{x0 + ukuran - 1}, y = {y0}-{y0 + ukuran - 1}")
  print(f"Skala      : {skala:.3f} ({jenis})")
  proses_baris(y0, x0, y0 + ukuran, skala)

# Menandai area ROI pada salinan khusus tampilan (data asli tidak diubah)
imgAsliTampil = imgAsli.copy()
imgHasilTampil = imgRgb.copy()

for x0, y0 in koordinat:
  pt1 = (x0, y0)
  pt2 = (x0 + ukuran - 1, y0 + ukuran - 1)
  cv.rectangle(imgAsliTampil, pt1, pt2, (0, 0, 255), 1)
  cv.rectangle(imgHasilTampil, pt1, pt2, (0, 0, 255), 1)

# Menampilkan hasil
cv.namedWindow("Gambar Asli ", cv.WINDOW_NORMAL)
cv.namedWindow("Hasil Modifikasi", cv.WINDOW_NORMAL)

cv.resizeWindow("Gambar Asli ", w, h)
cv.resizeWindow("Hasil Modifikasi", w, h)

cv.imshow("Gambar Asli ", imgAsliTampil)
cv.imshow("Hasil Modifikasi", imgHasilTampil)

cv.waitKey(0)
cv.destroyAllWindows()
