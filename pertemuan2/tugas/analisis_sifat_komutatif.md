# Analisis Sifat Komutatif pada Operasi Citra Digital

Dokumen ini menganalisis sifat **komutatif** pada lima operasi citra dasar: penjumlahan (*addition*), pengurangan (*subtraction*), dan tiga operasi bitwise (*AND*, *OR*, *XOR*). Analisis mencakup landasan matematis, pengujian empiris terhadap citra nyata, serta contoh numerik.

---

## 1. Definisi Sifat Komutatif

Suatu operasi biner $*$ dikatakan **komutatif** jika dan hanya jika urutan operand tidak mempengaruhi hasil:

$$A * B = B * A \quad \forall A, B$$

Pada citra digital, $A$ dan $B$ adalah matriks berukuran $H \times W \times C$ (tinggi, lebar, kanal warna). Operasi citra bekerja secara **per-elemen** (*element-wise*): setiap piksel pada koordinat $(x, y)$ dan kanal $k$ dihitung secara independen.

$$\text{Output}(x, y, k) = f\big(A(x, y, k),\ B(x, y, k)\big)$$

Karena itu, sifat komutatif operasi citra ditentukan oleh sifat komutatif fungsi skalar $f$ pada setiap elemen.

---

## 2. Metodologi Pengujian

| Aspek | Keterangan |
| :--- | :--- |
| **Skrip uji** | `2a_ImageAddition.py`, `2b_ImageSubtraction.py`, `2c_BitwiseAND.py`, `2d_BitwiseOR.py`, `2e_BitwiseXOR.py` |
| **Citra input** | `tugas 1.jpeg` dan `tugas 2.jpeg` |
| **Ukuran citra** | $1280 \times 960$ piksel (kedua citra identik ukurannya, tanpa *resize*) |
| **Metode verifikasi** | Perbandingan matriks hasil dengan `np.array_equal(hasil_12, hasil_21)` |
| **Tipe data** | `uint8` dengan rentang nilai $[0, 255]$ |

Setiap skrip menghitung hasil operasi pada dua urutan berbeda ($A \to B$ dan $B \to A$), lalu membandingkan keduanya secara bit-per-bit.

---

## 3. Tabel Ringkasan Hasil

| Operasi | Fungsi OpenCV | `A op B == B op A` | Sifat | Penyebab |
| :--- | :--- | :---: | :--- | :--- |
| Addition | `cv.add` | `True` | **Komutatif** | Penjumlahan bersifat komutatif; saturasi $\min(255, \cdot)$ simetris |
| Subtraction | `cv.subtract` | `False` | **Tidak Komutatif** | Pengurangan tidak komutatif; saturasi $\max(0, \cdot)$ asimetris |
| Bitwise AND | `cv.bitwise_and` | `True` | **Komutatif** | Operasi `AND` per bit komutatif |
| Bitwise OR | `cv.bitwise_or` | `True` | **Komutatif** | Operasi `OR` per bit komutatif |
| Bitwise XOR | `cv.bitwise_xor` | `True` | **Komutatif** | Operasi `XOR` per bit komutatif |

**Kesimpulan:** Dari kelima operasi, hanya **pengurangan (*subtraction*)** yang **tidak komutatif**. Keempat operasi lainnya bersifat komutatif.

---

## 4. Analisis per Operasi

### 4.1. Addition (`cv.add`)

**Rumus:**

$$\text{Output}(A, B) = \min(255,\ A + B)$$

**Bukti:**

$$\text{Output}(A, B) = \min(255,\ A + B) = \min(255,\ B + A) = \text{Output}(B, A)$$

Karena penjumlahan bilangan bulat bersifat komutatif ($A + B = B + A$) dan fungsi saturasi $\min(255, \cdot)$ menerapkan batas yang sama tanpa memperhatikan urutan operand, maka operasi ini **komutatif**.

**Contoh Numerik:** Misal $A = 150$, $B = 200$.

1. $A + B = 150 + 200 = 350 \Rightarrow \min(255, 350) = \mathbf{255}$
2. $B + A = 200 + 150 = 350 \Rightarrow \min(255, 350) = \mathbf{255}$

Hasil: $A + B = B + A = 255$. **Komutatif.**

---

### 4.2. Subtraction (`cv.subtract`)

**Rumus:**

$$\text{Output}(A, B) = \max(0,\ A - B)$$

**Bukti:**

$$\text{Output}(A, B) = \max(0,\ A - B) \neq \max(0,\ B - A) = \text{Output}(B, A) \quad \text{untuk } A \neq B$$

Pengurangan tidak komutatif secara aljabar: $A - B = -(B - A)$. Selain itu, *underflow* pada `uint8` dipotong ke nilai minimum $0$, sehingga hasil negatif kehilangan tandanya dan tidak dapat dipulihkan. Kedua faktor ini membuat operasi **tidak komutatif**.

**Contoh Numerik:** Misal $A = 150$, $B = 200$.

1. $A - B = 150 - 200 = -50 \Rightarrow \max(0, -50) = \mathbf{0}$ (hitam)
2. $B - A = 200 - 150 = 50 \Rightarrow \max(0, 50) = \mathbf{50}$ (abu-abu gelap)

