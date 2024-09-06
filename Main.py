# Mengimpor modul yang dibutuhkan
import ping3  # Modul untuk mengirim ping ke alamat IP
import time  # Modul untuk menangani waktu, seperti penundaan dan mendapatkan waktu saat ini
import speedtest_cli as speedtest  # Modul untuk mengukur kecepatan internet (download dan upload)
import os  # Modul untuk berinteraksi dengan sistem operasi, misalnya membersihkan layar
import json  # Modul untuk membaca dan menulis data dalam format JSON
import logging  # Modul untuk mencatat log atau pesan debug ke file log atau konsol
import socket  # Modul untuk mendapatkan informasi jaringan seperti alamat IP lokal
import sqlite3  # Modul untuk berinteraksi dengan database SQLite, menyimpan dan mengambil data hasil tes
import pandas as pd # Modul untuk memanipulasi data





# fungsi untuk membuat text berwarna dan memiliki style
from colorama import init, Fore, Style
init()
biru = Fore.BLUE
merah = Fore.RED
kuning = Fore.YELLOW

tebal = Style.BRIGHT

resetstyle = Style.RESET_ALL


# Membuat koneksi ke database SQLite dan membuat objek cursor untuk eksekusi query SQL
try:
    conn = sqlite3.connect('database.db')  # Membuka atau membuat database bernama 'networks.db'
    cursor = conn.cursor()  # Membuat cursor untuk mengeksekusi perintah SQL di database
except Exception as e:
    # Menangani pengecualian jika gagal membuat koneksi ke database
    print(f"Error {e}")  # Mencetak pesan error ke konsol

# Mengkonfigurasi logging untuk mencatat log ke file 'network.monitor.log'
logging.basicConfig(
    filename='network.monitor.log',  # Nama file tempat log akan disimpan
    level=logging.INFO,  # Level log yang dicatat, INFO dan lebih tinggi
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format pesan log dengan timestamp, level, dan pesan log
)

