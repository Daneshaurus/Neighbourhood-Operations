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


def konvolusi(img):
    # TODO: isi logika konvolusi umum di sini (pakai kernel 3x3 misalnya)
    print("[INFO] konvolusi belum diimplementasikan, mengembalikan citra asli.")
    return img


def low_pass_filter(img):
    # TODO: isi logika low pass filter (blur / smoothing)
    print("[INFO] low_pass_filter belum diimplementasikan, mengembalikan citra asli.")
    return img


def high_pass_filter(img):
    # TODO: isi logika high pass filter (penajaman / edge emphasis)
    print("[INFO] high_pass_filter belum diimplementasikan, mengembalikan citra asli.")
    return img


def high_boost_filter(img):
    # TODO: isi logika high boost filter
    print("[INFO] high_boost_filter belum diimplementasikan, mengembalikan citra asli.")
    return img


def emboss(img):
    # TODO: isi logika emboss (relief)
    print("[INFO] emboss belum diimplementasikan, mengembalikan citra asli.")
    return img


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
        print("4. Konvolusi (Umum)")
        print("5. Low Pass Filter")
        print("6. High Pass Filter")
        print("7. High Boost Filter")
        print("8. Emboss")
        print("9. Deteksi Tepi")

        try:
            pilihan = int(input("Pilih operasi (0-9): "))
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
                print("\n=== Konvolusi Umum ===")
                res = konvolusi(img)
                res.save("images/4_Konvolusi.jpg")
                open(res, "Konvolusi")

            case 5:
                print("\n=== Low Pass Filter ===")
                res = low_pass_filter(img)
                res.save("images/5_LowPass.jpg")
                open(res, "Low Pass Filter")

            case 6:
                print("\n=== High Pass Filter ===")
                res = high_pass_filter(img)
                res.save("images/6_HighPass.jpg")
                open(res, "High Pass Filter")

            case 7:
                print("\n=== High Boost Filter ===")
                res = high_boost_filter(img)
                res.save("images/7_HighBoost.jpg")
                open(res, "High Boost Filter")

            case 8:
                print("\n=== Emboss ===")
                res = emboss(img)
                res.save("images/8_Emboss.jpg")
                open(res, "Emboss")

            case 9:
                print("\n=== Deteksi Tepi ===")
                res = deteksi_tepi(img)
                res.save("images/9_DeteksiTepi.jpg")
                open(res, "Deteksi Tepi")

            case _:
                print("Pilihan tidak valid. Coba lagi.")