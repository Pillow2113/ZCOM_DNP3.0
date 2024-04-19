# -*- coding: utf-8 -*-
import minimalmodbus

#-------for 32 ------------

def read_modbus_32_device(device_port, device_id, register_data):
    # 创建Modbus设备对象
    instrument = minimalmodbus.Instrument(device_port, device_id)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1

    # 读取寄存器数据
    data = {}
    for address, name in register_data:
        value = instrument.read_long(address)
        data[name] = value

    return data

#-------for 16 -----------
def read_modbus_16_device(device_port, device_id, register_data):
    # 创建Modbus设备对象
    instrument = minimalmodbus.Instrument(device_port, device_id)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1

    # 读取寄存器数据
    data = {}
    for address, name in register_data:
        value = instrument.read_register(address)
        data[name] = value

    return data

def write_modbus_device(device_port, device_id, address, value):
    # 创建Modbus设备对象
    instrument = minimalmodbus.Instrument(device_port, device_id)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1

    # 写入寄存器数据
    instrument.write_register(address, value, functioncode=0x06)

