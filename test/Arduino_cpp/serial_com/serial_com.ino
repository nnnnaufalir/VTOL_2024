
// Fungsi CRC32 sederhana
unsigned long crc32(const byte *data, size_t length) {
    unsigned long crc = 0xFFFFFFFF;
    for (size_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1) {
                crc = (crc >> 1) ^ 0xEDB88320;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFF;
}

void setup() {
  Serial.begin(57600);
  delay(1000);
}

void loop() {
  String message = "Hello World";
  static int sequence_number = 0; // Gunakan variabel static untuk menyimpan sequence number
  String data_to_send = String(sequence_number) + "," + message;

  // Hitung CRC untuk data
  unsigned long crc = crc32((const byte *)data_to_send.c_str(), data_to_send.length());
  
  // Kirim data dengan CRC
  String full_message = data_to_send + "," + String(crc) + "\n";
  Serial.print(full_message);
  
  // // Debug print
  // Serial.println("Sent: " + full_message);
  
  // Incremen sequence number untuk pesan berikutnya
  sequence_number++;
  
  delay(1000);  // Tunggu 1 detik sebelum mengirim data lagi
}

