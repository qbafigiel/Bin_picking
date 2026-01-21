from pyorbbecsdk import Context

print("Creating Orbbec context...")

ctx = Context()

device_list = ctx.query_devices()

print("Number of devices found:", device_list.get_count())
