# coding=utf-8
import subprocess

def getCommand(slaveid: str, protocol: str, item: str):
    #functioncode = getfunctioncode(action)

    # sevendi: modified 28/09/2023
    print("Profile:", item)
    address = getaddr(item)
    print("Address:", address)
    if slaveid=='05':
        no_of_register = '00 01' #16bit
        if item == 'sm-total reactive power (W1)' or item == 'sm-total reactive power (W0)' or item == 'sm-total apparent power (W1)' or item == 'sm-total apparent power (W0)':
            no_of_register ='00 02' #32bit
            
    elif slaveid=='07':
        no_of_register = "00 02" #32bit
    
    #for SmartMeter of SICAM
    elif slaveid == '01':
        no_of_register = "00 01"
        
    commmand_without_crc = slaveid + ' 03' +' ' + address + ' ' + no_of_register
    crc = crc16(commmand_without_crc)
    command = commmand_without_crc + ' ' + crc
    return command


def getfunctioncode(action):
    if action == 'read':
        return '03'
    else:
        raise ActionError


def getaddr(item):
    #for smartmeter
    if item == 'sm-Irms_A':
        return '01 1E'
    elif item == 'sm-Irms_B':
        return '01 20'
    elif item == 'sm-Irms_C':
        return '01 22'
    elif item == 'sm-Irms.N':
        return '00  E0' 
    elif item == 'sm-Vrms_A':
        return '01 18'
    elif item == 'sm-Vrms_B':
        return '01 1A'
    elif item == 'sm-Vrms_C':
        return '01 1C'
    elif item == 'sm-Inst.W':
        return '01 24'
    elif item == 'sm-Inst.VAR':
        return '01 26'
    elif item == 'sm-Inst.Power Factor':
        return '01 2A'
    elif item == 'sm-frequency':
        return '01 2c'
    elif item == 'sm-Whn(net)':
        return '01 0A'
    #for DNP3 大同測試
    if item == 'outstation-line_current_phase_a' or item == "outstation-LC_phase_a":  # sevendi: modified 28/09/2023
        return '01 1E'
    elif item == 'outstation-line_current_phase_b' or item == "outstation-LC_phase_b": # sevendi: modified 28/09/2023
        return '01 20'
    elif item == 'outstation-line_current_phase_c' or item == "outstation-LC_phase_c": # sevendi: modified 28/09/2023
        return '01 22'
    elif item == 'outstation-line_current_phase_n' or item == "outstation-LC_phase_n": # sevendi: modified 28/09/2023
        return '00  E0' 
    elif item == 'outstation-line_voltage_phase_ab' or item == "outstation-LV_phase_ab": # sevendi: modified 28/09/2023
        return '01 18'
    elif item == 'outstation-line_voltage_phase_bc' or item == "outstation-LV_phase_bc": # sevendi: modified 28/09/2023
        return '01 1A'
    elif item == 'outstation-line_voltage_phase_ac' or item == "outstation-LV_phase_ac": # sevendi: modified 28/09/2023
        return '01 1C'
    elif item == 'outstation-REP_kw':
        return '01 24'
    elif item == 'outstation-RAP_kvar':
        return '01 26'
    elif item == 'outstation-PF_rms':
        return '01 2A'
    elif item == 'outstation-Freq_Hz':
        return '01 2c'
    elif item == 'outstation-Wha_wh':
        return '01 0A'
#---------------------設定--------------------
    elif item == 'outstation-IRradiance':
        return '01 26'
    elif item == 'outstation-Wind_speed':
        return '01 2A'
    elif item == 'outstation-PF_setting':
        return '01 2c'
    elif item == 'outstation-P_setting':
        return '01 0A'    
    elif item == 'outstation-Q_setting':
        return '01 2A'
    elif item == 'outstation-VPset_setting':
        return '01 2c'
    elif item == 'outstation-Total_kwh':
        return '01 2c'

#---------------------------------------------    
    #for PVInverter
    elif item == 'inv-Power Factor':
        return 'CF 14'
    elif item == 'inv-Output power':
        return 'C0 20'
    elif item == 'inv-AC voltage phase L1':
        return 'C0 21'
    elif item == 'inv-AC output current L1':
        return 'C0 24'
    elif item == 'inv-AC frequency':
        return 'C0 26'
    elif item == 'inv-DC1 input voltage':
        return 'C0 2B'
    elif item == 'inv-DC2 input voltage':
        return 'C0 2C'
    elif item == 'inv-DC1 input current':
        return 'C0 2D'
    elif item == 'inv-DC2 input current':
        return 'C0 2E'
    elif item == 'inv-Input Power A':
        return 'C0 2F'
    elif item == 'inv-Input Power B':
        return 'C0 30'
    elif item == 'inv-Total Output Power':
        return 'C0 31'
    elif item == 'inv-Inverter Heat sink temperature':
        return 'C0 2A'
    
    #for AMD005
    elif item =='sm-I1 present (rms)':
        return '00 C8'
    elif item =='sm-I2 present':
        return '00 C9'
    elif item =='sm-I3 present':
        return '00 CA'
    elif item =='sm-Va present':
        return '00 CC'
    elif item =='sm-Vb present':
        return '00 CD'
    elif item =='sm-Vc present':
        return '00 CE'
    elif item == 'sm-Frequency':
        return '00 D5'
    elif item == 'sm-total reactive power (W1)':
        return '03 1A'
    elif item == 'sm-total reactive power (W0)':
        return '03 1B'
    elif item == 'sm-total apparent power (W1)':
        return '01 42'
    elif item == 'sm-total apparent power (W0)':
        return '01 43'
    
    #for SmartMeter of Sicam
    elif item == 'sm-sicam_Vrms(A)':
        return '10 00'
    elif item == 'sm-sicam_Vrms(B)':
        return '10 01'
    elif item == 'sm-sicam_Vrms(C)':
        return '10 02'
    elif item == 'sm-sicam_Irms(A)':
        return '10 08'
    elif item == 'sm-sicam_Irms(B)':
        return '10 09'
    elif item == 'sm-sicam_Irms(C)':
        return '10 0A'
    elif item == 'sm-sicam_Frequency':
        return '10 1D'

def crc16(string):
    data = bytearray.fromhex(string)
    # logging.info(type(data))
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    crc_int = ((crc & 0xff) << 8) + (crc >> 8)
    crc_str = str(hex(crc_int))
    crc_format = crc_str.split("0x")[1].zfill(
        4)[0:2] + " " + crc_str.split("0x")[1].zfill(4)[2:]
    return crc_format




def main():
    #print(getCommand('05', 'AMD005', 'sm-Frequency'))
    #print(getCommand('01','','sm-/sicam_Frequency'))
    #print(getCommand('05', 'daton', 'read', 'sm-Frequency'))
    print('')

if __name__ == '__main__':
    main()
