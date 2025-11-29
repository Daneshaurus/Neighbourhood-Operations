# TODO: Filter Mean, Filter Median, Konvolusi, Low Pass Filter, High Pass Filter, High Boost Filter, Emboss, Deteksi Tepi

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math

def open(img, title="Result"):
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(title)  
    plt.imshow(img, cmap="gray" if img.mode == "L" else None)
    plt.title(title)
    plt.axis("off")
    plt.show()


def filter_batas(img):
    w, h = img.size
    pixels = img.load()

    # hasil tetap RGB, konsisten dengan pola program
    result = Image.new("RGB", (w, h))
    res_pixels = result.load()

    for y in range(h):
        for x in range(w):

            # kalau piksel di tepi, langsung copy
            if x == 0 or y == 0 or x == w-1 or y == h-1:
                res_pixels[x, y] = pixels[x, y]
                continue

            # ambil piksel pusat
            r, g, b = pixels[x, y]

            # Ambil tetangga 8 untuk tiap channel
            tetangga_r = []
            tetangga_g = []
            tetangga_b = []

            for yy in range(y-1, y+2):
                for xx in range(x-1, x+2):
                    if xx == x and yy == y:
                        continue  # skip pusat
                    rr, gg, bb = pixels[xx, yy]
                    tetangga_r.append(rr)
                    tetangga_g.append(gg)
                    tetangga_b.append(bb)

            # cari min & max tiap channel tepat seperti konsep filter batas
            minR, maxR = min(tetangga_r), max(tetangga_r)
            minG, maxG = min(tetangga_g), max(tetangga_g)
            minB, maxB = min(tetangga_b), max(tetangga_b)

            # aturan filter batas:
            r_new = minR if r < minR else maxR if r > maxR else r
            g_new = minG if g < minG else maxG if g > maxG else g
            b_new = minB if b < minB else maxB if b > maxB else b

            res_pixels[x, y] = (r_new, g_new, b_new)

    return result

def filter_mean(img):
    w, h = img.size
    pixels = img.load()

    # hasil tetap RGB
    result = Image.new("RGB", (w, h))
    res_pixels = result.load()

    for y in range(h):
        for x in range(w):

            # piksel tepi: langsung copy dari citra asli
            if x == 0 or y == 0 or x == w-1 or y == h-1:
                res_pixels[x, y] = pixels[x, y]
                continue

            sumR, sumG, sumB = 0, 0, 0
            count = 0

            # jendela 3x3 di sekitar (x, y)
            for yy in range(y-1, y+2):
                for xx in range(x-1, x+2):
                    r, g, b = pixels[xx, yy]
                    sumR += r
                    sumG += g
                    sumB += b
                    count += 1

            # rata-rata (mean) untuk tiap channel
            r_new = int(round(sumR / count))
            g_new = int(round(sumG / count))
            b_new = int(round(sumB / count))

            res_pixels[x, y] = (r_new, g_new, b_new)

    return result


def filter_median(img):
    w, h = img.size
    pixels = img.load()

    result = Image.new("RGB", (w, h))
    res_pixels = result.load()

    for y in range(h):
        for x in range(w):

            # piksel tepi tidak difilter, langsung disalin
            if x == 0 or y == 0 or x == w-1 or y == h-1:
                res_pixels[x, y] = pixels[x, y]
                continue

            window_r = []
            window_g = []
            window_b = []

            # ambil semua piksel di jendela 3x3
            for yy in range(y - 1, y + 2):
                for xx in range(x - 1, x + 2):
                    r, g, b = pixels[xx, yy]
                    window_r.append(r)
                    window_g.append(g)
                    window_b.append(b)

            # urutkan dan ambil median
            window_r.sort()
            window_g.sort()
            window_b.sort()

            median_r = window_r[4]   # index tengah dari 9 elemen
            median_g = window_g[4]
            median_b = window_b[4]

            res_pixels[x, y] = (median_r, median_g, median_b)

    return result


