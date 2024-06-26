import minimalmodbus

# ??Modbus????
instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)  # ?????????ID
instrument.serial.baudrate = 9600  # ???
instrument.serial.bytesize = 8  # ???
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE  # ???
instrument.serial.stopbits = 1  # ???
instrument.serial.timeout = 1  # ????(?)

# ???????????????
register_data_write = [
    (0x5030, 0x0005),  # ??????
    (0x501E, 0x0906),  # VPset 1.05 == 231
    (0x5031, 0x0384),  # PF???0.9 == 900
    (0x3005, 0x0050)  # P???80%
]

# ?????0x06(Write Single Register)?????????
instrument.write_register(0x5030, 0x0005,functioncode=0x06)

instrument.write_register(0x501E, 0x0906,functioncode=0x06)

print("????????")
