import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

mqtt_broker = '60.248.187.110'
mqtt_port = 1884
username = "zcom"
password = "Zcom@8414"
push_client_id = 'ea9b8de9-56b2-47f4-b0f2-e469bdc35497'
topic = "652dfe965bcfeb1b05699736"  # 這裡填入您要接收的 MQTT topic

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    received_data_text.config(state=tk.NORMAL)
    received_data_text.insert(tk.END, f"Received data: {msg.payload.decode('utf-8')}\n")
    received_data_text.config(state=tk.DISABLED)

def publish_data():
    selected_device = device_combobox.get()
    slaveid_value = slaveid_entry.get()
    comport_value = comport_combobox.get()
    baudrate_value = baudrate_combobox.get()
    stopbit_value = stopbit_combobox.get()
    databit_value = databit_combobox.get()
    parity_value = parity_combobox.get()

    # 檢查是否有欄位未填寫
    if not slaveid_value or not comport_value or not baudrate_value or not stopbit_value or not databit_value or not parity_value:
        print("請填寫所有欄位。")
        return

    device_info = {
        'device': selected_device,
        'slaveid': slaveid_value,
        'comport': comport_value,
        'baudrate': baudrate_value,
        'stopbit': stopbit_value,
        'databit': databit_value,
        'parity': parity_value
    }

    # 將資訊轉為 JSON 格式的字串
    device_json = json.dumps(device_info)

    # 傳送資料到 MQTT broker
    publish.single(topic, device_json, hostname=mqtt_broker, port=mqtt_port)

    print(f"已傳送 {selected_device} 的資料: {device_json}")

def start_reception():
    client = mqtt.Client(client_id=push_client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()

def stop_reception():
    # Add logic to stop receiving data from MQTT
    received_data_text.config(state=tk.NORMAL)
    received_data_text.insert(tk.END, "停止接收...\n")
    received_data_text.config(state=tk.DISABLED)

# 設定介面元件
root = tk.Tk()
root.title("MQTT 資料發布與接收")

# 主框架
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=5, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# 設定介面元件
device_label = ttk.Label(main_frame, text="選擇設備:")
device_combobox = ttk.Combobox(main_frame, values=['大同電表', 'PV3000'])
slaveid_label = ttk.Label(main_frame, text="Slave ID:")
slaveid_entry = ttk.Entry(main_frame)
comport_label = ttk.Label(main_frame, text="Comport:")
comport_combobox = ttk.Combobox(main_frame, values=['/dev/ttyUSB0', '/dev/ttyUSB1'])
baudrate_label = ttk.Label(main_frame, text="波特率:")
baudrate_combobox = ttk.Combobox(main_frame, values=['9600', '115200'])
stopbit_label = ttk.Label(main_frame, text="停止位:")
stopbit_combobox = ttk.Combobox(main_frame, values=['1', '2'])
databit_label = ttk.Label(main_frame, text="資料位:")
databit_combobox = ttk.Combobox(main_frame, values=['8', '7'])
parity_label = ttk.Label(main_frame, text="校驗位:")
parity_combobox = ttk.Combobox(main_frame, values=['None', 'Even', 'Odd'])

publish_button = ttk.Button(main_frame, text="發布資料", command=publish_data)
start_button = ttk.Button(main_frame, text="開始接收", command=start_reception)
stop_button = ttk.Button(main_frame, text="停止接收", command=stop_reception)

received_data_text = ScrolledText(root, wrap=tk.WORD, width=50, height=30)
received_data_text.config(state=tk.DISABLED)

# 排列介面元件
device_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
device_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
slaveid_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
slaveid_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
comport_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
comport_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
baudrate_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
baudrate_combobox.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)
stopbit_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
stopbit_combobox.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)
databit_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
databit_combobox.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)
parity_label.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
parity_combobox.grid(row=6, column=1, padx=10, pady=10, sticky=tk.W)

publish_button.grid(row=7, column=0, columnspan=2, pady=10, sticky=tk.W)
start_button.grid(row=8, column=0, pady=10, sticky=tk.W)
stop_button.grid(row=8, column=1, pady=10, sticky=tk.W)

received_data_text.grid(row=0, column=1, rowspan=9, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# 啟動主視窗
root.mainloop()
