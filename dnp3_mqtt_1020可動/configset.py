# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 13:19:31 2022

@author: erichuang
"""
def loadConfig():
    config = {}
    config_arr = [[]]
    temp_arr = []
    configFile = open('/zcomIottalk_update/iotconfig_v1.1.txt','r')
    configLines = configFile.readlines()
    for line in range(0,len(configLines)):
        str_result = configLines[line].split(":")[0]
        if str_result == 'end':
            #print(temp_arr)
            config_arr.append(temp_arr.copy())
            temp_arr.clear()
            #print(config_arr)
        elif str_result == 'target':
            target =configLines[line].replace("\n","").split("target:")[1]
            temp_arr.append('target:'+target)
            #print('target:',target)
        elif str_result == 'device':
            device =configLines[line].replace("\n","").split(":")[1]
            temp_arr.append('device:'+device)
            #print('device:',device)
        elif str_result == 'items':
            items =configLines[line].replace("\n","").split(":")[1]
            temp_arr.append('items:'+items)
            #print('items:',items)
        elif str_result == 'comport':
            comport =configLines[line].replace("\n","").split(":")[1]
            temp_arr.append('comport:'+comport)
        elif str_result == 'baudrate':
            baudrate =configLines[line].replace("\n","").split(":")[1]
            temp_arr.append('baudrate:'+baudrate)
            #print('baudrate:',baudrate)
        elif str_result == 'stopbit':
            stopbit =configLines[line].replace("\n","").split(":")[1]
            temp_arr.append('stopbit:'+stopbit)
            #print('stopbit:',stopbit)
        elif str_result == 'databit':
            databit =configLines[line].replace("\n","").split(":")[1]
            temp_arr.append('databit:'+databit)
            #print('databit:',databit)
        elif str_result == 'parity':
            parity =configLines[line].replace("\n","").split(":")[1]
            temp_arr.append('parity:'+parity)
            #print('parity:',parity)
            
    #print(config_arr)
    return config_arr

#loadConfig()

