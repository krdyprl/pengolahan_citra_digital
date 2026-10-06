import os
import numpy as np
import matplotlib

# Pakai backend non-GUI bila tidak ada display (server/CI)
if os.environ.get("DISPLAY", "") == "" and os.name != "nt" and os.uname().sysname != "Darwin":
    matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    import cv2
except ImportError:  # OpenCV opsional
    cv2 = None

L = 256


# ---------------------------------------------------------------- perhitungan
def compute_histogram(img, levels=L):
    """Return n_k, p(r_k), CDF (hitungan), c(r_k)."""
    n = img.size
    hist = np.bincount(img.ravel(), minlength=levels)
    cdf = np.cumsum(hist)
    return hist, hist / n, cdf, cdf / n


def equalize_basic(img, cdf, levels=L):
    """s_k = round_half_up((L-1) * CDF / N), memakai aritmetika integer (eksak)."""
    n = img.size
    s = (2 * (levels - 1) * cdf + n) // (2 * n)
    return s.astype(np.uint8)[img]


def equalize_opencv_style(img, cdf, levels=L):
    """Rumus OpenCV: round((CDF - CDF_min) / (N - CDF_min) * (L-1)), versi integer."""
    n = img.size
    cdf_min = int(cdf[cdf > 0].min())
    if n == cdf_min:  # citra konstan
        return img.copy()
    num = (cdf - cdf_min).clip(min=0)
    den = n - cdf_min
    lut = (2 * (levels - 1) * num + den) // (2 * den)
    return lut.clip(0, levels - 1).astype(np.uint8)[img]


