# Log Perbaikan Program — Pertemuan 5 (Histogram Citra)

Tanggal: 6 Oktober 2026
Folder: `pertemuan5`
Acuan: Modul, Makalah, dan PPT "Histogram Citra" Kelompok 5

## Ringkasan Masalah

1. **8 dari 9 file `.py` kosong (0 byte)** sehingga tidak ada kode yang bisa dijalankan
   maupun diperiksa. Hanya `HistogramSederhana.py` yang berisi kode.
2. **Path gambar tidak sesuai permintaan.** Kode contoh pada modul/makalah memakai nama
   file lain (`IMG_9549.jpg`, `stiker wa.jpg`, `gambar.png`, `home.jpg`), bukan `image.jpeg`.
3. **Kesalahan sintaks pada kode contoh di modul** (kurung tutup hilang).
4. **Potensi error pembagian nol** pada operasi contrast stretching bila nilai min = max.

## Detail Perbaikan per File

| No | File | Tindakan | Keterangan |
|----|------|----------|------------|
| 1 | `HistogramSederhana.py` | Diperbarui | Path sudah `image.jpeg`. Ditambahkan `.flatten()` pada hasil `cv2.calcHist` dan blok `print` intensitas kelipatan 20 (sesuai makalah). |
| 2 | `PlottingHistogramCitraGrayscale.py` | Dibuat | Diisi ulang dari Modul bagian C.1. Path diganti ke `image.jpeg`. |
| 3 | `HistogramWarnaRGB.py` | Dibuat | Diisi ulang dari Modul bagian C.2 (plot gabungan BGR). Path diganti ke `image.jpeg`. |
| 4 | `HistogramWarnaIndividu.py` | Dibuat | Diisi ulang dari Makalah 2.7 (plot per kanal terpisah). Path diganti ke `image.jpeg`. |
| 5 | `ContrastStretching.py` | Dibuat | Diisi ulang dari Modul bagian C.3 (rumus min–max). Path diganti ke `image.jpeg`. |
| 6 | `ContrastStretchingCDF.py` | Dibuat | Diisi ulang dari Makalah 2.5 (normalisasi CDF). Path diganti ke `image.jpeg`. |
| 7 | `HistogramEqualization.py` | Dibuat | Diisi ulang dari Modul bagian C.4. Path diganti ke `image.jpeg`. |
| 8 | `ModulBagianE_PPT.py` | Dibuat | Jawaban Soal bagian E (grid 2x2: grayscale, histogram, equalization, histogram). Path `image.jpeg`. |
| 9 | `ModulBagianD.py` | Dibuat | Jawaban Latihan Soal bagian D (4 panel). Path `image.jpeg`. |

## Daftar Kesalahan yang Ditemukan & Cara Perbaikan

### 1. File kosong (0 byte)
- **Masalah:** 8 file tidak memiliki isi sehingga `python namafile.py` tidak menghasilkan apa pun.
- **Perbaikan:** Mengisi ulang setiap file berdasarkan kode contoh pada Modul dan Makalah,
  disesuaikan dengan nama file masing-masing.

### 2. Path gambar tidak konsisten
- **Masalah:** Kode contoh merujuk ke `IMG_9549.jpg`, `stiker wa.jpg`, `gambar.png`, dan
  `home.jpg` yang tidak ada di folder, sehingga `cv2.imread()` mengembalikan `None` dan
  program akan error (`NoneType`) saat `cv2.cvtColor`/`calcHist`.
- **Perbaikan:** Semua path diseragamkan menjadi `"image.jpeg"` sesuai permintaan.

### 3. Kesalahan sintaks pada contoh modul
- **Masalah:** Potongan `hist, bins = np.histogram(img.ravel(), 256, [0, 256]` kehilangan
  tanda kurung tutup `)`.
- **Perbaikan:** Ditulis lengkap `np.histogram(img.ravel(), 256, [0, 256])`.

### 4. Placeholder tidak terdefinisi pada contoh makalah
- **Masalah:** Contoh `np.histogram(img.ravel(), histSize, (ranges))` dan
  `cv.imread('home.jpg', flags)` memakai variabel `histSize`, `ranges`, dan `flags` yang
  tidak pernah didefinisikan.
- **Perbaikan:** Diganti dengan nilai konkret `256` dan `[0, 256]`, serta flag
  `cv.IMREAD_GRAYSCALE` (0) / `cv.IMREAD_COLOR` (1).

### 5. Potensi pembagian nol (contrast stretching)
- **Masalah:** `(gray - fmin) / (fmax - fmin)` akan error bila `fmax == fmin` (citra seragam).
- **Perbaikan:** Ditambahkan pengecekan `if fmax == fmin` pada `ContrastStretching.py` dan
  `ModulBagianD.py`.

## Verifikasi

Semua 9 program dijalankan dengan `MPLBACKEND=Agg`:

```
[OK] ContrastStretching.py
[OK] ContrastStretchingCDF.py
[OK] HistogramEqualization.py
[OK] HistogramSederhana.py
[OK] HistogramWarnaIndividu.py
[OK] HistogramWarnaRGB.py
[OK] ModulBagianD.py
[OK] ModulBagianE_PPT.py
[OK] PlottingHistogramCitraGrayscale.py
```

Output `HistogramSederhana.py` (menunjukkan `image.jpeg` berhasil dibaca):

```
Intensitas |     OpenCV |      NumPy
--------------------------------------
         0 |         27 |         27
        20 |       2875 |       2875
        40 |       3686 |       3686
        60 |       3800 |       3800
        80 |       2789 |       2789
       100 |       3929 |       3929
       120 |       2953 |       2953
       140 |       4379 |       4379
       160 |       8390 |       8390
       180 |       3966 |       3966
       200 |       5753 |       5753
       220 |       1074 |       1074
       240 |        138 |        138
```

## Catatan

- `image.jpeg` pada folder ini identik dengan yang ada di `pertemuan4` (91.626 byte).
- Hasil `HistogramSederhana.py` menunjukkan sebaran piksel 0–255 yang cukup merata,
  artinya `image.jpeg` **bukan** citra low contrast seperti citra contoh di modul
  (`IMG_9549.jpg`). Efek contrast stretching/equalization tetap berjalan, namun
  perubahannya tidak seekstrem contoh pada modul.
