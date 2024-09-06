# Mengimpor modul yang dibutuhkan
import ping3  # Modul untuk mengirim ping ke alamat IP
import time  # Modul untuk menangani waktu
import speedtest_cli as speedtest  # Modul untuk mengukur kecepatan internet
import os # Modul untuk mengakses OS
import json # Modul untuk membaca file json
import logging
import socket #modul untuk mendapatkan IP Comp
import sqlite3 # Modul untuk menyimpan data hasil test ke database 

def menyimpan_ke_database(test_time,local_ip,ip_address,status,rtt,download_speed,upload_speed):
    """
    Menyimpan hasil tes ke dalam database SQLite.

    Args:
        test_time (str): Waktu pelaksanaan tes.
        local_ip (str): Alamat IP lokal.
        ip_address (str): Alamat IP yang diuji.
        status (str): Status koneksi (misal: reachable, unreachable).
        rtt (float): Waktu respon rata-rata (dalam ms).
        download_speed (float): Kecepatan download (dalam Mbps).
        upload_speed (float): Kecepatan upload (dalam Mbps).
    """
    conn = sqlite3.connect('networks_monitor.db')
    cursor = conn.cursor()

    # Membuat tabel jika belum ada
    cursor.execute('''CREATE TABLE IF NOT EXISTS networks
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      test_time TEXT, 
                      local_ip TEXT, 
                      ip_address TEXT, 
                      status TEXT, 
                      rtt REAL, 
                      download_speed REAL, 
                      upload_speed REAL)''')
    
    # Menyiapkan data untuk dimasukkan
    data = (test_time, local_ip, ip_address, status, rtt, download_speed, upload_speed)

    # Memasukkan data ke database
    cursor.execute('''
                   INSERT INTO networks (test_time, local_ip, ip_address, status, rtt, download_speed, upload_speed)
                   VALUES (?,?,?,?,?,?,?)''', data)
    
    conn.commit()
    conn.close()
    logging.info(f"Data hasil tes berhasil disimpan ke database")

def mendaptakan_ip_local():
    """
    Fungsi ini dibuat untuk mendapatkan IP lokal komputer
    """
    try:
        # Mendapatkan hostname
        hostname = socket.gethostname()
        # Mendapatkan IP address yang terhubung ke internet
        lokal_ip = socket.gethostbyname(hostname)
        return lokal_ip
    except Exception as e:
        logging.error(f"Error getting local IP : {e}")
        return None
    

