# VTOL_2024
VTOL KRTI 2024 


# Arduino Program 
## Sensor ToF VL53L1X dengan Arduino
Program ini menggunakan lima sensor VL53L1X untuk mengukur jarak ke objek di lima arah berbeda (depan, belakang, kanan, kiri, dan bawah). Jarak yang diukur kemudian dikirimkan ke komputer melalui komunikasi serial dalam format CSV (Comma-Separated Values).

## Persyaratan
<br>Arduino (misalnya, Arduino Uno, Nano, atau yang kompatibel)<br/>
Lima sensor VL53L1X<br/>
Library Adafruit_VL53L1X<br/>
Kabel jumper<br/>
Resistor jika diperlukan untuk pengaturan I2C yang benar</br>

## Pinout
Setiap sensor terhubung ke pin XSHUT yang berbeda untuk memungkinkan pengaturan alamat I2C yang unik:
Depan: Pin 2 (XSHUT_FRONT)
Belakang: Pin 14 (XSHUT_BACK)
Kanan: Pin 4 (XSHUT_RIGHT)
Kiri: Pin 5 (XSHUT_LEFT)
Bawah: Pin 12 (XSHUT_BOTTOM)

## Alamat I2C
Setiap sensor diberi alamat I2C yang unik:
<br>Depan: 0x30
<br>Belakang: 0x31
<br>Kanan: 0x32
<br>Kiri: 0x33
<br>Bawah: 0x34

## Fitur Utama
<br>Inisialisasi Sensor: Masing-masing sensor diinisialisasi dengan XSHUT pin untuk mengatur alamat I2C yang unik.
<br>Pengukuran Jarak: Program menggunakan buffer untuk menyimpan pembacaan jarak terbaru dan menghitung rata-rata jarak untuk mengurangi noise.
<br>Pengiriman Data: Jarak dari lima sensor dikirim melalui komunikasi serial dataSend(data_0,data_1,data_2,data_3,data_4).

## Menghubungkan Sensor
Hubungkan sensor VL53L1X ke Arduino sesuai dengan pin yang telah ditentukan:
<br>Sensor depan (Front): Pin 2 (XSHUT_FRONT)
<br>Sensor belakang (Back): Pin 14 (XSHUT_BACK)
<br>Sensor kanan (Right): Pin 4 (XSHUT_RIGHT)
<br>Sensor kiri (Left): Pin 5 (XSHUT_LEFT)
<br>Sensor bawah (Bottom): Pin 12 (XSHUT_BOTTOM)

## 3. Membaca Data
Data jarak akan dikirimkan ke komputer melalui port serial dengan format CSV sebagai berikut:
<pre>
data_0,data_1,data_2,data_3,data_4
</pre>
Dimana:
<br>data_0: Jarak sensor depan
<br>data_1: Jarak sensor belakang
<br>data_2: Jarak sensor kanan
<br>data_3: Jarak sensor kiri
<br>data_4: Jarak sensor bawah

# Catatan
<br>Timing Budget: Timing budget dari sensor diatur menggunakan konstanta TIMING, yang dapat diubah untuk menyesuaikan kecepatan pembacaan jarak.
<br>Buffer Size: Ukuran buffer diatur menggunakan konstanta BUFFER_SIZE, yang digunakan untuk menyimpan dan merata-rata pembacaan jarak untuk mengurangi noise.
<br>Dokumentasi ini dapat digunakan sebagai panduan untuk memahami dan menggunakan program Arduino yang mengukur jarak dengan sensor VL53L1X dan mengirimkan data ke komputer melalui serial.

