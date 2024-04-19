import paho.mqtt.client as mqtt
import json

# MQTT 設定
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
topic = "openGUI"

def on_message(client, userdata, msg):
    received_data_json = msg.payload.decode('utf-8')
    received_data = json.loads(received_data_json)

    with open("存吧.txt", "r") as f:
        res_data = f.read()

    duplicate_comport = any(
        f"comport:'{received_data['comport']}'" in config for config in res_data.split('end:')
    )

    
    with open("存吧.txt", "w") as f:
        configs = res_data.split('end:')
        config_found = False
        for config in configs:
            if f"comport:'{received_data['comport']}'" in config:
                f.write(f"device:'{received_data['device']}'\n")
                f.write(f"slaveid:'{received_data['slaveid']}'\n")
                f.write(f"comport:'{received_data['comport']}'\n")
                f.write(f"baudrate:'{received_data['baudrate']}'\n")
                f.write(f"stopbit:'{received_data['stopbit']}'\n")
                f.write(f"databit:'{received_data['databit']}'\n")
                f.write(f"parity:'{received_data['parity']}'\nend:\n")
                config_found = True
            elif config.strip():  
                f.write(config + 'end:\n')

        if not config_found:
            print("Adding new config.")
            f.write(f"device:'{received_data['device']}'\n")
            f.write(f"slaveid:'{received_data['slaveid']}'\n")
            f.write(f"comport:'{received_data['comport']}'\n")
            f.write(f"baudrate:'{received_data['baudrate']}'\n")
            f.write(f"stopbit:'{received_data['stopbit']}'\n")
            f.write(f"databit:'{received_data['databit']}'\n")
            f.write(f"parity:'{received_data['parity']}'\nend:\n")

client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(topic)
client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from MQTT broker")
