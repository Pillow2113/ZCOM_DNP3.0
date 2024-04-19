import paho.mqtt.client as mqtt
import json
import random
import datetime  

mqtt_broker = '60.248.187.110'
mqtt_port = 1884
username = "zcom"
password = "Zcom@8414"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("成功連線到MQTT伺服器")
    else:
        print("連線失敗，回傳碼: {}".format(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("成功訂閱主題")

def on_message(client, userdata, msg):
    print("收到主題 {} 的訊息: {}".format(msg.topic, msg.payload.decode()))

client = mqtt.Client()

client.username_pw_set(username, password)


client.on_connect = on_connect


client.on_subscribe = on_subscribe

client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

topic = "data/chineseSmartMeter"
client.subscribe(topic)

payload = {
    "devId": random.randint(0, 100),  
    "value": random.uniform(0, 100),
    "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f"),
}

client.publish(topic, json.dumps(payload))

client.loop_forever()
