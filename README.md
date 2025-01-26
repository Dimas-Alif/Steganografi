# Steganografi 

Proyek ini adalah implementasi steganografi multiformat yang dapat menyembunyikan pesan atau data ke dalam gambar, audio, dan video. Proyek ini mendukung berbagai format file dan memberikan kapasitas yang lebih besar dalam menyembunyikan pesan. Selain itu, proyek ini juga dilengkapi dengan fitur-fitur tambahan seperti notifikasi email, logging, dan pengamanan terhadap deteksi steganalisis dasar.

## Fitur Utama

- **Menyembunyikan pesan dalam berbagai format**: Gambar (PNG), Audio (WAV), dan Video (AVI/XVID).
- **Peningkatan kapasitas**: Memungkinkan untuk menyembunyikan pesan lebih besar dalam file media.
- **Pengamanan terhadap deteksi steganalisis**: Menggunakan teknik kompresi dan enkripsi untuk mengurangi kemungkinan deteksi.
- **Notifikasi Email**: Mengirimkan email peringatan saat pesan berhasil disembunyikan.
- **Logging**: Menyediakan log rinci untuk setiap aktivitas steganografi yang dilakukan.
- **CLI Automation**: Mendukung penggunaan command-line untuk memudahkan pengguna dalam mengautomasi proses steganografi.
- **Pemantauan Real-time**: Menyediakan informasi status proses steganografi secara langsung.

## Instalasi

Untuk menjalankan proyek ini, Anda memerlukan beberapa dependensi. Anda dapat menginstalnya dengan menggunakan `pip`:

    pip install opencv-python pillow numpy

## Penggunaan

### Encoding Pesan (Menambahkan pesan ke dalam file media)
Untuk menyembunyikan pesan dalam gambar, audio, atau video, gunakan perintah berikut:
- Menyembunyikan pesan dalam gambar:
```
python steganography.py encode_image input_image.png output_image.png "Pesan tersembunyi."
```
- Menyembunyikan pesan dalam audio:
```
python steganography.py encode_audio input_audio.wav output_audio.wav "Pesan tersembunyi untuk audio."
```
- Menyembunyikan pesan dalam video:
```
python steganography.py encode_video input_video.avi output_video.avi "Pesan tersembunyi dalam video."
```

### Decoding Pesan (Mengambil pesan yang tersembunyi)
Untuk mengekstrak pesan tersembunyi dari gambar, audio, atau video, gunakan perintah berikut:
- Mengambil pesan dari gambar:
```
python steganography.py decode_image output_image.png
```
- Mengambil pesan dari audio:
```
python steganography.py decode_audio output_audio.wav
```
- Mengambil pesan dari video:
```
python steganography.py decode_video output_video.avi
```

## Kelemahan dan Peningkatan yang Diperlukan
Meskipun proyek ini menawarkan banyak fitur canggih, ada beberapa kelemahan yang perlu diperhatikan:

1. Keterbatasan Kapasitas Penyimpanan:
Meski telah ada peningkatan kapasitas, file media tertentu (terutama gambar dengan resolusi rendah atau audio dengan durasi pendek) memiliki batasan dalam menyembunyikan pesan besar.

2. Steganalisis yang Lebih Lanjut:
Teknik yang digunakan untuk menyembunyikan pesan (termasuk kompresi dan enkripsi) mungkin masih rentan terhadap steganalisis yang lebih canggih. Misalnya, analisis statistik tingkat lanjut bisa saja mendeteksi pola yang tidak biasa dalam media yang telah dimodifikasi.

4. Keterbatasan Format dan Kompresi:
Format yang didukung terbatas pada PNG, WAV, dan AVI/XVID. Selain itu, algoritma kompresi yang digunakan dapat menyebabkan degradasi kualitas file media, meskipun ini lebih terlihat pada format gambar atau video dengan kualitas tinggi.

4. Keamanan Kata Sandi:
Kata sandi yang digunakan untuk autentikasi email tidak terenkripsi dalam kode. Sebaiknya menggunakan metode penyimpanan kata sandi yang lebih aman (misalnya, environment variables atau pengelola kata sandi) agar tidak terbuka dalam kode.

5. Keamanan dalam Penggunaan Email:
Penggunaan kredensial email dalam kode memungkinkan potensi penyalahgunaan jika tidak dikelola dengan baik. Sebaiknya menghindari hardcoding informasi sensitif.

6. Keterbatasan Platform dan Dependensi:
Proyek ini bergantung pada beberapa pustaka eksternal yang mungkin tidak sepenuhnya kompatibel dengan sistem operasi atau versi Python tertentu. Pengguna perlu memastikan bahwa pustaka-pustaka ini dapat diinstal dengan benar di sistem mereka.

## Kontribusi
Jika Anda ingin berkontribusi pada proyek ini, silakan buat pull request. Semua kontribusi, baik itu bug fix, fitur baru, atau perbaikan dokumentasi, akan sangat dihargai.
