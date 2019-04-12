#!/usr/bin/python
import serial
import time


ard = serial.Serial('COM6',115200,timeout=0.5)
time.sleep(2) # wait for Arduino


while 1:
    # Serial write section

    ard.flush()
    tempVal = "521"
    print ("Python value sent: ")
    print (tempVal)
    ard.write(str.encode(tempVal))
   # time.sleep(1) # I shortened this to match the new value in your Arduino code

    # Serial read section
    msg = ard.readline()
    print("Message from arduino: ")
    print (msg.decode('utf-8'))