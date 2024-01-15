import sqlite3
conn = sqlite3.connect("db_kasir.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS barang (kode_barang text, nama_barang text, harga_barang number, jumlah_barang number, harga_total number)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS transaksi (kode_barang text, nama_barang text, harga_barang number, jumlah_barang number, harga_total number)''')
def get_barang(kode_barang):
    cursor.execute("SELECT * FROM barang WHERE kode_barang = ?", (kode_barang,))
    row = cursor.fetchone()
    if row:
        return {"nama_barang": row[1], "harga_barang": row[2]}
    else:
        return None

def lihat_pembelian():
    cursor.execute("SELECT kode_barang, nama_barang, harga_barang, jumlah_barang, harga_total FROM transaksi WHERE jumlah_barang > 0")
    rows = cursor.fetchall()
    if rows:
        print("Data Pembelian Pelanggan")
        print("Kode Barang\tNama Barang\tHarga Barang\tJumlah Barang\tHarga Total")
        for row in rows:
            print(row[0], "\t\t", row[1], "\t\t", row[2], "\t\t", row[3], "\t\t", row[4])
    else:
        print("Belum ada data pembelian")

def menu_pembayaran(total_harga):
            print("Menu Pembayaran")
            print("1. Tunai")
            print("2. Kartu Debit")
            print("3. E-Wallet")
            metode_pembayaran = input("Pilih metode pembayaran (1/2/3): ")
            if metode_pembayaran == "1":
                uang_tunai = int(input("Masukkan jumlah uang tunai: "))
                if uang_tunai >= total_harga:
                    kembalian = uang_tunai - total_harga
                    print("Kembalian: ", kembalian)
                    print("Terima kasih!")
                else:
                    print("Uang tunai kurang")
            elif metode_pembayaran == "2":
                print("Pembayaran dengan kartu debit transaksi berhasil")
            elif metode_pembayaran == "3":
                print("Pembayaran dengan e-wallet transaksi berhasil")
            else:
                print("Pilihan tidak valid")
print("Selamat Datang")
print("1. Login sebagai admin")
print("2. Login sebagai kasir")
pilihan_login = input("Masukkan pilihan login (1/2): ")
if pilihan_login == "1":
    while True:
        print("Menu CRUD")
        print("1. Tambah barang")
        print("2. Lihat barang")
        print("3. Ubah barang")
        print("4. Hapus barang")
        print("5. Data Pembelian")
        print("6. Logout")
        pilihan_menu = input("Masukkan pilihan menu (1-6): ")
        if pilihan_menu == "1":
            nama_barang = input("Masukkan nama barang: ")
            kode_barang = input("Masukkan kode barang: ")
            harga_barang = input("Masukkan harga barang: ")
            jumlah_barang = input("Masukkan jumlah barang: ")
            harga_total = int(harga_barang) * int(jumlah_barang)
            cursor.execute("INSERT INTO barang (kode_barang, nama_barang, harga_barang, jumlah_barang, harga_total) VALUES (?, ?, ?, ?, ?)", (kode_barang, nama_barang, harga_barang, jumlah_barang, harga_total))
      
            print("Data barang berhasil ditambahkan")
        elif pilihan_menu == "2":
            cursor.execute("SELECT * FROM barang")
            rows = cursor.fetchall()
            if rows:
                print("Kode Barang\tNama Barang\tHarga Barang\tJumlah Barang\tHarga Total")
                for row in rows:
                    print(row[0], "\t\t", row[1], "\t\t", row[2], "\t\t", row[3], "\t\t", row[4])
            else:
                print("Belum ada data barang")
        elif pilihan_menu == "3":
            kode_barang = input("Masukkan kode barang yang ingin diubah: ")
            cursor.execute("SELECT * FROM barang WHERE kode_barang = ?", (kode_barang,))
            row = cursor.fetchone()
            if row:
                print("Data Barang Lama:")
                print("Kode Barang:", row[0])
                print("Nama Barang:", row[1])
                print("Harga Barang:", row[2])
                print("Jumlah Barang:", row[3])
                print("Harga Total:", row[4])
                nama_barang = input("Masukkan nama barang baru: ")
                harga_barang = input("Masukkan harga barang baru: ")
                jumlah_barang = input("Masukkan jumlah barang baru: ")
                harga_total = int(harga_barang) * int(jumlah_barang)
                cursor.execute("UPDATE barang SET nama_barang = ?, harga_barang = ?, jumlah_barang = ?, harga_total = ? WHERE kode_barang = ?", (nama_barang, harga_barang, jumlah_barang, harga_total, kode_barang))
                conn.commit()
                print("Data barang berhasil diubah")
            else:
                print("Data barang tidak ditemukan")
        elif pilihan_menu == "4":
            kode_barang = input("Masukkan kode barang yang ingin dihapus: ")
            cursor.execute("DELETE FROM barang WHERE kode_barang = ?", (kode_barang,))
            conn.commit()
            print("Data barang berhasil dihapus")
        elif pilihan_menu == "5":
            lihat_pembelian()
        elif pilihan_menu == "6":
            print("Anda telah logout")
            while True:
                pilihan_kembali = input("Kembali ke menu CRUD? (y/n): ")
                if pilihan_kembali == "y":
                    break
                elif pilihan_kembali == "n":
                    while True:
                        pilihan_logout = input("Logout? (y/n): ")
                        if pilihan_logout == "y":
                            print("Anda telah logout")
                            break
                        elif pilihan_logout == "n":
                            break
                    break
                else:
                    print("Pilihan tidak valid")
            break
        else:
            print("Pilihan tidak valid")
elif pilihan_login == "2":
    keranjang = []
    while True:
        kode_barang = input("Masukkan kode barang: ")
        barang = get_barang(kode_barang)
        if barang:
            nama_barang = barang["nama_barang"]
            harga_barang = barang["harga_barang"]
            print("Nama Barang:", nama_barang)
            print("Harga Barang:", harga_barang)
            jumlah_barang = int(input("Masukkan jumlah barang yang ingin dibeli: "))
            harga_total = harga_barang * jumlah_barang
            print("Harga Total:", harga_total)
            keranjang.append({"nama_barang": nama_barang, 
                              "harga_barang": harga_barang, 
                              "jumlah_barang": jumlah_barang, 
                              "harga_total": harga_total})
            cursor.execute("INSERT INTO transaksi (kode_barang, nama_barang, harga_barang, jumlah_barang, harga_total) VALUES (?, ?, ?, ?, ?)", (kode_barang, nama_barang, harga_barang, jumlah_barang, harga_total))
            conn.commit()
        else:
            print("Kode barang tidak ditemukan")
        pilihan_tambah = input("Tambah barang? (y/n): ")
        if pilihan_tambah == "n":
            break
        

    print("Nama Barang\tHarga Satuan\tJumlah\tHarga Total")
    total_harga = 0
    for barang in keranjang:
        print(barang["nama_barang"], "\t\t", barang["harga_barang"], "\t\t", barang["jumlah_barang"], "\t\t", barang["harga_total"])
        total_harga += barang["harga_total"]
    print("Total Harga:", total_harga)
    menu_pembayaran(total_harga)
conn.close()
