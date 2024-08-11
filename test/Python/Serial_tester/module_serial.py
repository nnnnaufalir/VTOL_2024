from module_serial import SerialCommunicator
import time

port = "COM4"
baudrate = 57600
serial_comm = SerialCommunicator(port=port, baudrate=baudrate)

# Loop untuk mencoba membuka port serial
while not serial_comm.is_connected:
    try:
        serial_comm.begin()
        if serial_comm.is_connected:
            print(f"Port {port} is successfully opened.")
        else:
            raise Exception("Port is not available")
    except Exception as e:
        print(f"Failed to open port {port}: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)  # Tunggu 5 detik sebelum mencoba lagi

jumlah_data = 5
try:
    while True:
        try:
            serial_comm.flush()
            response = serial_comm.parsing(",", jumlah_data, 500)

            if isinstance(response, list) and len(response) == jumlah_data:
                # Mengambil data sensor
                sensor_depan = response[0]
                sensor_belakang = response[1]
                sensor_kanan = response[2]
                sensor_kiri = response[3]
                sensor_bawah = response[4]

                print(response)
                print(
                    f"Depan :{sensor_depan} | Belakang :{sensor_belakang} | Kanan:{sensor_kanan} | Kiri:{sensor_kiri} | Bawah:{sensor_bawah}")

            else:
                print(f"Received data is incomplete or invalid: {response}")

        except serial_comm.SerialException as e:
            print(f"SerialException: {e}. Attempting to reconnect...")
            serial_comm.reconnect(5000)
            continue

        except PermissionError as e:
            print(f"PermissionError: {e}. Attempting to reconnect...")
            serial_comm.reconnect(5000)
            continue

        except Exception as e:
            print(f"Unexpected error: {e}. Attempting to reconnect...")
            serial_comm.reconnect(5000)
            continue

except KeyboardInterrupt:
    print("Terminated by user")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    serial_comm.end()
