import time
import paho.mqtt.client as mqtt

# 定義回應函數
def on_message(client, userdata, msg):
    global current_response
    payload = msg.payload.decode('utf-8')
    print(payload)
    
    if payload == "TEST1":
        current_response = "TEST1 RECE"
        
    elif payload == "TEST2":
        current_response = "TEST2 RECE"
        
    elif payload == "q":
        current_response = "Stopped"

    # 回傳當前 response
    client.publish("topic/DNP3_GUI", current_response)

# 設置 MQTT 客戶端
client = mqtt.Client()

# 設置回調函數
client.on_message = on_message

# 連接到 Mosquitto 公共測試伺服器
client.connect("test.mosquitto.org", 1883, 60)

# 訂閱 "topic/DNP3_GUI" 主題
client.subscribe("topic/DNP3_GUI")

# 初始 response
current_response = "Unknown Payload"

# 循環保持連接
client.loop_start()

# 模擬主程式
try:
    while True:
        time.sleep(1)
        if current_response == "Stopped":
            # 在這裡加入你想要的停止後的邏輯
            print("Response stopped. Waiting for the next state...")
except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
    client.loop_stop()
