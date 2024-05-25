# II4031-4 Back End
 Tugas 4 II4031 Kriptografi dan Koding Semester II Tahun 2023/2024

# Pranala Server
https://academic-trascript.azurewebsites.net/docs#/

# Dibuat Oleh
Muhammad Rafi Haidar - 18221134
Raditya Azka Prabaswara - 18221152
 
# Deskripsi
Program ini merupakan aplikasi backend dari aplikasi tugas 4. Program utama menjalankan server Uvicorn dengan framework FastAPI yang dapat diakses di pranala di atas.
Repository juga memuat implementasi algoritma RSA, RC4, dan SHA-3 di direktori cryptography.

# Batasan
- Python 3.12 atau terbaru

# Fitur
Program ini memiliki kemampuan untuk:
a) Membangkitkan kunci publik dan kunci privat RSA;
b) Membangkitan tanda tangan digital (signing) dengan algoritma hash SHA-3 dan RSA;
c) Memverifikasi tanda tangan digital (verifying);
d) Memasukkan data akademik;
e) Mengenkripsi dan mendekripsi field basis data dengan algoritma RC4;
f) Mengenkripsi field basis data yang sudah ditandatangani;
g) Menampilkan isi basis data ke layar (plaintext dan ciphertext);
h) Membuat laporan transkrip akademik setiap mahasiswa dan menyimpan dalam bentuk file PDF yang dienkripsi dengan algoritma AES; dan
i) Mendekripsi file laporan akademik kembali ke format PDF.

# Petunjuk Instalasi
Apabila ingin mengakses server melalui internet tanpa melakukan instalasi kunjungi 
https://academic-trascript.azurewebsites.net/docs

Apabila ingin menjalankan server di mesin lokal:
1. Unduh berkas Zip kode sumber dari repository atau clone repository Github
2. Buka direktori yang sudah berisi kode sumber melalui CLI seperti terminal atau command prompt, atau buka direktori kode sumber di aplikasi IDE seperti Visual Studio Code
3. Unduh semua package python yang digunakan di program ini ketik pada command prompt
   >  pip install -r requirements.txt  
4. Jalankan berkas gui.py, apabila menggunakan command prompt, ketik
   >  python main.py

# Petunjuk Penggunaan
Pada dokumentasi FastAPI:
1. Jalankan endpoint /transcript dengan request GET untuk mendapatkan transkrip yang tidak terenkripsi.
2. Jalankan endpoint /transcript/encrypted dengan request GET untuk mendapatkan transkrip yang terenkripsi, mengecualikan tanda tangan digital.
3. Jalankan endpoint /transcript/encrypted/all dengan request GET untuk mendapatkan transkrip yang terenkripsi.
4. Jalankan endpoint /transcript dengan request POST untuk mendapatkan transkrip yang terenkripsi. Kirim request body sesuai dengan format yang ada di dokumentasi.
5. Jalankan endpoint /key dengan request GET untuk mendapatkan eksponen dan modulus kunci RSA saat ini.
6. Jalankan endpoint /key/generate dengan request GET untuk membangkitkan kuci RSA baru.
7. Jalankan endpoint /signature dengan request POST untuk memvalidasi tanda tangan di transkrip. Kirim request body sesuai dengan format yang ada di dokumentasi.
8. Jalankan endpoint /pdf/encrypted dengan request POST untuk mengunduh berkas PDF transkrip yang terenkripsi. Kirim request body sesuai dengan format yang ada di dokumentasi.
9. Jalankan endpoint /pdf/decrypted dengan request POST untuk mengirim berkas PDF yang dienkripsi dan mengunduh berkas PDF transkrip yang telah didekripsi. Kirim request body sesuai dengan format yang ada di dokumentasi.
