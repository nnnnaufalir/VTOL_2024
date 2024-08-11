from module_serial import SerialCommunicator
import logging

logging.basicConfig(level=logging.DEBUG)  # Ubah level log menjadi DEBUG

# Ganti '/dev/ttyUSB0' dengan port yang sesuai untuk sistem Anda
port = 'COM4'
baudrate = 57600

# Buat instance dari SerialCommunicator
communicator = SerialCommunicator(port, baudrate)

try:
    while True:
        # Baca data dari ESP32
        data = communicator.read(delay_ms=50)

        if data:
            logging.info(f"Data received: {data}")
        else:
            logging.warning("No data received or failed to verify.")
except KeyboardInterrupt:
    print("Terminating program...")
finally:
    communicator.end()
