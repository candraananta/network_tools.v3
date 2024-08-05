
import subprocess

def check_connection_with_ping(host, count=1):
    """
    Mengecek koneksi ke host dengan melakukan ping sebanyak 'count' kali.

    Args:
        host (str): Alamat IP atau nama host yang akan diuji.
        count (int, optional): Jumlah ping yang akan dilakukan. Defaults to 20.

    Returns:
        bool: True jika setidaknya satu ping berhasil, False jika semuanya gagal.
    """

    # Gunakan perintah ping dengan opsi -c untuk menentukan jumlah ping
    result = subprocess.run(['ping', '-n', str(count), host], capture_output=True, text=True)

    # Periksa output ping
    if '100% packet loss' in result.stderr:
        return False
    else:
        return True

# Sisanya sama seperti kode sebelumnya...
if __name__ == "__main__":


    ip_addresses = {
        "QAD" : "192.168.150.155",
        "VSS" : "192.168.160.101",
        "System Manager" : "192.168.150.166",
        "M-Files" : "192.168.160.122",
        "HRIS" : "192.168.160.106",
    }

    for name, ip in ip_addresses.items():
        if check_connection_with_ping(ip) == True:
            print(f"Koneksi ke {name} ({ip}) berhasil!")
        else:
            print(f"Gagal terhubung ke {name} ({ip})")

input("tekan enter untuk keluar.....")
