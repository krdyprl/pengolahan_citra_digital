# Spesifikasi Teknik & Analisis Pemrosesan Piksel Citra

Dokumen ini berisi spesifikasi teknis mengenai konstruksi modifikasi intensitas piksel pada area tertentu (*Region of Interest* / ROI) serta analisis teoritis dan praktis terkait sifat aljabar operasi pengurangan (*subtraction*) pada citra digital.

---

## 1. Spesifikasi Pemrosesan & Modifikasi Piksel

### 1.1. Region of Interest (ROI) & Pemilihan Area
* **Ukuran Area Target:** Pemrosesan dibatasi pada sub-matriks ukuran $10 \times 10$ piksel atau $20 \times 20$ piksel.
* **Koordinat Rentang:** Diambil pada posisi indeks $100$ hingga $110$ (baik pada sumbu vertikal/baris $y$ maupun horizontal/kolom $x$).

### 1.2. Metode Pengambilan & Perulangan (Iteration & Recursion)
* **Mekanisme Akses:** Mengakses setiap piksel pada area target secara simultan dan berurutan menggunakan struktur perulangan (*looping* / rekursif).
* **Kanal Warna:** Pengambilan dilakukan spesifik pada nilai intensitas tiga kanal warna:
  * **R (Red / Merah)**
  * **G (Green / Hijau)**
  * **B (Blue / Biru)**

### 1.3. Transformasi Intensitas Piksel
Setiap piksel pada koordinat $(x, y)$ dan kanal warna $k \in \{R, G, B\}$ ditransformasikan menggunakan penambahan skalar $C$:

$$P_{\text{output}}(x, y, k) = P_{\text{input}}(x, y, k) + C$$

Keterangan:
* $P_{\text{input}}$: Nilai intensitas awal piksel.
* $C$: Nilai skalar konstanta penambahan.
* $P_{\text{output}}$: Nilai intensitas akhir piksel.

### 1.4. Penanganan Overflow (Saturasi Arsitektur 8-bit)
Citra digital standar menggunakan tipe data **8-bit Unsigned Integer (`uint8`)** dengan rentang nilai $[0, 255]$. Penambahan skalar $C$ berpotensi menghasilkan nilai $> 255$ (*overflow*).

* **Metode Batasan (Clipping):** Menggunakan fungsi pemotongan nilai (*saturating arithmetic* / `np.clip`).
* **Formulasi Matematis:**

$$P_{\text{final}} = \min(255, P_{\text{input}} + C)$$

* **Logika Pemrosesan (NumPy Concept):**
  * Jika $P_{\text{input}} + C \le 255$, maka $P_{\text{final}} = P_{\text{input}} + C$.
  * Jika $P_{\text{input}} + C > 255$, maka $P_{\text{final}} = 255$ (warna mengalami saturasi penuh/putih pada kanal tersebut).

### 1.5. Format Output & Format Visualisasi
* Output diekstraksi piksel demi piksel dalam bentuk matriks atau data terstruktur (misal: koordinat $(x,y) \rightarrow [R, G, B]$).
* Menampilkan perbandingan nilai sebelum ($P_{\text{input}}$) dan sesudah ($P_{\text{output}}$) transformasi secara presisi.

---

## 2. Analisis Sifat Komutatif pada Operasi Pengurangan (*Subtraction*)

### 2.1. Definisi Komutatif
Secara umum dalam aljabar, suatu operasi biner $*$ dikatakan **komutatif** jika dan hanya jika:

$$A * B = B * A \quad \forall A, B$$

### 2.2. Evaluasi pada Operasi Pengurangan Citra
Operasi pengurangan dua citra/piksel $A$ dan $B$ didefinisikan sebagai $A - B$. Untuk menguji sifat komutatif, kita harus memeriksa apakah:

$$A - B \stackrel{?}{=} B - A$$

**Kesimpulan:** Operasi pengurangan citra **TIDAK BERLAKU KOMUTATIF** ($A - B \neq B - A$).

---

### 2.3. Penyebab Operasi Tidak Komutatif

#### A. Asimetri Operasi Aljabar Pengurangan
Secara matematis dasar pada bilangan real:
$$A - B = -(B - A)$$
Jika $A \neq B$, maka $A - B \neq B - A$. Nilai $A - B$ dan $B - A$ memiliki magnitudo yang sama tetapi berlawanan tanda.

#### B. Efek Batasan Tipe Data Citra (`uint8`) & Underflow
Dalam sistem pengolahan citra, intensitas warna tidak boleh bernilai negatif ($< 0$). Ketika nilai hasil pengurangan bernilai negatif, sistem melakukan *clipping* / *underflow handling* ke nilai minimum yaitu $0$ (hitam).

Formulasi operasi pengurangan citra dengan batasan ($[0, 255]$):

$$\text{Output}(A, B) = \max(0, A - B)$$

$$\text{Output}(B, A) = \max(0, B - A)$$

Karena $\max(0, A - B) \neq \max(0, B - A)$ ketika $A \neq B$, maka kedua hasil operasi pasti menghasilkan nilai dan penampilan visual yang berbeda.

---

### 2.4. Contoh Kasus Numerik

Misalkan terdapat dua nilai piksel pada titik koordinat yang sama dari dua citra yang berbeda:
* Nilai piksel Citra $A = 150$
* Nilai piksel Citra $B = 200$

#### Kasus 1: Pengurangan $A - B$
1. Perhitungan matematis: $150 - 200 = -50$
2. Aplikasi batas *underflow* `uint8`: $\max(0, -50) = \mathbf{0}$
3. Hasil Akhir: **0** (Piksel menjadi Hitam Sempurna)

#### Kasus 2: Pengurangan $B - A$
1. Perhitungan matematis: $200 - 150 = 50$
2. Aplikasi batas *underflow* `uint8`: $\max(0, 50) = \mathbf{50}$
3. Hasil Akhir: **50** (Piksel bernilai Abu-abu Gelap)

**Hasil:** $A - B = 0$, sedangkan $B - A = 50$. Jelas bahwa $A - B \neq B - A$.

---

### 2.5. Implikasi Visual & Aplikasi Praktis

| Parameter | Operasi $A - B$ | Operasi $B - A$ |
| :--- | :--- | :--- |
| **Area yang Menonjol** | Bagian di mana Citra $A$ lebih terang daripada Citra $B$. | Bagian di mana Citra $B$ lebih terang daripada Citra $A$. |
| **Area bernilai 0 (Hitam)** | Semua area di mana $A \le B$. | Semua area di mana $B \le A$. |
| **Pengunaan dalam Pengolahan Citra** | Menghilangkan latar belakang $B$ dari objek $A$. | Menghilangkan latar belakang $A$ dari objek $B$. |


