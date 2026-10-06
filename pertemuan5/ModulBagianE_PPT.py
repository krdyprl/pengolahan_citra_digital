"""
Cara Pakai Kodenya 
    python KerjaKelompok.py image.jpeg
    python KerjaKelompok.py image.jpeg --low 1 --high 99 --out hasil
    python KerjaKelompok.py image.jpeg --raw      # histogram tanpa penghalusan
"""
import argparse
import os
import re
import sys
from dataclasses import dataclass

import cv2
import matplotlib
import numpy as np

# Backend non-GUI bila tidak ada display (server/CI)
if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

CHANNELS = ("Red", "Green", "Blue")
COLORS = ("#d62728", "#2ca02c", "#1f77b4")
METHOD_COLORS = ("#444444", "#ff7f0e", "#9467bd", "#17becf", "#e377c2")
N_COLS = 3


@dataclass
class Result:
    name: str
    image: np.ndarray

    @property
    def gray(self):
        return cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

    @property
    def std(self):
        return float(self.gray.std())

    @property
    def entropy(self):
        p = np.bincount(self.gray.ravel(), minlength=256) / self.gray.size
        p = p[p > 0]
        return float(-(p * np.log2(p)).sum())


# ------------------------------------------------------------------ I/O
def load_rgb(path):
    bgr = cv2.imread(path, cv2.IMREAD_COLOR)  # selalu 3 channel (alpha dibuang)
    if bgr is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan atau gagal dibaca: {path}")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def save_rgb(path, rgb):
    cv2.imwrite(path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))


def slugify(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")


# ------------------------------------------------------------ pemrosesan
def stretch_channel(ch, low_pct=0.0, high_pct=100.0):
    """g = (f - lo) / (hi - lo) * 255 dengan pembulatan; lo/hi dari persentil."""
    lo, hi = np.percentile(ch, [low_pct, high_pct])
    if hi <= lo:
        return ch.copy()
    out = (ch.astype(np.float32) - lo) / (hi - lo) * 255.0
    return np.rint(np.clip(out, 0, 255)).astype(np.uint8)


def per_channel(img, fn):
    """Terapkan fn pada tiap channel R, G, B lalu gabungkan."""
    return cv2.merge([fn(np.ascontiguousarray(c)) for c in cv2.split(img)])


def on_luminance(img, fn):
    """Terapkan fn hanya pada kanal Y (YCrCb) agar warna tidak bergeser."""
    ycc = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    ycc[..., 0] = fn(np.ascontiguousarray(ycc[..., 0]))
    return cv2.cvtColor(ycc, cv2.COLOR_YCrCb2RGB)


def run_methods(img, low, high):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return [
        Result("Asli", img),
        Result(f"Stretching RGB (p{low:g}-p{high:g})",
               per_channel(img, lambda c: stretch_channel(c, low, high))),
        Result("Equalization RGB", per_channel(img, cv2.equalizeHist)),
        Result("Equalization Y (YCrCb)", on_luminance(img, cv2.equalizeHist)),
        Result("CLAHE Y (clip 2, 8x8)", on_luminance(img, clahe.apply)),
    ]


# --------------------------------------------------------------- laporan
def print_report(results):
    w = max(len(r.name) for r in results) + 2
    head = (f"{'Metode':<{w}}| {'R min-max':^10}| {'G min-max':^10}| "
            f"{'B min-max':^10}| {'Std':>6} | {'Entropi':>7}")
    print("INFORMASI CITRA RGB")
    print("=" * len(head), head, "-" * len(head), sep="\n")
    for r in results:
        mm = [f"{r.image[..., i].min()}-{r.image[..., i].max()}" for i in range(3)]
        print(f"{r.name:<{w}}| {mm[0]:^10}| {mm[1]:^10}| {mm[2]:^10}| "
              f"{r.std:6.2f} | {r.entropy:7.3f}")
    print("=" * len(head))
    print("Std = simpangan baku luminansi (kontras); entropi dalam bit (maks 8).\n")


# ------------------------------------------------------------ visualisasi
def smooth(hist, k):
    """Moving average ukuran ganjil k (k<=1 = tanpa penghalusan)."""
    if k <= 1:
        return hist.astype(float)
    pad = k // 2
    padded = np.pad(hist.astype(float), pad, mode="edge")
    return np.convolve(padded, np.ones(k) / k, mode="valid")


def make_grid(n_panels, title, panel_size=(5.2, 4.2)):
    rows = int(np.ceil(n_panels / N_COLS))
    fig, axes = plt.subplots(rows, N_COLS, layout="constrained",
                             figsize=(panel_size[0] * N_COLS, panel_size[1] * rows))
    fig.suptitle(title, fontsize=15, fontweight="bold")
    axes = np.atleast_1d(axes).ravel()
    return fig, axes


def finish(fig, filename, show):
    fig.savefig(filename, dpi=140)
    print(f"Disimpan: {filename}")
    if show and matplotlib.get_backend().lower() != "agg":
        plt.show()
    plt.close(fig)


def plot_images(results, notes, filename, show):
    fig, axes = make_grid(len(results) + 1, "Perbandingan Citra")
    for ax, r in zip(axes, results):
        ax.imshow(r.image)
        ax.set_title(f"{r.name}\nStd {r.std:.1f}  |  Entropi {r.entropy:.2f}", fontsize=10)
        ax.axis("off")
    for ax in axes[len(results):]:   # panel sisa: catatan
        ax.axis("off")
        ax.text(0, 1, notes, va="top", ha="left", fontsize=9.5, linespacing=1.6,
                transform=ax.transAxes)
    finish(fig, filename, show)


def plot_histograms(results, k_smooth, filename, show):
    fig, axes = make_grid(len(results) + 1, "Histogram RGB per Metode")
    hist_axes, cdf_ax = axes[:len(results)], axes[len(results)]
    x = np.arange(256)

    ymax = 0
    for ax, r in zip(hist_axes, results):
        for i, (name, col) in enumerate(zip(CHANNELS, COLORS)):
            h = smooth(np.bincount(r.image[..., i].ravel(), minlength=256), k_smooth)
            ymax = max(ymax, h.max())
            ax.plot(x, h, color=col, lw=1.3, label=name)
            ax.fill_between(x, h, color=col, alpha=0.10)
        ax.set_title(r.name, fontsize=10, fontweight="bold")
        ax.set_xlim(0, 255)
        ax.set_xticks([0, 64, 128, 192, 255])
        ax.grid(alpha=0.25)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:g}k"))
    for ax in hist_axes:
        ax.set_ylim(0, ymax * 1.05)
        ax.sharey(hist_axes[0])
    hist_axes[0].legend(fontsize=8, loc="upper left", frameon=False)
    for ax in hist_axes:
        ax.set_xlabel("Intensitas piksel")
        ax.set_ylabel("Frekuensi")
        ax.label_outer()

    # Panel CDF luminansi: equalization ideal mendekati garis diagonal
    cdf_ax.plot([0, 255], [0, 1], "k--", lw=1, alpha=0.5, label="Ideal (merata)")
    for r, col in zip(results, METHOD_COLORS):
        c = np.cumsum(np.bincount(r.gray.ravel(), minlength=256)) / r.gray.size
        cdf_ax.plot(x, c, color=col, lw=1.6, label=r.name)
    cdf_ax.set_title("CDF luminansi (semua metode)", fontsize=10, fontweight="bold")
    cdf_ax.set_xlim(0, 255)
    cdf_ax.set_ylim(0, 1.02)
    cdf_ax.set_xticks([0, 64, 128, 192, 255])
    cdf_ax.set_xlabel("Intensitas piksel")
    cdf_ax.set_ylabel("Probabilitas kumulatif")
    cdf_ax.grid(alpha=0.25)
    cdf_ax.legend(fontsize=7.5, loc="lower right", frameon=False)

    for ax in axes[len(results) + 1:]:
        ax.axis("off")
    if k_smooth > 1:
        fig.text(0.995, 0.005, f"histogram dihaluskan (moving average {k_smooth})",
                 ha="right", va="bottom", fontsize=8, color="gray")
    finish(fig, filename, show)