Hasil: $A - B = 0 \neq 50 = B - A$. **Tidak komutatif.**

---

### 4.3. Bitwise AND (`cv.bitwise_and`)

**Rumus (per bit):**

$$\text{Output}(A, B) = A \,\&\, B$$

**Bukti:** Operasi `AND` pada bit tunggal bersifat komutatif:

| $A$ | $B$ | $A \,\&\, B$ | $B \,\&\, A$ |
| :-: | :-: | :-: | :-: |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |

Karena berlaku untuk setiap bit, maka berlaku pula untuk keseluruhan bilangan 8-bit, sehingga operasi ini **komutatif**.

**Contoh Numerik:** Misal $A = 150$ (`10010110`), $B = 200$ (`11001000`).

1. $A \,\&\, B = 10010110 \,\&\, 11001000 = 10000000 = \mathbf{128}$
2. $B \,\&\, A = 11001000 \,\&\, 10010110 = 10000000 = \mathbf{128}$

Hasil: $A \,\&\, B = B \,\&\, A = 128$. **Komutatif.**

---

### 4.4. Bitwise OR (`cv.bitwise_or`)

**Rumus (per bit):**

$$\text{Output}(A, B) = A \,|\, B$$

**Bukti:** Operasi `OR` pada bit tunggal bersifat komutatif:

| $A$ | $B$ | $A \,|\, B$ | $B \,|\, A$ |
| :-: | :-: | :-: | :-: |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 |

Karena berlaku untuk setiap bit, maka operasi ini **komutatif**.

**Contoh Numerik:** Misal $A = 150$ (`10010110`), $B = 200$ (`11001000`).

1. $A \,|\, B = 10010110 \,|\, 11001000 = 11011110 = \mathbf{222}$
2. $B \,|\, A = 11001000 \,|\, 10010110 = 11011110 = \mathbf{222}$

Hasil: $A \,|\, B = B \,|\, A = 222$. **Komutatif.**

---

### 4.5. Bitwise XOR (`cv.bitwise_xor`)

**Rumus (per bit):**

$$\text{Output}(A, B) = A \oplus B$$

**Bukti:** Operasi `XOR` pada bit tunggal bersifat komutatif:

| $A$ | $B$ | $A \oplus B$ | $B \oplus A$ |
| :-: | :-: | :-: | :-: |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |

Karena berlaku untuk setiap bit, maka operasi ini **komutatif**.

**Contoh Numerik:** Misal $A = 150$ (`10010110`), $B = 200$ (`11001000`).

1. $A \oplus B = 10010110 \oplus 11001000 = 01011110 = \mathbf{94}$
2. $B \oplus A = 11001000 \oplus 10010110 = 01011110 = \mathbf{94}$

Hasil: $A \oplus B = B \oplus A = 94$. **Komutatif.**

---

## 5. Mengapa Saturasi `uint8` Tidak Merusak Komutatifitas

Saturasi citra 8-bit menerapkan pembatasan nilai pada rentang $[0, 255]$. Untuk operasi yang komutatif, pembatasan ini **tidak mengubah urutan operand** karena fungsi batas bersifat simetris:

* **Overflow (batas atas):** $\min(255, A + B) = \min(255, B + A)$
* **Underflow (batas bawah):** $\max(0, A - B) \neq \max(0, B - A)$

Perbedaan kunci terletak pada **simetri fungsi batas terhadap operasi dasar**:

* Penjumlahan bersifat komutatif, sehingga $\min(255, \cdot)$ tetap komutatif.
* Pengurangan bersifat anti-komutatif ($A - B = -(B - A)$), dan $\max(0, \cdot)$ menghancurkan informasi tanda negatif, sehingga komutatifitas tidak dapat dipulihkan.
* Operasi bitwise (`AND`, `OR`, `XOR`) bekerja langsung pada representasi biner tanpa aritmetika carry/borrow, sehingga bebas dari masalah saturasi.

---

## 6. Implikasi Praktis

| Operasi | Implikasi Terhadap Urutan Operand |
| :--- | :--- |
| **Addition** | Urutan bebas. Umum dipakai untuk *brightness adjustment* atau *blending* dua citra. |
| **Subtraction** | **Urutan kritis.** $A - B$ menghilangkan latar belakang $B$ dari objek $A$, sedangkan $B - A$ melakukan sebaliknya. Dipakai pada *background subtraction* dan deteksi pergerakan. |
| **Bitwise AND** | Urutan bebas. Umum untuk *masking* (mengekstrak ROI dari citra menggunakan mask biner). |
| **Bitwise OR** | Urutan bebas. Umum untuk menggabungkan dua mask atau menambahkan objek ke citra. |
| **Bitwise XOR** | Urutan bebas. Umum untuk *watermarking*, deteksi perbedaan, dan operasi *toggle* bit. |

**Inti:** Hanya operasi **subtraction** yang menghasilkan citra berbeda ketika urutan operand dibalik. Hal ini konsisten dengan hasil uji empiris pada `tugas 1.jpeg` dan `tugas 2.jpeg`, di mana `np.array_equal` mengembalikan `False` hanya untuk `cv.subtract`.
