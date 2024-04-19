import paho.mqtt.client as mqtt
import json
import DNP3_modbus

# ??????,??????????
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')

    try:
        payload_dict = json.loads(payload)  # ? JSON ??? payload ?? Python ??
        print("######################################################", payload_dict)
        command_value = payload_dict["command_value"]

        if command_value is not None:
            if topic == '652dfe965bcfeb1b05699736/pf':
                if command_value == 90:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1,0x5031, 0x0384)
                elif command_value == 100:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x5031, 0x03E8)
                else:
                    print(f"Received /pf message with unknown command_value: {command_value}")
            elif topic == '652dfe965bcfeb1b05699736/p':
                if command_value == 80:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x3005, 0x0050)
                elif command_value == 100:
                    DNP3_modbus.write_modbus_device('/dev/ttyUSB1', 1, 0x3005, 0x0064)
                else:
                    print(f"Received /p message with unknown command_value: {command_value}")
            elif topic == '652dfe965bcfeb1b05699736/VPset':
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


client = mqtt.Client(client_id="ea9b8de9-56b2-47f4-b0f2-e469bdc34497")

client.on_message = on_message

broker_address = "192.168.178.1"
port = 1883
client.connect(broker_address, port)


client.subscribe("652dfe965bcfeb1b05699736/pf")
client.subscribe("652dfe965bcfeb1b05699736/p")
client.subscribe("652dfe965bcfeb1b05699736/VPset")

client.loop_forever()
