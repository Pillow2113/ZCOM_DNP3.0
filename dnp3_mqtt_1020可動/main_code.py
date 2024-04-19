# -*- coding: utf-8 -*-
import DNP3_modbus 
import configset
import time
import datetime
import threading
import mqtt_handler
import rece
import register
import json
import paho.mqtt.client as mqtt

 
#------------------------------------------------

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
    (0x010A, 'outstation-Wha_wh')
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

#----------------------------------------------------------------

def items():
   # 讀取配置數據

    res_data = configset.loadConfig()
    profile = []
    orin_profile = []
    
    for i in range(1, len(res_data)):
        for j in range(0, len(res_data[i])):
            if res_data[i][j].split(':')[0] == 'items':
               items = res_data[i][j].split(':')[1]
               print('items:', items)
               profile.append(items)
               orin_profile.append(items)
    mac_address = register.get_mac_addr()
    register.register_gw(mac_address, profile)


#----------------------------------------------------------------

def publish_data_periodically():
    while True:
        formatted_data = get_formatted_data()  # 取得需要發佈的數據
        mqtt_client = mqtt_handler.connect_mqtt()  # 連接到MQTT代理
        mqtt_handler.publish_data(mqtt_client, formatted_data)  # 發布數據
        mqtt_client.disconnect()  # 斷開MQTT連接
        time.sleep(2.5)  # 設定發布資料的時間間隔
#----------------------------------------------------------------

def get_formatted_data():
     device1_data = DNP3_modbus.read_modbus_32_device('/dev/ttyUSB0', 7, register_data_device1)
     device2_data = DNP3_modbus.read_modbus_16_device('/dev/ttyUSB1', 1, register_data_device2)
     # 處理 outstation-PF_setting 和 outstation-VPset_setting 數據

     if 'outstation-PF_setting' in device2_data:
         device2_data['outstation-PF_setting'] /= 10  # 除以10
     
     if 'outstation-VPset_setting' in device2_data:
         device2_data['outstation-VPset_setting'] = (device2_data['outstation-VPset_setting'] / 220) * 10
     
     combined_data = {**device1_data, **device2_data}

     formatted_data = [
          {
               "sensor_name": key,
               "value": value,
               "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          }
        for key, value in combined_data.items()
     ]

     return formatted_data 
#----------------------------------------------------------------
def start_mqtt_receiver():
    try:
        client = rece.connect_mqtt()  
        client.loop_forever()  

    except Exception as e:
        print("Error connecting to MQTT:", str(e))
#----------------------------------------------------------------

def start_data_uploader():
    
    publish_data_periodically()
#----------------------------------------------------------------

if __name__ == "__main__":
    items()

   # 建立一個執行緒來運行 MQTT 接收
    receiver_thread = threading.Thread(target=start_mqtt_receiver)
    receiver_thread.daemon = True
    receiver_thread.start()

   # 建立一個執行緒來運行資料上傳
    uploader_thread = threading.Thread(target=start_data_uploader)
    uploader_thread.daemon = True
    uploader_thread.start()      
    while True:
        
        time.sleep(3)

