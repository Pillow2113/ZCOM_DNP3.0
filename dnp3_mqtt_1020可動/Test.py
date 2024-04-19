import DNP3_modbus
import time

register_data_device1 = [
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
    (0x010A, 'outstation-Wha_wh'),
    (0x0106, 'Whi(import)'),
    (0x0108, 'Whe(export)'),
    (0x010A, 'Whn(net)'),
]

register_data_device2 = [
    (0x5031, "outstation-IRradiance"),
    (0x5031, "outstation-Wind_speed"),
    (0x5031, "outstation-PF_setting"),
    (0x3005, "outstation-P_setting"),
    (0x5114, "outstation-Q_setting"),
    (0x501E, "outstation-VPset_setting"),
    (0x501E, "outstation-Total_kwh"),
]

def valueconverse(item, value):
    if item in ['outstation-LC_phase_a', 'outstation-LC_phase_b', 'outstation-LC_phase_c', 'outstation-LC_phase_n', 'outstation-LV_phase_ab', 'outstation-LV_phase_bc', 'outstation-LV_phase_ac', 'outstation-PF_rms']:
        value *= 0.01
    elif item in ['outstation-REP_kw', 'outstation-RAP_kvar', 'sm-current sicam_Irms(B)', 'sm-current sicam_Irms(C)']:
        value *= 0.001
    elif item in ['outstation-Freq_Hz', 'outstation-RAP_kvar', 'sm-current sicam_Irms(B)', 'sm-current sicam_Irms(C)']:
        value *= 0.1        
    return value



def read_and_print_modbus_data():
    while True:
        device1_data = DNP3_modbus.read_modbus_32_device('/dev/ttyUSB0', 7, register_data_device1)
        device2_data = DNP3_modbus.read_modbus_16_device('/dev/ttyUSB1', 1, register_data_device2)


        # 打印设备1的数据
        print("Device 1 Data:")
        for key, value in device1_data.items():
            # 将无符号整数解释为有符号整数
            # signed_value = value if value < 2**31 else value - 2**32  # 先进行符号转换
            # converted_value = valueconverse(key, signed_value)  # 再进行单位转换
            print(f"{key}: {value}")

            #print(f"{key}: {converted_value}")



        
        # 打印设备2的数据
        print("Device 2 Data:")
        for key, value in device2_data.items():
            print(f"{key}: {value}")
        
        time.sleep(2.5)  # 设置读取数据的时间间隔

if __name__ == "__main__":
    read_and_print_modbus_data()

