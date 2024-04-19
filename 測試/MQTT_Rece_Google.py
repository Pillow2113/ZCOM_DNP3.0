import requests
import paho.mqtt.client as mqtt
import json

mqtt_broker = '60.248.187.110'
mqtt_port = 1884
username = "zcom"
password = "Zcom@8414"

AP_Total, Avg_Vrms, Avg_Irms, PF_Data, KW_Date = 0, 0, 0, 0, 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("成功連線到MQTT伺服器")
    else:
        print("連線失敗，回傳碼: {}".format(rc))

def on_message(client, userdata, msg):
    global AP_Total, Avg_Vrms, Avg_Irms, PF_Data, KW_Date
    try:
        payload = json.loads(msg.payload.decode())
    
        AP_Total = payload.get("AP_Total", 0)
        Avg_Vrms = payload.get("Avg_Vrms", 0)
        Avg_Irms = payload.get("Avg_Irms", 0)
        PF_Data = payload.get("PF", 0)
        KW_Date = payload.get("KW", 0)

        print("收到主題 {} 的訊息: {}".format(msg.topic, payload))

        url = 'https://script.google.com/macros/s/AKfycbzIc_4LK8E9V3Xh0jIofk_D6gjLiVNgPWTBKwLny1sz3lg3aV_hi8mczdtYsOf0Ehxh/exec'
    
        params = {
            'name': 'Today',
            'top': 'true',
            'data': '[' + str(AP_Total) + ',' + str(Avg_Vrms) + ',' + str(Avg_Irms) + ',' + str(PF_Data) + ',' + str(KW_Date) + ']'
        }

        web = requests.get(url=url, params=params)
    except Exception as e:
        print(f"發生例外: {e}")

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
topic = "data/chineseSmartMeter"
client.subscribe(topic)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("程式被中斷")
    client.disconnect()
    print("已斷開與MQTT伺服器的連線")
