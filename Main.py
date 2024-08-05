# Mengimpor modul yang dibutuhkan
import ping3  # Modul untuk mengirim ping ke alamat IP
import time  # Modul untuk menangani waktu
import speedtest_cli as speedtest  # Modul untuk mengukur kecepatan internet
import os # Modul untuk mengakses OS
import json # Modul untuk membaca file json
import logging
import socket #modul untuk mendapatkan IP Comp

def mendaptakan_ip_local():
    """
    fungsi ini dibuat unntuk mendapatkan IP lokal komputer
    """
    try:
        #mendapatkan hostname
        hostname = socket.gethostname()
        #mendapatkan IP address yang terhubung ke internet
        lokal_ip = socket.gethostbyname(hostname)
        return lokal_ip
    except Exception as e:
        logging.error(f"Error getting local IP : {e}")
        return None
    

#konfigurasi logging module
logging.basicConfig(filename='network.monitor.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Fungsi untuk mengirim ping ke IP yang diberikan
def ping_ip(ip):
        """
        Fungsi untuk melakukan ping ke IP yang diberikan.
        :param ip: Alamat IP yang akan diuji koneksinya.
        :return: True jika koneksi berhasil, False jika gagal.
        """
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
             logging.info(f"Configuration loaded from  {config_file}")
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
    print("-----------------AKR NETWORK TOOLS------------------")
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

    except speedtest.SpeedtestException as e:
        # Menangani kesalahan jika tes kecepatan gagal
        logging.error(f"Error during the speed test: {str(e)}")
        print("Gagal Melakukan speed test karena :", str(e))
        print("An error occurred during the speed test:", str(e))

def ping(ip):
    """Mengirimkan ping ke alamat IP dan mengembalikan True jika berhasil, False jika gagal."""
    try:
        # Mengirim ping ke alamat IP yang diberikan
        response = ping3.ping(ip)
        logging.info(f"Ping to {ip} {'Succeeded' if response else 'failed'}")
        # Mengembalikan True jika ada respons, False jika tidak ada
        return response is not None and response
    except Exception as e:
        # Menangani pengecualian jika ping gagal
        logging.error(f"Failed to ping {ip} : {str(e)}")
        return False

def check_network(ip_list, counter=4):
    """Memeriksa status jaringan untuk daftar alamat IP."""
    
    try:
        # Mengiterasi setiap pasangan nama dan alamat IP dalam daftar
        for ip_config in ip_list:
            alamat_ip = ip_config['ip']
            nama_ip = ip_config['name']
            gagal = 0  # Menghitung jumlah ping yang gagal
            berhasil = 0  # Menghitung jumlah ping yang berhasil
            for _ in range(counter):  # Mengirim ping sejumlah counter kali
                if not ping(alamat_ip):  # Jika ping gagal
                    gagal += 1
                else:  # Jika ping berhasil
                    berhasil += 1
            
            # Menampilkan status koneksi berdasarkan hasil ping
            if gagal == counter:  # Jika semua ping gagal
                print(f"Host {nama_ip} ({alamat_ip}) ====>> is unreachable \n")
                print('______________________________________________________________________')
                logging.warning(f"Host {nama_ip} ({alamat_ip}) is unreachable")
                # print(f"gagal = {gagal}")
                # print(f"berhasil = {berhasil}")
            elif gagal < counter and gagal > 1:  # Jika beberapa ping gagal
                print(f"Host {nama_ip} ({alamat_ip}) ====>> mengalami koneksi kurang bagus. \n")
                print('______________________________________________________________________')
                logging.warning(f"Host {nama_ip} ({alamat_ip}) has poor connection")
                # print(f"gagal = {gagal}")
                # print(f"berhasil = {berhasil}")
            else:  # Jika semua atau hampir semua ping berhasil
                print(f"Host {nama_ip} ({alamat_ip}) ====>> is reachable. Koneksi jaringan bagus. \n")
                print('______________________________________________________________________')
                logging.info(f"Host {nama_ip} ({alamat_ip}) is reachable")
                # print(f"berhasil = {berhasil}")
                # print(f"gagal = {gagal}")
    except Exception as e:
        # Menangani pengecualian jika terjadi kesalahan selama pengecekan jaringan
        logging.error(f'Error ketika melakukan ping karena +{e}')
        print(f"An error occurred: {e}")

def tampil(inputan):
    """Memanggil fungsi untuk mengecek jaringan dan menguji kecepatan internet."""
    check_network(ip_addresses)  # Memeriksa status jaringan untuk daftar IP
    test_internet_speed()  # Menguji kecepatan internet

if __name__ == "__main__":
    
    try:
        
        os.system("cls")
        welcome_message()  # Menampilkan pesan selamat datang

        #mendapatkan ip dan mencetak ip local
        iplcl = mendaptakan_ip_local()
        if iplcl is not None:
            print(f"==========  IP Computer anda adalah: {iplcl}  ==========")
            print("\n")
            logging.info(f'Alamat IP lokal adalah {iplcl}')
        else:
            print("Gagal mendapatkan alamat IP lokal")
            logging.error("Gagal mendapatkan alamat IP lokal")

        #membaca konfigurasi dari file
        config = read_config('config.json')
        ip_addresses = config['ip_addresses']
        check_network(ip_addresses) # Memeriksa status jaringan
        test_internet_speed()  # Menguji kecepatan internet 

        #looping untuk menjalankan program
        while True:
            answer = input("want to try again ? (y/n): ")
            if answer == "n":
                break 
            check_network(ip_addresses) # Memeriksa status jaringan
            test_internet_speed()  # Menguji kecepatan internet 
        

    except Exception as e:
        # Menangani pengecualian jika terjadi kesalahan selama program berjalan
        print(f"An error occurred: {e}")    
        logging.error(f'Error ketika menjalankan program karena +{e}')
        


   