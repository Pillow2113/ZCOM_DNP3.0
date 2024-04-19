import minimalmodbus
import time

# 设置串口参数
instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)  # 串口设备路径和设备ID
instrument.serial.baudrate = 9600  # 波特率
instrument.serial.bytesize = 8  # 数据位
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE  # 校验位
instrument.serial.stopbits = 1  # 停止位
instrument.serial.timeout = 1  # 超时时间（秒）

# 寄存器地址和名称列表
register_data = [
    (0x103D, "inv-Power Factor"),
    (0x1001, "inv-AC voltage phase L1"),
    (0x1002, "inv-AC output current L1"),
    (0x1005, "inv-AC frequency L1"),
    (0x1010, "inv-DC1 input voltage"),
    (0x1014, "inv-DC2 input voltage"),
    (0x1011, "inv-DC1 input current"),
    (0x1015, "inv-DC2 input current"),
    (0x1012, "inv-Input Power A DC High"),
    (0x1013, "inv-Input Power A DC Low"),
    (0x1037, "inv-Total Output Power High"),
    (0x1038, "inv-Total Output Power Low"),
    (0x101C, "inv-Inverter Heat sink temperature"),
    (0x5031, "PF Setting"),
    (0x501E, "VPset"),
    (0x3005, "P Setting"),
    (0x5114, "Q")
]

while True:
    values = {}  # 创建一个空字典来存储读取到的值

    # 读取每个寄存器的值并将其存储在字典中
    for address, name in register_data:
        value = instrument.read_register(address)
        values[name] = value

    # 打印每个命名和对应的值
    for name, value in values.items():
        print(f"{name}: {value}")

    time.sleep(3)  # 等待3秒后再次读取数据
