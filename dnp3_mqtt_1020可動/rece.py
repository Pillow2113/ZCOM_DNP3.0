import paho.mqtt.client as mqtt
import DNP3_modbus
import json

mqtt_broker = '192.168.178.1'
mqtt_port = 1883

mqtt_topic_pf = '652dfe965bcfeb1b05699736/pf'
mqtt_topic_p = '652dfe965bcfeb1b05699736/p'
mqtt_topic_vpset = '652dfe965bcfeb1b05699736/VPset'

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    
    try:
        payload_dict = json.loads(payload)
        print("Received message:", payload_dict)
        
        if "command_value" in payload_dict:
            command_value = payload_dict["command_value"]

            if topic == mqtt_topic_pf:
                if command_value == 90:
                    #with mqtt_lock:

                        DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x5031, 0x0384)
                elif command_value == 100:
                    #with mqtt_lock:

                        DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x5031, 0x03E8)
                else:
                    print(f"Received /pf message with unknown command_value: {command_value}")
            elif topic == mqtt_topic_p:
                if command_value == 80:
                    #with mqtt_lock:

                        DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x3005, 0x0050)
                elif command_value == 100:
                    #with mqtt_lock:

                        DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x3005, 0x0064)
                else:
                    print(f"Received /p message with unknown command_value: {command_value}")
            elif topic == mqtt_topic_vpset:
                if command_value == 105:
                    #with mqtt_lock:
                        DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x501E, 0x0906)
                else:
                    print(f"Received /VPset message with unknown command_value: {command_value}")
            else:
                print(f"Received message on unknown topic: {topic}")
        else:
            print(f"Received message with no 'command_value' in payload: {payload}")
    except json.JSONDecodeError:
        print(f"Received message with invalid JSON payload: {payload}")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message  
    client.connect(mqtt_broker, mqtt_port)

    client.subscribe(mqtt_topic_pf)
    client.subscribe(mqtt_topic_p)
    client.subscribe(mqtt_topic_vpset)
    
    return client

if __name__ == "__main__":
    client = connect_mqtt()
    client.loop_forever()