# CREATE TABLE
try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS speedtest_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            test_time TEXT,  
            server_found TEXT, 
            located_in TEXT,
            download REAL,  
            upload REAL)''')
        # Membuat tabel speedtest_result jika belum ada
        cursor.execute('''CREATE TABLE IF NOT EXISTS networks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            test_time TEXT,  
            local_ip TEXT, 
            ip_address TEXT, 
            status TEXT,  
            rtt TEXT)''')  
except Exception as e:
        # Menangani pengecualian jika gagal membuat table
        print(f"Terjadi kesalahan dalam membuat table speedtest_result : {e}")  # Mencetak pesan error ke konsol
        logging.error(f"Error creating table : {e}")  # Mencatat error ke file log

# MENYIMPAN KE DALAM TABLE SPEEDTEST_RESULTS
def menyimpan_ke_database_speedtest_results(test_time,server_found,located_in,download,upload):
    try:
        # Memasukkan data hasil tes ke dalam tabel
        cursor.execute(
            "INSERT INTO speedtest_results (test_time, server_found, located_in, download, upload) VALUES (?,?,?,?,?)",
            (test_time,server_found, located_in, download, upload)
        )
        # Menyimpan perubahan ke database
        conn.commit()
        print("Data hasil speedtest berhasil disimpan ke database!")  # Memberi tahu pengguna bahwa data telah disimpan
        logging.info("Data hasil speedtes berhasil disimpan ke database")  # Mencatat informasi ke file log
    except Exception as e:
        print(f"Tejadi kesalahan : {e}")
        logging.error(f"Error saving data to database : {e}")  # Mencatat error ke file log

# MENYIMPAN KE DALAM TABLE NETWORKS
def menyimpan_ke_database(test_time, local_ip, ip_address, status, rtt):
    try:
        # Memasukkan data hasil tes ke dalam tabel
        cursor.execute(
            "INSERT INTO networks (test_time,local_ip,ip_address,status,rtt) VALUES (?,?,?,?,?)",
            (test_time, local_ip, ip_address, status, rtt)
        )

        # Menyimpan perubahan ke database
        conn.commit()
        print("Data berhasil disimpan ke database!")  # Memberi tahu pengguna bahwa data telah disimpan
        logging.info("Data hasil tes berhasil disimpan ke database")  # Mencatat informasi ke file log
    except Exception as e:
        # Menangani pengecualian jika terjadi kesalahan saat menyimpan data
        print(f"Terjadi kesalahan : {e}")  # Mencetak pesan error ke konsol
        logging.error(f"Error saving data to database : {e}")  # Mencatat error ke file log

# Fungsi untuk mendapatkan alamat IP lokal dari komputer
def mendaptakan_ip_local():
    try:
        # Mendapatkan nama host komputer
        hostname = socket.gethostname()
       
        # Mendapatkan alamat IP yang terkait dengan nama host
        lokal_ip = socket.gethostbyname(hostname)
        return lokal_ip  # Mengembalikan alamat IP lokal
    except Exception as e:
        # Menangani pengecualian jika gagal mendapatkan alamat IP
        logging.error(f"Error getting local IP : {e}")  # Mencatat error ke file log
        return None  # Mengembalikan None jika terjadi kesalahan
    

# Fungsi untuk membaca konfigurasi dari file JSON
def read_config(config_file):
    try:
        # Membuka file konfigurasi JSON dalam mode baca
        with open(config_file, 'r') as f:
            config = json.load(f)  # Membaca file dan mengonversi JSON ke dictionary Python
            logging.info(f"Configuration loaded from {config_file}")  # Mencatat informasi ke file log
        return config  # Mengembalikan konfigurasi yang telah dibaca
    except FileNotFoundError as e:
        # Menangani pengecualian jika file tidak ditemukan
        logging.error(f"Error reading configuration file : {e}")  # Mencatat error ke file log
        print(f"Error: {e}")  # Mencetak pesan error ke konsol
        return None  # Mengembalikan None jika terjadi kesalahan

# Fungsi untuk menampilkan pesan selamat datang dan informasi aplikasi
def welcome_message():
    logging.info("Displaying welcome message")  # Mencatat informasi ke file log
    print("\n==================================================")  # Garis pemisah
    print(tebal + biru + "---------------USER NETWORK TOOLS------------------" + resetstyle)  # Judul aplikasi
    print("====================================================")
    print(f"Waktu Pengecekan: {biru}{time.strftime('%A, %d %B %Y %H:%M:%S')}{resetstyle}")  # Menampilkan waktu saat ini
    print("----------------------------------------------------\n")  # Garis pemisah
    print("")

    
# Fungsi untuk mengirimkan ping ke alamat IP dan mengembalikan waktu respons
def ping(ip,timeout=10):
    try:
        response = ping3.ping(ip)  # Mengirim ping ke alamat IP yang diberikan
        if response:
            return response  # Mengembalikan waktu respons jika ping berhasil
        else:
            return None  # Mengembalikan None jika ping gagal
        logging.info(f"Ping to {ip} {'Succeeded' if response else 'failed'}")  # Mencatat hasil ping ke file log
    except Exception as e:
        # Menangani pengecualian jika ping gagal
        logging.error(f"Failed to ping {ip} : {str(e)}")  # Mencatat error ke file log
        return False  # Mengembalikan False jika terjadi kesalahan
    
# Fungsi untuk menguji kecepatan internet (download dan upload)
def test_internet_speed():
    try:
        st = speedtest.Speedtest(secure=True)  # Membuat objek Speedtest dengan HTTPS untuk mengukur kecepatan internet
        logging.info('Testing internet speed')  # Mencatat informasi ke file log
        print("Testing internet speed...Mohon menunggu...")  # Memberi tahu pengguna bahwa tes sedang berjalan

        st.get_best_server()  # Mendapatkan server terbaik berdasarkan lokasi geografis pengguna
        best = st.get_best_server()  # Menyimpan informasi tentang server terbaik dalam variabel

        download_speed = st.download() / 1000000  # Mengukur kecepatan download dan mengonversinya ke Mbps
        upload_speed = st.upload() / 1000000  # Mengukur kecepatan upload dan mengonversinya ke Mbps
        dwspeed = round(download_speed,2) #round adalah fungsi untuk membulatkan angka. keterangan 2 adalah 2 angka dibelakang koma
        upspeed = round(upload_speed,2)

        # Menampilkan hasil tes kecepatan internet ke konsol
        print("----------------------------------------------------")
        print(f"**** {merah + tebal}Download Speed:{resetstyle}======>> {kuning }{dwspeed}{resetstyle} Mbps")
        print(f"**** {merah + tebal}Upload Speed:{resetstyle}======>> {kuning }{upspeed}{resetstyle} Mbps")
        print("----------------------------------------------------")
        print(f"Found: {best['host']} -- Located in {best['country']}")  # Menampilkan informasi tentang server terbaik
        print("----------------------------------------------------")
        logging.info(f"Internet speed test results - Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps")  # Mencatat hasil tes ke file log

        # Menyimpan hasil tes kecepatan internet ke database
        test_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Mendapatkan waktu saat ini dalam format YYYY-MM-DD HH:MM:SS
        menyimpan_ke_database_speedtest_results(test_time, best['host'], best['country'], dwspeed,upspeed)  # Memanggil fungsi menyimpan ke database
        return download_speed, upload_speed  # Mengembalikan kecepatan download dan upload
        print("data speedtest berhasil disimpan ke datababase")
        logging.info("data speedtest berhasil disimpan ke database")          
    
    except speedtest.SpeedtestException as e:
        # Menangani pengecualian jika tes kecepatan gagal
        logging.error(f"Error during the speed test: {str(e)}")  # Mencatat error ke file log
        print(f"Gagal Melakukan speed test karena : {str(e)}")  # Mencetak pesan error ke konsol
        print(f"An error occurred during the speed test: {str(e)}")  # Mencetak pesan error ke konsol


# Fungsi untuk memeriksa status jaringan untuk daftar alamat IP
def check_network(ip_list, counter=10):
    
    try:
        nomer = 0 # untuk nomer urut
        for ip_config in ip_list:
            alamat_ip = ip_config['ip']  # Mendapatkan alamat IP dari konfigurasi
            nama_ip = ip_config['name']  # Mendapatkan nama IP dari konfigurasi
            gagal = 0  # Menghitung jumlah ping yang gagal
            berhasil = 0  # Menghitung jumlah ping yang berhasil
            rtt_total = 0  # Menghitung total waktu respons untuk rata-rata waktu   
            rata_rtt = 0
            nomer == 0 #untuk mengembalikan nilai nomer ke 0

            for _ in range(counter):  # Mengirim ping sejumlah counter kali
                rtt = ping(alamat_ip)  # Mengirim ping dan mendapatkan waktu respons
                time.sleep(0.25) #untuk mengulur waktu
                persen_berhasil = (berhasil/counter) * 100

                if rtt:  # Jika ping berhasil
                    berhasil += 1  # Menambah jumlah ping yang berhasil
                    rtt_total += rtt  # Menambah waktu respons ke total
                    # status = "reachable"
                    logging.info(f"{nama_ip} ({alamat_ip}) Connection is good : {rtt:.2f} ms")  # Mencatat informasi ke file log
                else:  # Jika ping gagal
                    gagal += 1  # Menambah jumlah ping yang gagal
                    logging.warning(f"{nama_ip} ({alamat_ip}) Connection failed")  # Mencatat peringatan ke file log

            persen_berhasil = (berhasil/counter) * 100 #menghitung jumlag persen berhasil

            nomer += 1 #menambahkan jumlah nomor urut
            # if berhasil == counter:  # Jika lebih banyak ping yang berhasil
            if persen_berhasil == 100:
                rata_rtt = rtt_total / berhasil  # Menghitung rata-rata waktu respons
                status = f"NO. {nomer} ==>{kuning + tebal}{nama_ip}{resetstyle} {merah}({alamat_ip} {resetstyle}) {biru + tebal}Koneksi ke {nama_ip} SANGAT BAIK !! {resetstyle} Time avg: ({rata_rtt:.2f}) ms"  # Status koneksi berhasil
                status_untuk_disimpandatabase =  f"NO. {nomer} ==> {nama_ip} {alamat_ip} Koneksi ke {nama_ip} TERHUBUNG !! Time: ({rata_rtt:.2f}) ms"
                status_jumlah_ping = (f"dilakukan ping sebanyak {counter}") #menampilkan jumlag ping counter = 4
                status_ping_berhasil = (f"Jumlah ping berhasil = {berhasil}") # menampilkan jumlah ping yang berhasil
                status_ping_gagal = (f"Jumlah ping gagal = {gagal}") # menampilkan jumlah ping yang gagal
                status_avg_waktu_ping = (f"Rata - rata waktu ping dari {counter} percobaan = ({rata_rtt:.2f}) milisecond") #menampilkan rata-rata waktu
                status_persen_berhasil = persen_berhasil
                logging.info(status)  # Mencatat informasi ke file log
            # elif berhasil == counter:  # Jika ping gagal
            # elif berhasil < counter and berhasil > 0 : #kondisi jika jaringan putus - putus
            elif persen_berhasil > 80 :
                rata_rtt = rtt_total / berhasil
                # status = f"NO. {nomer} ==>{kuning + tebal}{nama_ip}{resetstyle} {merah}({alamat_ip} {resetstyle}) {merah + tebal}Koneksi ke {nama_ip} DOWN !! {resetstyle} RTT: {rata_rtt} ms
                status = f"NO. {nomer} ==>{kuning + tebal}{nama_ip}{resetstyle} {merah}({alamat_ip} {resetstyle}) {kuning + tebal}Koneksi ke {nama_ip} CUKUP BAIK ! {resetstyle} Time avg: {rata_rtt:.2f} ms" 
                status_untuk_disimpandatabase =  f"NO. {nomer} ==> {nama_ip} {alamat_ip} Koneksi ke {nama_ip} DOWN !! Time: {rata_rtt} ms"
                status_jumlah_ping = (f"dilakukan ping sebanyak {counter}") #menampilkan jumlag ping counter = 4
                status_ping_berhasil = (f"Jumlah ping berhasil = {berhasil}") # menampilkan jumlah ping yang berhasil
                status_ping_gagal = (f"Jumlah ping gagal = {gagal}") # menampilkan jumlah ping yang gagal
                status_avg_waktu_ping = (f"Rata - rata waktu ping dari {counter} percobaan = {rata_rtt} milisecond") #menampilkan rata-rata waktu
                status_persen_berhasil = persen_berhasil
                logging.warning(status)  # Mencatat informasi ke file log
            elif persen_berhasil > 50 :
                rata_rtt = rtt_total / berhasil
                # status = f"NO. {nomer} ==>{kuning + tebal}{nama_ip}{resetstyle} {merah}({alamat_ip} {resetstyle}) {merah + tebal}Koneksi ke {nama_ip} DOWN !! {resetstyle} RTT: {rata_rtt} ms
                status = f"NO. {nomer} ==>{kuning + tebal}{nama_ip}{resetstyle} {merah}({alamat_ip} {resetstyle}) {kuning + tebal}Koneksi ke {nama_ip} KURANG BAIK ! {resetstyle} Time avg: {rata_rtt:.2f} ms" 
                status_untuk_disimpandatabase =  f"NO. {nomer} ==> {nama_ip} {alamat_ip} Koneksi ke {nama_ip} DOWN !! Time: {rata_rtt} ms"
                status_jumlah_ping = (f"dilakukan ping sebanyak {counter}") #menampilkan jumlag ping counter = 4
                status_ping_berhasil = (f"Jumlah ping berhasil = {berhasil}") # menampilkan jumlah ping yang berhasil
                status_ping_gagal = (f"Jumlah ping gagal = {gagal}") # menampilkan jumlah ping yang gagal
                status_avg_waktu_ping = (f"Rata - rata waktu ping dari {counter} percobaan = {rata_rtt} milisecond") #menampilkan rata-rata waktu
                status_persen_berhasil = persen_berhasil
                logging.warning(status)  # Mencatat informasi ke file log
            else:  # Jika lebih banyak ping yang gagal
                rata_rtt = 'timeout'
                # status = f"NO. {nomer} ==>{kuning + tebal}{nama_ip}{resetstyle} {merah}({alamat_ip} {resetstyle}) {kuning + tebal}Koneksi ke {nama_ip} PUTUS-PUTUS ! {resetstyle} RTT: ({rata_rtt:.2f}) ms" 
                status = f"NO. {nomer} ==>{kuning + tebal}{nama_ip}{resetstyle} {merah}({alamat_ip} {resetstyle}) {merah + tebal}Koneksi ke {nama_ip} BURUK ! {resetstyle} Time avg: ({rata_rtt}) ms" 
                status_untuk_disimpandatabase =  f"NO. {nomer} ==> {nama_ip} {alamat_ip} Koneksi ke {nama_ip} PUTUS-PUTUS !! Time: ({rata_rtt}) ms"
                status_jumlah_ping = (f"dilakukan ping sebanyak {counter}") #menampilkan jumlag ping counter = 4
                status_ping_berhasil = (f"Jumlah ping berhasil = {berhasil}") # menampilkan jumlah ping yang berhasil
                status_ping_gagal = (f"Jumlah ping gagal = {gagal}") # menampilkan jumlah ping yang gagal
                status_avg_waktu_ping = (f"Rata - rata waktu ping dari {counter} percobaan = {rata_rtt} milisecond") #menampilkan rata-rata waktu
                status_persen_berhasil = persen_berhasil
                logging.warning(status)  # Mencatat informasi ke file log
                

            # Menampilkan status ke konsol
            print("----------------------------------------------------------------")
            print(status)
            # print("\n")
            # print(status_jumlah_ping)
            # print(status_ping_berhasil)
            # print(status_ping_gagal)
            # print(status_avg_waktu_ping)
            print(f"Persentase koneksi yang berhasil: {status_persen_berhasil}%")

            #persiapan menyimpan ke database
            test_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Mendapatkan waktu saat ini dalam format YYYY-MM-DD HH:MM:SS
            local_ip = mendaptakan_ip_local()  # Mendapatkan alamat IP lokal
            menyimpan_ke_database(test_time, local_ip, alamat_ip, status_untuk_disimpandatabase, rata_rtt)  # Menyimpan hasil tes ke database

        print('\n')
        print("---Uji koneksi jaringan selesai---")  # Memberi tahu pengguna bahwa uji koneksi selesai
    except Exception as e:
        # Menangani pengecualian jika terjadi kesalahan selama pemeriksaan jaringan
        print(f"Terjadi kesalahan1: {str(e)}")  # Mencetak pesan error ke konsol
        logging.error(f"Network check error: {str(e)}")  # Mencatat error ke file log


# Fungsi utama yang dijalankan ketika program dimulai
def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar konsol (cls untuk Windows, clear untuk Unix)
        lokal_ip = mendaptakan_ip_local()
        print(f"##############--Your IP Address is  = {kuning}{lokal_ip}{resetstyle} --##############")
        print('\n')

        config = read_config('config.json')  # Membaca konfigurasi dari file 'config.json'
        if not config:  # Jika konfigurasi tidak berhasil dibaca
            print("Konfigurasi tidak ditemukan atau gagal dibaca.")  # Menampilkan pesan error
            return  # Keluar dari fungsi utama

        ip_list = config.get('ip_addresses')  # Mendapatkan daftar IP dari konfigurasi
        if not ip_list:  # Jika daftar IP tidak ditemukan dalam konfigurasi
            print("Daftar IP tidak ditemukan dalam konfigurasi.")  # Menampilkan pesan error
            return  # Keluar dari fungsi utama
        
        ip_list_device = config.get('IP_address_device')  # Mendapatkan daftar IP dari konfigurasi
        if not ip_list_device:  # Jika daftar IP tidak ditemukan dalam konfigurasi
            print("Daftar IP tidak ditemukan dalam konfigurasi.")  # Menampilkan pesan error
            return  # Keluar dari fungsi utama
        
        check_network(ip_list)  # Memeriksa status jaringan untuk setiap IP dalam daftar
        # check_network(ip_list_device)  # Memeriksa status jaringan untuk setiap IP dalam daftar
         # Menjalankan tes kecepatan internet jika diaktifkan dalam konfigurasi
        test_internet_speed()

    except Exception as e:
        # Menangani pengecualian jika terjadi kesalahan selama eksekusi program
        print(f"Terjadi kesalahan: {str(e)}")  # Mencetak pesan error ke konsol
        logging.error(f"An error occurred in the main function: {str(e)}")  # Mencatat error ke file log

# Menjalankan fungsi utama jika script dieksekusi secara langsung
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Membersihkan layar konsol (cls untuk Windows, clear untuk Unix)
    while True:
        try:
            print("\n")
            welcome_message()
            print("--Silahkan pilih untuk menjalankan--")
            print("1. Check Koneksi aplikasi AKR")
            print("2. Tampilkan List IP yang ada di Nilam Utara")
            print("3. Keluar")

            inp = int(input("Masukan pilihan anda : "))

            if inp == 1:
                main()  # Jalankan fungsi utama
            # time.sleep(60)  # Tunggu 1 menit sebelum melakukan ulang uji koneksi
            elif inp == 2:
                try:
                    config = read_config('config.json')
                    #ambil data IP_adress_device
                    ip_data = config['IP_address_device']
                    #buat data frame panda
                    df = pd.DataFrame(ip_data) #data frame
                    print(df)
                    logging.info("membaca menu nomor 2 dan berhasil menampilkan data IP address")
                except Exception as e:
                    print(f"Terjadi kesalahan: {str(e)}")  # Mencetak pesan error ke konsol
                    logging.error(f"An error occurred in the main function: {str(e)}")  # Mencatat error ke file log

            elif inp==3:
                break #
            else:
                print("Pilihan yang anda masukkan salah.")
                  # Menampilkan pesan error jika pilihan salah
        except KeyboardInterrupt:
            break  # Keluar jika user menekan Ctrl+C

