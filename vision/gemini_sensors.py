from pyorbbecsdk import Context

ctx = Context()
devices = ctx.query_devices()
device = devices[0]

print("Devices count:", devices.get_count())
sensors = device.get_sensor_list()
print("Sensors available:")
for i, s in enumerate(sensors):
    print(i, s)
