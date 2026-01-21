from pyorbbecsdk import Context

ctx = Context()
devices = ctx.query_devices()
print("Devices count:", devices.get_count())
device = devices[0]

print("Device attributes and methods:")
for attr in dir(device):
    print(attr)
