
# ==========================================
# SISTEM PENJUALAN PRODUK SKINCARE
# ==========================================

# Data pengguna
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# Data produk skincare
produk = {
    1: {"nama": "Facial Wash", "harga": 45000, "stok": 20},
    2: {"nama": "Serum", "harga": 98000, "stok": 10},
    3: {"nama": "Sunscreen SPF 50", "harga": 85000, "stok": 15}
}

id_terakhir = 3

# Format harga rupiah
rupiah = lambda angka: f"Rp{angka:,}".replace(",", ".")


# Validasi input angka
def input_angka(pesan, minimum, maksimum):
    while True:
        try:
            angka = int(input(pesan))
        except ValueError:
            print("Input harus berupa angka!")
            continue

        if minimum <= angka <= maksimum:
            return angka

        print(f"Masukkan angka antara {minimum} sampai {maksimum}.")


# Validasi input teks
def input_teks(pesan):
    while True:
        teks = input(pesan).strip()

        if teks and not teks.isdigit():
            return teks

        print("Nama produk tidak boleh kosong atau hanya angka.")


# Memilih produk berdasarkan ID
def pilih_produk():
    while True:
        kode = input_angka("Masukkan ID produk (0 untuk batal): ", 0, 999)

        if kode == 0 or kode in produk:
            return kode

        print("ID produk tidak ditemukan.")


# Menampilkan daftar produk
def lihat_produk():
    print("\n=== DAFTAR PRODUK SKINCARE ===")
    print(f"{'ID':<5}{'Nama':<25}{'Harga':<15}Stok")

    for kode, p in produk.items():
        print(f"{kode:<5}{p['nama']:<25}"
              f"{rupiah(p['harga']):<15}{p['stok']}")

    if not produk:
        print("Belum ada produk.")


# Mengisi data produk
def isi_data_produk(kode_lama=None):
    while True:
        nama = input_teks("Nama produk: ")

        # Mengecek nama produk agar tidak duplikat
        nama_ada = {
            p["nama"].lower()
            for kode, p in produk.items()
            if kode != kode_lama
        }

        if nama.lower() not in nama_ada:
            break

        print("Nama produk sudah tersedia!")

    harga = input_angka("Harga produk: ", 1000, 1000000)
    stok = input_angka("Jumlah stok: ", 0, 1000)

    return {
        "nama": nama,
        "harga": harga,
        "stok": stok
    }


# Menu admin
def menu_admin():
    global id_terakhir

    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Tambah Produk")
        print("2. Lihat Produk")
        print("3. Ubah Produk")
        print("4. Hapus Produk")
        print("0. Logout")

        menu = input_angka("Pilih menu: ", 0, 4)

        if menu == 0:
            break

        elif menu == 1:
            id_terakhir += 1
            produk[id_terakhir] = isi_data_produk()
            print("Produk berhasil ditambahkan.")

        elif menu == 2:
            lihat_produk()

        else:
            lihat_produk()
            kode = pilih_produk()

            if kode == 0:
                continue

            if menu == 3:
                produk[kode] = isi_data_produk(kode)
                print("Produk berhasil diubah.")

            elif menu == 4:
                del produk[kode]
                print("Produk berhasil dihapus.")


# Menu pembeli
def menu_user():
    keranjang = []

    while True:
        print("\n=== MENU USER ===")
        print("1. Lihat Produk")
        print("2. Beli Produk")
        print("3. Lihat Keranjang")
        print("4. Checkout")
        print("0. Logout")

        menu = input_angka("Pilih menu: ", 0, 4)

        if menu == 0:
            # Mengembalikan stok jika belum checkout
            for kode, nama, harga, jumlah in keranjang:
                produk[kode]["stok"] += jumlah

            break

        elif menu == 1:
            lihat_produk()

        elif menu == 2:
            lihat_produk()
            kode = pilih_produk()

            if kode == 0:
                continue

            p = produk[kode]

            if p["stok"] == 0:
                print("Stok produk habis.")
                continue

            jumlah = input_angka("Jumlah pembelian: ", 1, p["stok"])

            keranjang.append([kode, p["nama"], p["harga"], jumlah])
            p["stok"] -= jumlah

            print("Produk berhasil dimasukkan ke keranjang.")

        elif menu == 3:
            # Menampilkan isi keranjang
            if not keranjang:
                print("Keranjang masih kosong.")
            else:
                print("\n=== ISI KERANJANG ===")
                total = 0

                for kode, nama, harga, jumlah in keranjang:
                    subtotal = harga * jumlah
                    total += subtotal

                    print(f"{nama} x{jumlah} = {rupiah(subtotal)}")

                print("--------------------------")
                print("Total sementara:", rupiah(total))

        elif menu == 4:
            if not keranjang:
                print("Keranjang masih kosong.")
                continue

            total = 0

            print("\n=== STRUK BELANJA ===")

            for kode, nama, harga, jumlah in keranjang:
                subtotal = harga * jumlah
                total += subtotal

                print(f"{nama} x{jumlah} = {rupiah(subtotal)}")

            # Diskon 10% jika belanja minimal Rp200.000
            diskon = total * 10 // 100 if total >= 200000 else 0

            print("--------------------------")
            print("Total belanja :", rupiah(total))
            print("Diskon        :", rupiah(diskon))

            total_bayar = total - diskon
            print("Total bayar   :", rupiah(total_bayar))

            # Pilihan metode pembayaran (Tuple)
            METODE_PEMBAYARAN = ("Cash", "QRIS")

            print("\n=== METODE PEMBAYARAN ===")

            for i, metode in enumerate(METODE_PEMBAYARAN, 1):
                print(f"{i}. {metode}")

            pilihan_bayar = input_angka(
                "Pilih metode pembayaran: ",
                1,
                len(METODE_PEMBAYARAN)
            )

            metode_terpilih = METODE_PEMBAYARAN[pilihan_bayar - 1]
            print("Metode pembayaran:", metode_terpilih)

            # Proses pembayaran berdasarkan metode
            if metode_terpilih == "Cash":
                while True:
                    bayar = input_angka(
                        "Uang pembayaran: ", 0, 100000000
                    )

                    if bayar >= total_bayar:
                        break

                    print("Uang pembayaran masih kurang.")

                kembalian = bayar - total_bayar
                print("Kembalian:", rupiah(kembalian))

            elif metode_terpilih == "QRIS":
                print(
                    "Silakan scan QRIS untuk pembayaran sebesar:",
                    rupiah(total_bayar)
                )
                print("Simulasi: Pembayaran QRIS berhasil dikonfirmasi.")

            print("Terima kasih sudah berbelanja!")

            keranjang.clear()


# Proses login
def login():
    for kesempatan in range(3):
        username = input("Username: ").strip()
        password = input("Password: ")

        if username in users and users[username]["password"] == password:
            return users[username]["role"]

        print("Username atau password salah.")

    print("Kesempatan login habis.")
    return None


# Menu utama program
while True:
    print("\n=== TOKO SKINCARE ===")
    print("1. Login")
    print("0. Keluar")

    pilihan = input_angka("Pilih menu: ", 0, 1)

    if pilihan == 0:
        print("mator skalangkong .")
        break

    role = login()

    if role == "admin":
        menu_admin()

    elif role == "user":
        menu_user()
