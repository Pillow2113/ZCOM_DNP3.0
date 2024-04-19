
import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT GUI")
        self.root.geometry("400x300")  

        self.option_var = tk.StringVar()
        self.data_label = tk.Label(root, text="接收到的数据:")
        self.data_text = tk.Text(root, height=10, width=50)  
        self.option_label = tk.Label(root, text="當前選項:")
        self.current_option_text = tk.Text(root, height=1, width=20, state="disabled")
        self.option_menu = ttk.Combobox(root, textvariable=self.option_var, values=["Option 1", "Option 2", "Option 3"])
        self.start_button = tk.Button(root, text="開始", command=self.start_mqtt, width=15)  
        self.stop_button = tk.Button(root, text="停止", command=self.stop_mqtt, width=15)

        self.data_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.data_text.grid(row=1, column=0, columnspan=2, pady=10)
        self.option_label.grid(row=2, column=0, pady=5)
        self.current_option_text.grid(row=2, column=1, pady=5)
        self.option_menu.grid(row=3, column=0, columnspan=2, pady=10)   
        self.start_button.grid(row=4, column=0, pady=10, padx=5)  
        self.stop_button.grid(row=4, column=1, pady=10, padx=5)

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message

        # 在初始化時就連接和訂閱
        self.mqtt_client.connect("test.mosquitto.org", 1883, 60)
        self.mqtt_client.subscribe("topic/DNP3_GUI")

    def start_mqtt(self):
        selected_option = self.option_var.get()
        self.current_option_text.configure(state="normal")
        self.current_option_text.delete(1.0, tk.END)
        self.current_option_text.insert(tk.END, f"{selected_option}")
        self.current_option_text.configure(state="disabled")

        if selected_option == "Option 1":
            self.mqtt_client.publish("topic/DNP3_GUI", "TEST1")
        elif selected_option == "Option 2":
            self.mqtt_client.publish("topic/DNP3_GUI", "TEST2")
        elif selected_option == "Option 3":
            self.mqtt_client.publish("topic/DNP3_GUI", "q")

    def stop_mqtt(self):
        self.mqtt_client.loop_stop()

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode("utf-8")
        self.data_text.insert(tk.END, f"{data}\n")

if __name__ == "__main__":
    root = tk.Tk()
    mqtt_client = MQTTClient(root)
    root.mainloop()
