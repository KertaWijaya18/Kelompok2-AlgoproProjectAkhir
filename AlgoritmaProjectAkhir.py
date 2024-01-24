import datetime
import sqlite3
daftar_barang = {
    "B001": {"nama": "Black Forest", "harga": 110000},
    "B002": {"nama": "Cheese Cake", "harga": 200000},
    "B003": {"nama": "Choco Brownies", "harga": 160000},
    "B004": {"nama": "Fruit Cake", "harga": 180000},
    "B005": {"nama": "Greentea Cake", "harga": 160000},
    "B006": {"nama": "Lapis Surabaya", "harga": 160000},
    "B007": {"nama": "Oreo Cake", "harga": 160000},
    "B008": {"nama": "Rainbow Cake", "harga": 160000},
    "B009": {"nama": "Red Velvet Cake", "harga": 180000},
    "B0010": {"nama": "Tiramisu Cake", "harga": 160000},
}
print("Navigasi = Menu utama\n")
nama_toko = "Toko Cake"
alamat_toko = "Jl. Sudirman No. 123"
print(f"{nama_toko}\n{alamat_toko}\n")
waktu = datetime.datetime.now()
print(f"Waktu: {waktu.strftime('%d/%m/%Y %H:%M:%S')}\n")
print("List:")
print("1. Login kasir")
print("2. Riwayat transaksi")
print("3. Lihat daftar harga")
print("4. Exit")
nomor_menu = input("Masukkan nomor menu yang dipilih: ")
if nomor_menu == "1":
    kode_kasir = input("Masukkan kode kasir: ")
    if kode_kasir == "001":
        nama_kasir = "Reza Zidan"
    elif kode_kasir == "002":
        nama_kasir = "Kerta Wijaya"
    else:
        nama_kasir = "Kasir Tidak Dikenal"
        print(nama_kasir)
        exit()
    print(f"\nNavigasi = Menu Utama -> Login Kasir -> Transaksi\n")
    input("Tekan enter untuk memulai transaksi...")
    transaksi = []
    while True:
        kode_barang = input("Masukkan kode barang (klik enter untuk selesai, x untuk batal): ")
        if kode_barang.lower() == "x":
            break
        elif kode_barang in daftar_barang:
            print(f"{daftar_barang[kode_barang]['nama']} - Rp {daftar_barang[kode_barang]['harga']}")
            # Input jumlah barang
            jumlah = int(input("Masukkan jumlah: "))
            transaksi.append({"kode_barang": kode_barang, 
                              "nama_barang": daftar_barang[kode_barang]['nama'], 
                              "harga_satuan": daftar_barang[kode_barang]['harga'], 
                              "jumlah": jumlah})

    print(f"\n{'Nama Toko':<15} {nama_toko}")
    print(f"{'Alamat':<15} {alamat_toko}\n")
    print(f"{'Nama Kasir':<15} {nama_kasir}")
    print(f"{'Waktu':<15} {waktu.strftime('%d/%m/%Y %H:%M:%S')}\n")
    print(f"{'Nama Barang':<20} {'Ukuran':<10} {'QTY':<10} {'Harga':<10} {'Total Harga':<10}")
    print("-" * 60)
    total_harga = 0
    for item in transaksi:
        total_harga_item = item['harga_satuan'] * item['jumlah']
        print(f"{item['nama_barang']:<20} {'':<10} {item['jumlah']:<10} {item['harga_satuan']:<10} {total_harga_item:<10}")
        total_harga += total_harga_item
    print("-" * 60)
    print(f"{'Jumlah Harga':<50} {total_harga:>10}")
    print("-" * 60)
    uang_tunai = int(input("Bayar tunai: "))
    kembalian = uang_tunai - total_harga
    print("-" * 60)
    print(f"{'Kembalian':<50} {kembalian:>10}")
    print("-" * 60)
    print("Terima kasih telah berbelanja di Toko Cake!")
    conn = sqlite3.connect('transactions.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 date TEXT NOT NULL,
                 cashier TEXT NOT NULL,
                 item TEXT NOT NULL,
                 quantity INTEGER NOT NULL,
                 price INTEGER NOT NULL,
                 total INTEGER NOT NULL);''')
    date = waktu.strftime('%d/%m/%Y %H:%M:%S')
    for item in transaksi:
        item_name = item['nama_barang']
        quantity = item['jumlah']
        price = item['harga_satuan']
        total = item['harga_satuan'] * item['jumlah']
        conn.execute(f"INSERT INTO transactions (date, cashier, item, quantity, price, total) VALUES ('{date}', '{nama_kasir}', '{item_name}', {quantity}, {price}, {total})")
    conn.commit()
    conn.close()
elif nomor_menu == "2":
    print("\nNavigasi = Menu Utama -> Riwayat transaksi -> Lihat riwayat transaksi\n")
    print(f"{nama_toko}\n{alamat_toko}\n")
    print(f"Waktu: {waktu.strftime('%d/%m/%Y %H:%M:%S')}\n")
    print("Riwayat transaksi")
    print("-" * 7)
    conn = sqlite3.connect('transactions.db')
    cursor = conn.execute("SELECT date, cashier, item, quantity, price, total FROM transactions")
    transactions = cursor.fetchall()
    total_transaksi = 0
    total_penjualan = 0
    total_uang_diterima = 0
    for transaction in transactions:
        date = transaction[0]
        cashier = transaction[1]
        item = transaction[2]
        quantity = transaction[3]
        price = transaction[4]
        total = transaction[5]
        print("\n")
        print("-" * 9)
        print(f"{'':<1}{'nama kasir:':<20}{cashier}")
        print(f"{'':<1}{'waktu:':<20}{date}")
        print("\n")
        print(f"{'':<1}{'nama barang':<20}{'QTY':<10}{'harga satuan':<15}{'total harga':<15}")
        print(f"{'':<1}{'-----':<20}{'----':<10}{'------------':<15}{'-----------':<15}")
        print(f"{'':<1}{item:<20}{quantity:<10}{price:<15}{total:<15}")
        print(f"{'':<1}{'jumlah harga total:':<50}{total:<10}")
        print(f"{'':<1}{'jumlah bayar:':<50}{total:<10}")
        print(f"{'':<1}{'':<50}{'':<10}")
        total_transaksi += 1
        total_penjualan += total
        total_uang_diterima += total
        print("-" * 7)
        print(f"{'':<1}{'Total transaksi:':<50}{total_transaksi:<10}")
        print(f"{'':<1}{'Total penjualan:':<50}{total_penjualan:<10}")
        print(f"{'':<1}{'Total uang yang diterima:':<50}{total_uang_diterima:<10}")
        print("-" * 7)
elif nomor_menu == "3":
    print("Daftar Harga Menu Kue")
    print(f"Kode Barang {'':<8} | Nama Barang {'':<18} | Harga")
    for kode, barang in daftar_barang.items():
        print(f"{kode:<20} | {barang['nama']:<30} | {barang['harga']}")
elif nomor_menu == "4":
    exit()
else:
    print("Nomor tidak valid")   