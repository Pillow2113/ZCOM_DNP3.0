# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:16:28 2022

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""

# pip install paho-mqtt
from multiprocessing import Value
import paho.mqtt.client as mqtt
from random import randint
import datetime
import time 
import requests 
import subprocess
import DNP3_modbus
import json

broker_address = '192.168.178.1' # '122.146.84.34'
port = 1883
client_id = 'ea9b8de9-56b2-47f4-b0f2-e469bdc34497'
username = "zcom"
password = "zcom"
addr = broker_address



def get_mac_addr():
    try:
      command='ifconfig|grep br-lan'
      val=subprocess.getstatusoutput(command)
      res = val[1].split('HWaddr')
      #print('res:',res[1])
      res = str.lstrip(res[1])
      print("Mac address:", res)
      return res.lower()
    except:
      print('mac address error.')
      return 'none'



def register_gw(mac_addr, profiles):
    print(f"Registering new gateway with mac {mac_addr}...")
    r = requests.post(f"https://{addr}:24/dnp3_gateway/register", 
                 headers={"token": "COPYRIGHT ZCOM INC"},
		 verify=False,
                 json={
                        "gateway_name": 'MQTT Dev-test 1.0',
                        "mac_address": mac_addr,
                        "profile": profiles
                    })
    print("Registration status:", r.json())
    return r.json()

def get_token(): 

    mac_address = get_mac_addr()
    print("Catch mac:", mac_address)
    r = requests.get(f"https://{addr}:24/dnp3_gateway/get_token",
                     verify=False, 
                     headers={"authorization": mac_address})
    print("Get token:", r.json())
    return r.json() 

def get_gw_info(token):
    r = requests.get(f"https://{addr}:24/dnp3_gateway/get_gateway_info",
                     verify=False, 
                     headers={"token": token})
    return r.json()


    
    

