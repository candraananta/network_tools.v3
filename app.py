# Menginport module flask, jsonify dan request dari flask untuk membuat API
from flask import Flask, jsonify, request
import sqlite3 # module sqlite3 untuk berinteraksi dengan database SQlite
import logging # Module logging untuk mencatat aplikasi ( activities)

# Inisialisasi aplikasi flask module
app = Flask(__name__)

# Konfigurasi logging untuk mencatat aktivitas aplikasi

logging.basicConfig(filename='api.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Membuat koneksi ke database
def get_database_connection():
  try:
    conn = sqlite3.connect('database.db') #membuat koneksi ke database.db
    conn.row_factory = sqlite3.Row # Mengatur row factory untuk mengakses data dalam bentuk dictionary
    logging.info('Database connection successfully')
    return conn # mengembalikan object koneksi
  except Exception as e:
    logging.error(f"Error creating connection: {e}") # menulis log error
    return None # mengembalikan None jika gagal membuat koneksi
  
@app.route('/')
def home():
    return "Hello, World!"  # Mengembalikan respon sederhana
    logging.info('success read router home')

# Mendefinisikan endpoints untuk mendapatkan semua hasil speedtest
@app.route('/api/speedtest_result', methods=['GET'])
def get_speedtest_results():
      conn = get_database_connection() # Mendapatkan koneksi ke database
      if not conn:
        logging.error('koneksi get api gagal')
        return jsonify('Error : Database connection failed '), 500 # Mengembalikan errror jika koneksi gagal

      cursor = conn.cursor() # Membuat cursor untuk menjalankan query
      cursor.execute("SELECT * FROM speedtest_results") # Memilih semua data pada table speedtest_results
      results = cursor.fetchall() # mengambil semua querry
      logging.info("Speedtest results api read")

      conn.close() # Menutup koneksi database

      #Mengembalikan hasil dalam format JSON
      '''
      Mengubah hasil query menjadi format JSON dan mengembalikannya sebagai respons.
      [dict(row) for row in results]: List comprehension untuk mengubah setiap tuple dalam results menjadi dictionary, sehingga lebih mudah dikonversi menjadi JSON.
      '''
      return jsonify([dict(row) for row in results])
# Mendefinisikan endpoint untuk menambahkan hasil speedtest
      
# Menjalankan aplikasi flask di port 5000
if __name__ == '__main__':
     app.run(debug=True) # Menjalankan server dengan mode debug diaktifkan




