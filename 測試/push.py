import tkinter as tk
from tkinter import ttk
import paho.mqtt.publish as publish
import json

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
        print("Please fill in all fields.")
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

    print(f"Data sent for {selected_device}: {device_json}")

# 設定MQTT broker的地址和端口
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883

# 定義每個設備的 MQTT topic
topic = "openGUI"

# 建立主視窗
root = tk.Tk()
root.title("MQTT Data Publisher")

# 設定介面元件
device_label = ttk.Label(root, text="Select Device:")
device_combobox = ttk.Combobox(root, values=['SmartMeter', 'PV3000'])
slaveid_label = ttk.Label(root, text="Slave ID:")
slaveid_entry = ttk.Entry(root)
comport_label = ttk.Label(root, text="Comport:")
comport_combobox = ttk.Combobox(root, values=['/dev/ttyUSB0', '/dev/ttyUSB1'])
baudrate_label = ttk.Label(root, text="Baudrate:")
baudrate_combobox = ttk.Combobox(root, values=['9600', '115200'])
stopbit_label = ttk.Label(root, text="Stopbit:")
stopbit_combobox = ttk.Combobox(root, values=['1', '2'])
databit_label = ttk.Label(root, text="Databit:")
databit_combobox = ttk.Combobox(root, values=['8', '7'])
parity_label = ttk.Label(root, text="Parity:")
parity_combobox = ttk.Combobox(root, values=['None', 'Even', 'Odd'])

publish_button = ttk.Button(root, text="Publish Data", command=publish_data)

# 排列介面元件
device_label.grid(row=0, column=0, padx=10, pady=10)
device_combobox.grid(row=0, column=1, padx=10, pady=10)
slaveid_label.grid(row=1, column=0, padx=10, pady=10)
slaveid_entry.grid(row=1, column=1, padx=10, pady=10)
comport_label.grid(row=2, column=0, padx=10, pady=10)
comport_combobox.grid(row=2, column=1, padx=10, pady=10)
baudrate_label.grid(row=3, column=0, padx=10, pady=10)
baudrate_combobox.grid(row=3, column=1, padx=10, pady=10)
stopbit_label.grid(row=4, column=0, padx=10, pady=10)
stopbit_combobox.grid(row=4, column=1, padx=10, pady=10)
databit_label.grid(row=5, column=0, padx=10, pady=10)
databit_combobox.grid(row=5, column=1, padx=10, pady=10)
parity_label.grid(row=6, column=0, padx=10, pady=10)
parity_combobox.grid(row=6, column=1, padx=10, pady=10)

publish_button.grid(row=7, column=0, columnspan=2, pady=10)

# 啟動主視窗
root.mainloop()