# Konfigurasi logging module
logging.basicConfig(filename='network.monitor.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
# Fungsi untuk mengirim ping ke IP yang diberikan
def read_config(config_file): #untuk membaca nama file .json
    """
    Fungsi untuk membaca file JSON yang berisi pengaturan.
    :param config_file: Nama file JSON yang berisi pengaturan.
    :return: Objek pengaturan yang telah dibaca.
    """
    try:
        with open(config_file, 'r') as f:
            '''
            Mencoba membuka file JSON dalam mode baca ('r').
            Jika file berhasil dibuka, isinya dibaca dan diubah menjadi objek Python (dictionary) menggunakan json.load(f).
            Objek pengaturan yang telah dibaca kemudian dikembalikan (return config).
            '''
            config = json.load(f)
            logging.info(f"Configuration loaded from {config_file}")
        return config
    except FileNotFoundError as e:
        logging.error(f"Error reading configuration file : {e}")
        print(f"Error: {e}")
        return None
    
def welcome_message():
    """Menampilkan pesan selamat datang dan informasi aplikasi."""
    logging.info(f"Displaying welcome message")
    # Mencetak garis pemisah dan judul aplikasi
    print("\n==================================================")
    print("---------------USER NETWORK TOOLS------------------")
    print("====================================================")
    # Mencetak waktu pengecekan saat ini
    print(f"Waktu Pengecekan: {time.strftime('%A, %d %B %Y %H:%M:%S')}")
    print("----------------------------------------------------\n")

# Fungsi untuk menguji kecepatan internet
def test_internet_speed():
    try:
        # Membuat objek Speedtest dengan parameter secure=True untuk menggunakan HTTPS
        st = speedtest.Speedtest(secure=True)
        logging.info('Testing internet speed')
        print(f"Testing internet speed...Mohon menunggu...")  # Memberi tahu pengguna bahwa tes sedang berjalan
        
        # Mendapatkan server terbaik untuk pengujian
        st.get_best_server()
        best = st.get_best_server()  # Menyimpan server terbaik dalam variabel

        # Melakukan tes kecepatan download
        download_speed = st.download() / 1000000  # Konversi ke Mbps

        # Melakukan tes kecepatan upload
        upload_speed = st.upload() / 1000000  # Konversi ke Mbps

        # Menampilkan hasil tes kecepatan internet
        print("----------------------------------------------------")
        print("**** Download Speed:======>> {:.2f} Mbps".format(download_speed))
        print("**** Upload Speed  :======>> {:.2f} Mbps".format(upload_speed))
        print("----------------------------------------------------")
        print(f"Found: {best['host']} -- Located in {best['country']}")
        print("----------------------------------------------------")
        logging.info(f"Internet speed test results - Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps")

        return download_speed, upload_speed

    except speedtest.SpeedtestException as e:
        # Menangani kesalahan jika tes kecepatan gagal
        logging.error(f"Error during the speed test: {str(e)}")
        print("Gagal Melakukan speed test karena :", str(e))
        print("An error occurred during the speed test:", str(e))
        return None, None

def ping(ip):
    """Mengirimkan ping ke alamat IP dan mengembalikan RTT jika berhasil, None jika gagal."""
    try:
        # Mengirim ping ke alamat IP yang diberikan
        response = ping3.ping(ip)
        if response:
            logging.info(f"Ping to {ip} succeeded with RTT: {response:.2f} ms")
            return response
        else:
            logging.warning(f"Ping to {ip} failed")
            return None
    except Exception as e:
        # Menangani pengecualian jika ping gagal
        logging.error(f"Failed to ping {ip} : {str(e)}")
        return None

def check_network(ip_list, counter=4):
    """Memeriksa status jaringan untuk daftar alamat IP."""
    
    try:
        # Mengiterasi setiap pasangan nama dan alamat IP dalam daftar
        for ip_config in ip_list:
            alamat_ip = ip_config['ip']
            nama_ip = ip_config['name']
            gagal = 0  # Menghitung jumlah ping yang gagal
            berhasil = 0  # Menghitung jumlah ping yang berhasil
            rtt_total = 0  # Menghitung total RTT untuk rata-rata
            for _ in range(counter):  # Mengirim ping sejumlah counter kali
                rtt = ping(alamat_ip)
                if rtt:  # Jika ping berhasil
                    berhasil += 1
                    rtt_total += rtt
                    logging.info(f"{nama_ip} ({alamat_ip}) Connection is good : {rtt:.2f} ms")
                else:  # Jika ping gagal
                    gagal += 1
                    logging.warning(f"Host {nama_ip} ({alamat_ip}) Request time out")

            # Menampilkan status koneksi berdasarkan hasil ping
            if gagal == counter:  # Jika semua ping gagal
                status = "unreachable"
                print(f"Host {nama_ip} ({alamat_ip}) ====>> is unreachable \n")
                print('______________________________________________________________________')
                logging.warning(f"Host {nama_ip} ({alamat_ip}) is unreachable")
            elif gagal < counter and gagal > 1:  # Jika beberapa ping gagal
                status = "poor connection"
                rtt_avg = rtt_total / berhasil
                print(f"Host {nama_ip} ({alamat_ip}) ====>> mengalami koneksi kurang bagus. \n")
                print('______________________________________________________________________')
                logging.warning(f"Host {nama_ip} ({alamat_ip}) has poor connection")
            else:  # Jika semua atau hampir semua ping berhasil
                status = "reachable"
                rtt_avg = rtt_total / berhasil 
                print(f"Host {nama_ip} ({alamat_ip}) ====>> is OK!. Koneksi jaringan bagus Ping time: {rtt_avg:.2f} ms")
                print('______________________________________________________________________')
                logging.info(f"Host {nama_ip} ({alamat_ip}) is reachable Ping time: {rtt_avg:.2f} ms")
    
            # Mendapatkan hasil tes kecepatan internet
            download_speed, upload_speed = test_internet_speed()

            # Menyimpan hasil tes ke database
            test_time = time.strftime('%Y-%m-%d %H:%M:%S')
            local_ip = mendaptakan_ip_local()
            menyimpan_ke_database(test_time, local_ip, alamat_ip, status, rtt_avg, download_speed, upload_speed)

                
    
    except Exception as e:
        # Menangani pengecualian jika terjadi kesalahan selama pengecekan jaringan
        logging.error(f"Failed to check network: {str(e)}")
        print(f"Failed to check network: {str(e)}")


# Fungsi utama untuk menjalankan program
if __name__ == "__main__":
    welcome_message()
    config = read_config("ip_config.json")
    if config:
        # Melakukan pengecekan jaringan menggunakan konfigurasi yang telah dibaca
        check_network(config["ip_list"])
    else:
        print("Error: Unable to read configuration. Please check the configuration file.")
