# mqtt_handler.py

import datetime
import json
import paho.mqtt.client as mqtt
import DNP3_modbus
import register

mqtt_broker = '192.168.178.1'
mqtt_port = 1883
client_id = 'ea9b8de9-56b2-47f4-b0f2-e469bdc34497'
username = "zcom"
password = "zcom"

mqtt_topic_pf = '652dfe965bcfeb1b05699736/pf'
mqtt_topic_p = '652dfe965bcfeb1b05699736/p'
mqtt_topic_vpset = '652dfe965bcfeb1b05699736/VPset'

def on_message_receive(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    print("Received message:", payload)  

    if payload:
        process_received_message(topic, payload)  

def process_received_message(topic, payload):
    try:
        payload_dict = json.loads(payload)  
        if "command_value" in payload_dict:
            command_value = payload_dict["command_value"]

            if topic == mqtt_topic_pf:
                if command_value == 90:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x5031, 0x0384)
                elif command_value == 100:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x5031, 0x03E8)
                else:
                    print(f"Received /pf message with unknown command_value: {command_value}")
            elif topic == mqtt_topic_p:
                if command_value == 80:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x3005, 0x0050)
                elif command_value == 100:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x3005, 0x0064)
                else:
                    print(f"Received /p message with unknown command_value: {command_value}")
            elif topic == mqtt_topic_vpset:
                if command_value == 105:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x501E, 0x0906)
                else:
                    print(f"Received /VPset message with unknown command_value: {command_value}")
            else:
                print(f"Received message on unknown topic: {topic}")
        else:
            print(f"Received message with no 'command_value' in payload: {payload}")
    except json.JSONDecodeError:
        print(f"Received message with invalid JSON payload: {payload}")


def publish_data(client, data):
    print("Publishing data...")

    try:
        token = register.get_token()['token']
        print("Token: %s", token)
        gw_id = "652dfe965bcfeb1b05699736"
        print("Gateway id: %s", gw_id)

        to_send = {	
            "token": token,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"),
            "inverter_com_port": "1", 
            "inverter_id": "",
            "smart_meter_com_port": "2", 
            "smart_meter_id": "8",
            "data": data
        }
        #with mqtt_lock:
        client.publish(gw_id, json.dumps(to_send))
        print("Data published successfully")
    except Exception as e:
        print("Error publishing data: %s", str(e))




def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!   ready UP Data")
        else:
            print(f"Failed to connect, return code {rc}\n")
    
    client = mqtt.Client(client_id=client_id, clean_session=True, transport="tcp")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)

    return client