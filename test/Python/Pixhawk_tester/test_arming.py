from dronekit import connect, VehicleMode
import time


def arm_drone(vehicle):
    print("Checking pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Motors are armed!")


def main():
    try:
        # Koneksi ke Pixhawk melalui serial port
        print("Connecting to Pixhawk")
        vehicle = connect('/dev/ttyACM0', baud=921600, wait_ready=True)
        # vehicle = connect('127.0.0.1:14550', wait_ready=True)
    except Exception as e:
        print(f"Failed to connect to the vehicle: {e}")
        return

    arm_drone(vehicle)

    try:
        # Tambahkan logika tambahan di sini jika diperlukan

        # Contoh: sleep 5 detik untuk menjaga drone tetap armed
        time.sleep(5)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Disarm motors sebelum menutup koneksi
        print("Disarming motors")
        vehicle.armed = False

        # Menutup koneksi ke Pixhawk
        vehicle.close()
        print("Connection to Pixhawk closed")


if __name__ == "__main__":
    main()
