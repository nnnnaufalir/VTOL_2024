import serial.tools.list_ports
import serial


def serial_port_checker():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"{port.device} - {port.description}")


def serial_start():
    # Tentukan port serial yang digunakan ESP32
    # Ubah ini sesuai dengan port ESP32 Anda (misal: '/dev/ttyUSB0' untuk Linux)
    port = 'COM4'
    baud_rate = 57600

    # Membuka komunikasi serial
    ser = serial.Serial(port, baud_rate)

    try:
        while True:
            if ser.in_waiting > 0:  # Jika ada data yang masuk
                data = ser.readline().decode('utf-8').rstrip()
                print(f"Received: {data}")
    except KeyboardInterrupt:
        ser.close()  # Tutup komunikasi serial saat keluar
        print("Serial connection closed.")


# serial_port_checker()
serial_start()
