from constants import getPackage, getFirmware
import time, os
import serial

tmp_buffer = b''

def printlabel(device, deviceid, imei, amount):
    i = 1
    printFile = open("Template.txt", "r")
    lines = printFile.readlines()
    lineStr = "".join(lines)
    lineStr = lineStr.replace("{DEVICEID}", deviceid).replace("{IMEI}", imei).replace("{FIRMWARE}", getFirmware()).replace("{PACKAGE}", getPackage())
    ser = serial(device, 9600)
    if ser.isOpen():
        ser.close()
    ser.open()

    while i <= int(amount):
        ser.write(lineStr.encode())
        time.sleep(.05)
        i += 1

    printFile.close()