

import numpy as np
import pandas as pd
import time
import datetime
#import cv2
import os
import serial
import ambient


am_v = ambient.Ambient(55079,'fd6b857abb95293d')
am_i = ambient.Ambient(55084,'b6fc84c5f8f17138')

#データを取得するためのクラス
class GetData:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0',115200,timeout=None)
        print('Port Open')
        print("")
    def GetData(self):
        #センサからのデータを取得
        v_string="Sent data"
        self.ser.write(f"{v_string}\n".encode())
        print("Wait data from microbit")
        
        #print(type("kblhvlhvS".encode()))
        line = self.ser.readline()
        print("Recieve data")
        line_So=eval(line)
        data_voltage,data_current = line_So
        print(data_voltage, data_current)
        print("")
            
        return data_voltage,data_current

def amSend(am, data):

     # Ambient
    r = am.send(data)
    print(data)

GD = GetData()

interval = 30#データを取得する時間間隔

while(True):
    try:
        start_time = time.time()#処理開始時間記録
        dt_now = datetime.datetime.now()#記録用の時間取得
        dt_now_arranged = dt_now.strftime('%Y/%m/%d %H:%M:%S.%f')#タイムスタンプの形式変換
        data_voltage,data_current = GD.GetData() #データ取得
        dic_v = {"d1":data_voltage}
        dic_i = {"d1":data_current}
        amSend(am_v,dic_v)
        amSend(am_i,dic_i)


        pro_time = time.time() - start_time #処理にかかった時間を計算
        wait_time = interval - pro_time #データを取得する間隔を調整する時間を計算
        print(f'ProcessingTime {pro_time}')
        print("")
        time.sleep(wait_time) #時間調整
        
    except Exception as e:
        print(e)


ser.close()
