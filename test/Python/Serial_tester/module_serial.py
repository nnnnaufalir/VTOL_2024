import serial
import time
import zlib
import logging

logging.basicConfig(level=logging.DEBUG)


class SerialCommunicator:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.sequence_number = 0
        self._connect()

    def _connect(self):
        """Mencoba membuka koneksi serial. Akan retry setiap 5 detik jika gagal."""
        while True:
            try:
                self.ser = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1
                )
                logging.info("Serial connection established.")
                return
            except serial.SerialException as e:
                logging.error(f"Failed to open serial port: {e}")
                logging.info("Retrying in 5 seconds...")
                time.sleep(5)

    def begin(self):
        """Memastikan koneksi serial terbuka."""
        if self.ser is None or not self.ser.is_open:
            self._connect()

    def end(self):
        """Menutup koneksi serial jika terbuka."""
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
            logging.info("Serial connection closed.")

    def available(self):
        """Memeriksa apakah ada data yang tersedia untuk dibaca."""
        return self.ser.in_waiting > 0

    def compute_crc(self, data):
        """Menghitung CRC32 untuk data yang diberikan."""
        return zlib.crc32(data.encode('utf-8')) & 0xFFFFFFFF

    def verify_crc(self, data, received_crc):
        """Memverifikasi CRC dari data yang diterima."""
        return self.compute_crc(data) == received_crc

    def write(self, data, delay_ms=0):
        """Menulis data ke serial dengan sequence number dan CRC."""
        if self.ser is None or not self.ser.is_open:
            self._connect()
        time.sleep(delay_ms / 1000)
        data_to_send = f"{self.sequence_number},{data}"
        crc = self.compute_crc(data_to_send)
        full_message = f"{data_to_send},{crc}\n"
        self.ser.write(full_message.encode('utf-8'))
        logging.info(f"Sent: {full_message.strip()}")
        self.sequence_number += 1

    def read(self, delay_ms=0):
        """Membaca data dari serial dengan pengecekan CRC dan sequence number."""
        if self.ser is None or not self.ser.is_open:
            self._connect()
        if self.available():
            time.sleep(delay_ms / 1000)
            try:
                raw_data = self.ser.readline()  # Baca data mentah
                logging.debug(f"Raw data received (bytes): {raw_data}")
                # Coba decode data dengan UTF-8
                decoded_data = raw_data.decode('utf-8').strip()
                logging.debug(f"Decoded data: {decoded_data}")
                data_parts = decoded_data.split(',')

                if len(data_parts) > 2:
                    try:
                        received_seq = int(data_parts[0])
                        data = ','.join(data_parts[1:-1])
                        received_crc = int(data_parts[-1])

                        if self.verify_crc(f"{received_seq},{data}", received_crc):
                            ack_message = f"ACK,{received_seq}\n"
                            self.ser.write(ack_message.encode('utf-8'))
                            logging.info(
                                f"Received: {decoded_data}, Sent ACK: {ack_message.strip()}")
                            return data
                        else:
                            logging.error(
                                f"CRC check failed for message: {decoded_data}")
                    except ValueError as e:
                        logging.error(f"Error parsing message: {e}")
                else:
                    logging.error(
                        f"Incomplete message received: {decoded_data}")
            except UnicodeDecodeError as e:
                logging.error(f"Unicode decode error: {e}")
        return None

    def write_with_ack(self, data, delay_ms=0, retries=3):
        """Menulis data ke serial dan menunggu ACK."""
        for attempt in range(retries):
            self.write(data, delay_ms)
            ack = self.read(delay_ms)
            if ack and "ACK" in ack:
                logging.info(
                    f"ACK received for sequence number {self.sequence_number - 1}")
                return True
            else:
                logging.warning(
                    f"No ACK received, retrying... ({attempt + 1}/{retries})")
                self._connect()  # Coba sambungkan kembali jika tidak ada ACK
        logging.error("Failed to receive ACK after retries.")
        return False

    def flush(self):
        """Flush semua data dari buffer serial."""
        if self.ser is not None and self.ser.is_open:
            self.ser.flush()

    def flush_input(self):
        """Flush input buffer serial."""
        if self.ser is not None and self.ser.is_open:
            self.ser.reset_input_buffer()

    def flush_output(self):
        """Flush output buffer serial."""
        if self.ser is not None and self.ser.is_open:
            self.ser.reset_output_buffer()
