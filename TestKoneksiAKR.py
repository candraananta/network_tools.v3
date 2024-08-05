import subprocess  # Mengimpor modul subprocess untuk menjalankan perintah sistem

def ping_ip(ip):
    """
    Fungsi untuk melakukan ping ke IP yang diberikan.
    :param ip: Alamat IP yang akan diuji koneksinya.
    :return: True jika koneksi berhasil, False jika gagal.
    """

    pesanError = subprocess.check_output

    try:
        # Menjalankan perintah ping menggunakan subprocess
        output = subprocess.check_output(['ping', '-n', '1', ip], stderr=subprocess.STDOUT, universal_newlines=True)
        # Memeriksa apakah ada string "TTL=" dalam output, yang menunjukkan bahwa ping berhasil
        if "TTL=" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        # Jika terjadi kesalahan dalam menjalankan perintah ping, kembalikan False
        return False , pesanError

def test_connections(ip_list, num_tests=2):
    """
    Fungsi untuk menguji koneksi ke daftar IP yang diberikan.
    :param ip_list: Daftar alamat IP yang akan diuji koneksinya.
    :param num_tests: Jumlah ping yang akan dilakukan untuk setiap IP.
    """
    for ip_name, ip_address in ip_list.items():
        # Looping melalui setiap item dalam daftar IP
        failures = 0  # Counter untuk jumlah kegagalan
        for _ in range(num_tests):
            # Melakukan ping sebanyak num_tests kali
            if not ping_ip(ip_address):
                # Jika ping gagal, tambahkan counter kegagalan
                failures += 1

        # Menghitung persentase kegagalan
        failure_rate = (failures / num_tests) * 100

        # Memeriksa hasil koneksi dan menampilkan pesan yang sesuai
        if failure_rate == 0:
            # Jika tidak ada kegagalan, koneksi bagus
            print(f"Koneksi ke {ip_name} ({ip_address}) berhasil. Koneksi jaringan bagus.")
        elif failure_rate < 20:
            # Jika kegagalan lebih dari 20%, koneksi intermitten
            print(f"Koneksi ke {ip_name} ({ip_address}) mengalami koneksi intermitten.")
        elif failure_rate == 100:
            # Jika kegagalan lebih dari 100%, koneksi intermitten
            print(f"Koneksi ke {ip_name} ({ip_address}) mengalami koneksi putus.")
        else:
            # Jika kegagalan ada tapi kurang dari 20%, tampilkan jumlah kegagalan
            print(f"Koneksi ke {ip_name} ({ip_address}) gagal sebanyak {failures} dari {num_tests} kali uji.")

if __name__ == "__main__":
    # Daftar alamat IP yang akan diuji koneksinya
    ip_list = {
        "QAD": "192.168.150.155",
        "VSS": "192.168.160.101",
        "System Manager": "192.168.150.166",
        "M-Files": "192.168.160.112",
        "HRIS": "192.168.160.106"
    }
    # Memanggil fungsi test_connections untuk menguji koneksi ke daftar IP

    test_connections(ip_list)
    input("Tekan enter untuk keluar....")



