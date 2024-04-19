import minimalmodbus
import time

# 设置串口参数
instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 7)  # 串口设备路径和设备ID
instrument.serial.baudrate = 9600  # 波特率
instrument.serial.bytesize = 8  # 数据位
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE  # 校验位
instrument.serial.stopbits = 1  # 停止位
instrument.serial.timeout = 1  # 超时时间（秒）

#-------------------------------------read--------------------------------
# 寄存器地址和名称列表
register_data_read = [
    (0x011E, 'outstation-LC_phase_a'),
    (0x0120, 'outstation-LC_phase_b'),
    (0x0122, 'outstation-LC_phase_c'),
    (0x00E0, 'outstation-LC_phase_n'),
    (0x0118, 'outstation-LV_phase_ab'),
    (0x011A, 'outstation-LV_phase_bc'),
    (0x011C, 'outstation-LV_phase_ac'),
    (0x0124, 'outstation-REP_kw'),
    (0x0126, 'outstation-RAP_kvar'),
    (0x012A, 'outstation-PF_rms'),
    (0x012C, 'outstation-Freq_Hz'),
    (0x010A, 'outstation-Wha_wh')

]

while True:
    values = {}  # 创建一个空字典来存储读取到的值

    # 读取每个寄存器的值并将其存储在字典中
    for address, name in register_data_read:
        value = instrument.read_long(address)
        values[name] = value

    # 打印每个命名和对应的值
    for name, value in values.items():
        print(f"{name}: {value}")

    time.sleep(3)  # 等待3秒后再次读取数据
