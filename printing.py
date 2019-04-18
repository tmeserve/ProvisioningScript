from constants import getPackage, getFirmware
from serial import Serial
import time, os
from zebra import zebra

tmp_buffer = b''

def printlabel(device, deviceid, imei):
    printFile = open("Template.txt", "r")
    printer = zebra(device)
    lines = printFile.readlines()
    lineStr = "".join(lines)
    lineStr = lineStr.replace("{DEVICEID}", deviceid).replace("{IMEI}", imei).replace("{FIRMWARE}", getFirmware()).replace("{PACKAGE}", getPackage())
    printer.output(lineStr)
    time.sleep(2)
    printFile.close()