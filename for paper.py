# -*- coding: utf-8 -*-
import serial
#import easygui as g
import numpy as np
import matplotlib.pyplot as plt
import time
import re
from scipy import signal
import seaborn
import struct
import sys
from bluetooth import *

serialport = serial.Serial('/dev/ttyUSB0', 9600) # 串口配对（蓝牙数据为COM9输出）
if serialport.isOpen():
    print("open success") # 串口打开成功
else:
    print("open failed") # 串口打开失败
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

t = [0] # 数据初始化
m = [0]
i = 0
intdata = 0
data = ''
count = 0
n = 0
msg = 'your posture is not right'
msgtext = ' you are posting'
while True:
    if i > 1000:# 1000次后清零
        del t [:]
        del m [:] # 数据清空
        i = 0
    count = serialport.inWaiting()
    if n >= 80          :
       if n == 80: # 取第80个点为reference
          ref = pdata
       if abs(ref-pdata) >= 0.1 and  n % 40 == 0:# 每在40倍数时开始验证是否需要弹窗提醒
          client_sock.send(msg)
          plt.pause(3)
          #mes = g.msgbox(msg='你驼背了!', title='SEMG muscle', ok_button='I know, 我已坐好')
          del t[:] # 弹窗后清空图像和数据
          del m[:]
          i = 0
          n = 0
    if count > 0:
        data = serialport.readline(2) # 读取头两个数据检测是否为验证数据
        while data == b'AA':
          data=serialport.readline(3) # 数据验证成功，读取电压数据
          if data != '': # 如果数据不为空，则进行绘图
            print('%s' % (data))
            
            i = i + 1
            n = n + 1
            t.append(i)
            intdata=int(data)
            pdata=float((intdata-100)/100) # 对原数据进行还原
            round(pdata,2)
            m.append(pdata)
          plt.pause(0.05)  # 绘图频率

client_sock.close()
server_sock.close()
