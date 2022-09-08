

import numpy as np
import pandas as pd
import time
import datetime
import os
import serial
import ambient


am_v = ambient.Ambient(55079,'fd6b857abb95293d')
am_i = ambient.Ambient(55084,'b6fc84c5f8f17138')

#class to get data from microbit
class GetData:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0',115200,timeout=None)
        print('Port Open')
        print("")
    def GetData(self):
        #wait data from microbit by serial-port
        v_string="Sent data"
        self.ser.write(f"{v_string}\n".encode())
        print("Wait data from microbit")

        line = self.ser.readline()
        print("Recieve data")
        line_So=eval(line)
        data_voltage,data_current = line_So
        print(data_voltage, data_current)
        print("")

        return data_voltage,data_current

def amSend(am, data):

     # Send data to Ambient
    r = am.send(data)
    print(data)

GD = GetData()

#Set interval time of date
interval = 30

while(True):
    try:
        start_time = time.time() #record prosseing time
        dt_now = datetime.datetime.now()#get real time from raspberry pi
        dt_now_arranged = dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')#change format of timestamp
        data_voltage,data_current = GD.GetData() #Get data from microbit
        dic_v = {"d1":data_voltage}
        dic_i = {"d1":data_current}
        amSend(am_v,dic_v)
        amSend(am_i,dic_i)


        pro_time = time.time() - start_time #calculate time to need prosseing
        wait_time = interval - pro_time #calculate reschedule interval time
        print(f'ProcessingTime {pro_time}')
        print("")
        time.sleep(wait_time) #wait to next get data time

    except Exception as e:
        print(e)


ser.close()