def konvolusi(img, kernel):
    w, h = img.size
    pixels = img.load()

    result = Image.new("RGB", (w, h))
    res_pixels = result.load()

    for y in range(h):
        for x in range(w):

            if x == 0 or y == 0 or x == w-1 or y == h-1:
                res_pixels[x, y] = pixels[x, y]
                continue

            sumR, sumG, sumB = 0, 0, 0

            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    r, g, b = pixels[x + kx, y + ky]
                    weight = kernel[ky + 1][kx + 1]

                    sumR += r * weight
                    sumG += g * weight
                    sumB += b * weight

            r_new = max(0, min(255, int(sumR)))
            g_new = max(0, min(255, int(sumG)))
            b_new = max(0, min(255, int(sumB)))

            res_pixels[x, y] = (r_new, g_new, b_new)

    return result

def deteksi_tepi(img):
    # TODO: isi logika deteksi tepi (Sobel / Prewitt / Laplacian)
    print("[INFO] deteksi_tepi belum diimplementasikan, mengembalikan citra asli.")
    return img


# ==========================
# Main Program 
# ==========================
if __name__ == "__main__":
    img = Image.open("images/Orangutan.jpg")

    while True:
        print("\n=== MENU OPERASI FILTER TETANGGAAN ===")
        print("0. Keluar")
        print("1. Filter Batas")
        print("2. Filter Mean")
        print("3. Filter Median")
        print("4. Konvolusi (Low / High / High-Boost / Emboss)")

        try:
            pilihan = int(input("Pilih operasi (0-4): "))
        except ValueError:
            print("Input tidak valid. Masukkan angka saja.")
            continue

        if pilihan == 0:
            print("Program selesai. Terima kasih!")
            break

        match pilihan:
            case 1:
                print("\n=== Filter Batas ===")
                res = filter_batas(img)
                res.save("images/1_FilterBatas.jpg")
                open(res, "Filter Batas")

            case 2:
                print("\n=== Filter Mean ===")
                res = filter_mean(img)
                res.save("images/2_FilterMean.jpg")
                open(res, "Filter Mean")

            case 3:
                print("\n=== Filter Median ===")
                res = filter_median(img)
                res.save("images/3_FilterMedian.jpg")
                open(res, "Filter Median")

            case 4:
                print("\n=== Konvolusi ===")
                print("1. Low Pass Filter")
                print("2. High Pass Filter")
                print("3. High Boost Filter")
                print("4. Emboss")

                try:
                    sub = int(input("Pilih jenis konvolusi (1-4): "))
                except ValueError:
                    print("Input tidak valid. Masukkan angka saja.")
                    continue

                # default
                kernel = None
                nama = ""
                filename = ""

                if sub == 1:
                    # Low Pass: blur sederhana 3x3 (dirata-ratakan)
                    k = [
                        [1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]
                    ]
                    # normalisasi 1/9
                    kernel = [[val / 9.0 for val in row] for row in k]
                    nama = "Low Pass Filter"
                    filename = "images/4a_LowPass.jpg"

                elif sub == 2:
                    # High Pass: penajaman / penekanan tepi
                    kernel = [
                        [-1, -1, -1],
                        [-1,  8, -1],
                        [-1, -1, -1]
                    ]
                    nama = "High Pass Filter"
                    filename = "images/4b_HighPass.jpg"

                elif sub == 3:
                    # High Boost: A * I - LowPass(I)
                    # di sini dipakai bentuk kernel langsung (misal A = 1.5)
                    kernel = [
                        [0,   -1,    0],
                        [-1,  5.5,  -1],
                        [0,   -1,    0]
                    ]
                    nama = "High Boost Filter"
                    filename = "images/4c_HighBoost.jpg"

                elif sub == 4:
                    # Emboss: efek timbul
                    kernel = [
                        [-2, -1, 0],
                        [-1,  1, 1],
                        [0,   1, 2]
                    ]
                    nama = "Emboss"
                    filename = "images/4d_Emboss.jpg"
                else:
                    print("Pilihan konvolusi tidak valid.")
                    continue

                res = konvolusi(img, kernel)
                res.save(filename)
                open(res, f"Konvolusi - {nama}")

            case _:
                print("Pilihan tidak valid. Coba lagi.")