NOTES = (
    "Catatan metode\n"
    "-------------------------\n"
    "Stretching RGB   : meregangkan tiap channel\n"
    "                   ke 0-255.\n"
    "Equalization RGB : meratakan histogram tiap\n"
    "                   channel (warna bisa bergeser).\n"
    "Equalization Y   : hanya kanal luminansi,\n"
    "                   warna lebih terjaga.\n"
    "CLAHE Y          : equalization lokal dengan\n"
    "                   batas kontras (noise terjaga).\n\n"
    "Std tinggi = kontras tinggi.\n"
    "Entropi tinggi = sebaran intensitas lebih kaya."
)


# ------------------------------------------------------------------ main
def parse_args():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?", default="gambar.jpeg", help="path citra masukan")
    ap.add_argument("--low", type=float, default=0.0, help="persentil bawah stretching")
    ap.add_argument("--high", type=float, default=100.0, help="persentil atas stretching")
    ap.add_argument("--smooth", type=int, default=5, help="lebar penghalusan histogram (ganjil)")
    ap.add_argument("--raw", action="store_true", help="histogram mentah, tanpa penghalusan")
    ap.add_argument("--out", default="hasil", help="folder keluaran")
    ap.add_argument("--no-show", action="store_true", help="jangan tampilkan jendela plot")
    args = ap.parse_args()
    if not 0 <= args.low < args.high <= 100:
        ap.error("--low/--high harus memenuhi 0 <= low < high <= 100")
    if args.raw:
        args.smooth = 1
    elif args.smooth % 2 == 0:
        args.smooth += 1
    return args


def main():
    args = parse_args()
    try:
        img = load_rgb(args.image)
    except FileNotFoundError as e:
        sys.exit(str(e))

    full_range = all(img[..., i].min() == 0 and img[..., i].max() == 255 for i in range(3))
    if full_range and args.low == 0 and args.high == 100:
        print("Catatan: citra sudah full-range (0-255), min-max stretching tidak "
              "mengubah apa pun. Coba --low 1 --high 99.\n")

    results = run_methods(img, args.low, args.high)
    print_report(results)

    os.makedirs(args.out, exist_ok=True)
    for i, r in enumerate(results[1:], start=1):
        save_rgb(os.path.join(args.out, f"{i}_{slugify(r.name)}.png"), r.image)

    show = not args.no_show
    plot_images(results, NOTES, os.path.join(args.out, "perbandingan_citra.png"), show)
    plot_histograms(results, args.smooth, os.path.join(args.out, "perbandingan_histogram.png"), show)


if __name__ == "__main__":
    main()