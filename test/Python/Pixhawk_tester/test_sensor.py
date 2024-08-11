from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading


class PixhawkData:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def get_gps_data(self):
        gps_data = self.vehicle.location.global_frame
        return {
            'latitude': gps_data.lat,
            'longitude': gps_data.lon,
            'altitude': gps_data.alt
        }

    def get_attitude_data(self):
        attitude = self.vehicle.attitude
        return {
            'roll': attitude.roll,
            'pitch': attitude.pitch,
            'yaw': attitude.yaw
        }

    def get_velocity_data(self):
        velocity = self.vehicle.velocity
        return {
            'north': velocity[0],
            'east': velocity[1],
            'down': velocity[2]
        }

    def get_battery_data(self):
        battery = self.vehicle.battery
        return {
            'voltage': battery.voltage,
            'current': battery.current,
            'level': battery.level
        }

    def get_mode(self):
        return self.vehicle.mode.name

    def get_compass_data(self):
        return {'heading': self.vehicle.heading}

    def get_barometer_data(self):
        return {'altitude': self.vehicle.location.global_relative_frame.alt}


def main():
    try:
        # Koneksi ke Pixhawk melalui serial port
        print("Connecting to Pixhawk")
        vehicle = connect('COM7', baud=921600, wait_ready=True)
        # vehicle = connect('127.0.0.1:14550', wait_ready=True)
    except Exception as e:
        print(f"Failed to connect to the vehicle: {e}")
        return

    pixhawk_data = PixhawkData(vehicle)

    try:
        while True:
            # Mengambil data dari setiap sensor dan menyimpannya dalam variabel terpisah
            gps_data = pixhawk_data.get_gps_data()
            attitude_data = pixhawk_data.get_attitude_data()
            velocity_data = pixhawk_data.get_velocity_data()
            battery_data = pixhawk_data.get_battery_data()
            mode_data = pixhawk_data.get_mode()
            compass_data = pixhawk_data.get_compass_data()
            barometer_data = pixhawk_data.get_barometer_data()

            # Mencetak nilai dari setiap sensor
            print(f"GPS Data: {gps_data}")
            print(f"Attitude Data: {attitude_data}")
            print(f"Velocity Data: {velocity_data}")
            print(f"Battery Data: {battery_data}")
            print(f"Mode: {mode_data}")
            print(f"Compass Data: {compass_data}")
            print(f"Barometer Data: {barometer_data}")
            print("------")

            time.sleep(2)  # Ulangi setiap 2 detik
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Menutup koneksi ke Pixhawk
        vehicle.close()
        print("Connection to Pixhawk closed")


if __name__ == "__main__":
    main()