def contrast_stretch(img):
    """g = round_half_up((f - fmin) / (fmax - fmin) * 255), integer eksak."""
    fmin, fmax = int(img.min()), int(img.max())
    if fmax == fmin:
        return img.copy()
    num = 2 * 255 * (img.astype(np.int64) - fmin) + (fmax - fmin)
    return (num // (2 * (fmax - fmin))).astype(np.uint8)


# -------------------------------------------------------------------- output
def print_table(img, hist, p, cdf, c, s_basic, s_cv):
    n = img.size
    header = (f"{'r_k':>5} | {'n_k':>4} | {'p(r_k)':>8} | {'CDF':>5} | "
              f"{'c(r_k)':>8} | {'255*c':>8} | {'s_k':>5} | {'OpenCV-style':>12}")
    line = "-" * len(header)
    print("=" * len(header))
    print("TABEL ANALISIS HISTOGRAM".center(len(header)))
    print("=" * len(header))
    print(f"Dimensi = {img.shape[0]}x{img.shape[1]} | N = {n} | L = {L} | "
          f"f_min = {img.min()} | f_max = {img.max()}")
    print(line)
    print(header)
    print(line)
    for k in np.nonzero(hist)[0]:
        sk = int(s_basic[img == k][0])
        sc = int(s_cv[img == k][0])
        print(f"{k:5d} | {int(hist[k]):4d} | {p[k]:8.4f} | {int(cdf[k]):5d} | "
              f"{c[k]:8.4f} | {255 * c[k]:8.3f} | {sk:5d} | {sc:12d}")
    print(line)
    print(f"Total piksel = {int(hist.sum())} | Total probabilitas = {p.sum():.4f}")
    print("=" * len(header) + "\n")


def plot_results(img, hist, p, c, eq_basic, eq_cv, stretched, filename, show=True):
    nz = np.nonzero(hist)[0]
    fig, ax = plt.subplots(3, 3, figsize=(15, 12))
    fig.suptitle("Histogram, Ekualisasi, dan Contrast Stretching (Citra 6x6)",
                 fontsize=16, fontweight="bold")

    def stem(a, data, title, color):
        idx = np.nonzero(data)[0]
        a.stem(idx, data[idx], linefmt=color, markerfmt="o", basefmt=" ")
        a.set_xlim(-5, 260)
        a.set_title(title)
        a.set_xlabel("Intensitas")

    ax[0, 0].imshow(img, cmap="gray", vmin=0, vmax=255)
    ax[0, 0].set_title("Citra Asli")
    stem(ax[0, 1], hist, r"Histogram $n_k$", "black")
    ax[0, 1].set_ylabel("Jumlah piksel")
    stem(ax[0, 2], p, r"Probabilitas $p(r_k)$", "tab:blue")

    ax[1, 0].step(range(L), c, where="post", color="tab:red")
    ax[1, 0].set_title(r"CDF $c(r_k)$")
    ax[1, 0].set_xlabel("Intensitas")
    ax[1, 1].imshow(eq_basic, cmap="gray", vmin=0, vmax=255)
    ax[1, 1].set_title("Ekualisasi (rumus dasar)")
    stem(ax[1, 2], np.bincount(eq_basic.ravel(), minlength=L),
         "Histogram sesudah ekualisasi", "tab:green")

    ax[2, 0].imshow(eq_cv, cmap="gray", vmin=0, vmax=255)
    ax[2, 0].set_title("Ekualisasi (gaya OpenCV)")
    ax[2, 1].imshow(stretched, cmap="gray", vmin=0, vmax=255)
    ax[2, 1].set_title("Contrast stretching (citra low-contrast)")
    stem(ax[2, 2], np.bincount(stretched.ravel(), minlength=L),
         "Histogram sesudah stretching", "tab:orange")

    for a in (ax[0, 0], ax[1, 1], ax[2, 0], ax[2, 1]):
        a.axis("off")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(filename, dpi=130)
    print(f"Plot disimpan ke: {filename}")
    if show and matplotlib.get_backend().lower() != "agg":
        plt.show()
    plt.close(fig)


# ---------------------------------------------------------------------- main
def main(plot_filename="hasil_plot_6x6.png"):
    img = np.array([
        [170, 238,  85, 255, 221,   0],
        [ 68, 136,  17, 170, 119,  68],
        [221,   0, 238, 136,   0, 255],
        [119, 255,  85, 170, 136, 238],
        [238,  17, 221,  68, 119, 255],
        [ 85, 170, 119, 221,  17, 136],
    ], dtype=np.uint8)

    hist, p, cdf, c = compute_histogram(img)

    eq_basic = equalize_basic(img, cdf)
    eq_cv_style = equalize_opencv_style(img, cdf)

    print_table(img, hist, p, cdf, c, eq_basic, eq_cv_style)

    # Validasi terhadap OpenCV (jika tersedia)
    if cv2 is not None:
        eq_cv = cv2.equalizeHist(img)
        print(f"Selisih maks. implementasi gaya-OpenCV vs cv2.equalizeHist: "
              f"{np.abs(eq_cv_style.astype(int) - eq_cv.astype(int)).max()}")
    else:
        print("cv2 tidak terpasang; validasi OpenCV dilewati.")
    diff = np.abs(eq_basic.astype(int) - eq_cv_style.astype(int))
    print(f"Selisih maks. rumus dasar vs gaya OpenCV: {diff.max()} "
          f"(wajar, karena OpenCV menormalisasi dengan CDF_min = {int(cdf[cdf > 0].min())})\n")

    # Contrast stretching: citra asli sudah full-range (0..255) -> tidak berubah
    stretch_orig = contrast_stretch(img)
    if int(img.min()) == 0 and int(img.max()) == 255:
        print("Catatan: citra asli sudah full-range, stretching tidak mengubah apa pun "
              f"(identik: {np.array_equal(stretch_orig, img)}).")
    # Demo bermakna: kompres ke rentang sempit 50..180, lalu regangkan
    low = (50 + img.astype(np.int64) * 130 // 255).astype(np.uint8)
    stretch_low = contrast_stretch(low)
    print(f"Citra low-contrast: rentang {low.min()}..{low.max()} -> "
          f"setelah stretching {stretch_low.min()}..{stretch_low.max()}\n")

    print("--- CITRA ASLI ---");                    print(img)
    print("\n--- EKUALISASI (RUMUS DASAR) ---");    print(eq_basic)
    print("\n--- EKUALISASI (GAYA OPENCV) ---");    print(eq_cv_style)
    print("\n--- CITRA LOW-CONTRAST ---");          print(low)
    print("\n--- HASIL STRETCHING ---");            print(stretch_low)
    print()

    plot_results(img, hist, p, c, eq_basic, eq_cv_style, stretch_low, plot_filename)


if __name__ == "__main__":
    main()