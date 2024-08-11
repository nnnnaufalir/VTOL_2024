import serial
import serial.tools.list_ports
import time


class SerialCommunicator:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.is_connected = False

    def begin(self):
        try:
            if self.ser is None or not self.ser.is_open:
                self.ser = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1
                )
                self.is_connected = True
                print(f"Port {self.port} is open.")
        except serial.SerialException as e:
            print(f"Error initializing serial port: {e}")
            self.ser = None
            self.is_connected = False

    def end(self):
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
                self.is_connected = False
                print(f"Port {self.port} is closed.")
        except serial.SerialException as e:
            print(f"Error closing serial port: {e}")

    def reconnect(self, delay_ms):
        self.end()
        # Tunggu sebentar sebelum mencoba menyambung kembali
        time.sleep(delay_ms/1000)
        self.begin()

    def available(self):
        try:
            return self.ser.in_waiting > 0 if self.ser else False
        except serial.SerialException as e:
            print(f"Error checking data availability: {e}")
            return False

    def write(self, data, delay_ms=None):
        try:
            if self.ser:
                if delay_ms:
                    time.sleep(delay_ms / 1000)
                data = data + "\n"
                self.ser.write(data.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Error writing to serial port: {e}")

    def read(self, delay_ms=None):
        try:
            if self.ser and self.available():
                if delay_ms:
                    time.sleep(delay_ms / 1000)
                raw = self.ser.readline()
                if raw:
                    data = str(raw[:len(raw) - 1])
                    result = data[2:len(data) - 3]
                    return result
            return None
        except serial.SerialException as e:
            print(f"Error reading from serial port: {e}")
            return None

    def parsing(self, separator, count, delay_ms=None):
        try:
            data = self.read(delay_ms)
            if data is None:
                return "No data received"

            warning = "Data is not completed: " + data
            if data.count(separator) == count-1:
                data_receive = data.split(separator)
                return data_receive
            return warning
        except serial.SerialException as e:
            print(f"Error parsing data: {e}")
            return "Parsing error"

    def flush(self):
        try:
            if self.ser:
                self.ser.flush()
        except serial.SerialException as e:
            print(f"Error flushing serial port: {e}")

    def flush_input(self):
        try:
            if self.ser:
                self.ser.flushInput()
        except serial.SerialException as e:
            print(f"Error flushing input buffer: {e}")

    def flush_output(self):
        try:
            if self.ser:
                self.ser.flushOutput()
        except serial.SerialException as e:
            print(f"Error flushing output buffer: {e}")


def serial_port_checker():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"{port.device} - {port.description}")
