# from dronekit import connect, VehicleMode
# import time

# # Menghubungkan ke SITL
# connection_string = '127.0.0.1:631'
# print('Connecting to vehicle on: %s' % connection_string)
# vehicle = connect(connection_string, wait_ready=True)

# # Mengambil informasi dasar dari drone
# print("GPS: %s" % vehicle.gps_0)
# print("Battery: %s" % vehicle.battery)
# print("Last Heartbeat: %s" % vehicle.last_heartbeat)
# print("Is Armable?: %s" % vehicle.is_armable)
# print("System status: %s" % vehicle.system_status.state)
# print("Mode: %s" % vehicle.mode.name)    # mode

# # Menutup koneksi
# vehicle.close()


from dronekit import connect
import time

# Ganti dengan port yang sesuai (5760 dalam hal ini)
connection_string = '127.0.0.1:5760'

print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True, timeout=60)

print("Connected to vehicle")
print("Vehicle state: %s" % vehicle.mode.name)  # Print mode saat ini
vehicle.close()
