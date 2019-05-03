from constants import getPackage, getFirmware
import time, os
import serial

tmp_buffer = b''

def printlabel(device, deviceid, imei, amount):
    i = 1
    printFile = open("Template.txt", "r")
    # Reads the file
    lines = printFile.readlines()
    lineStr = "".join(lines)
    # Replaces everything needed to be replaced
    lineStr = lineStr.replace("{DEVICEID}", deviceid).replace("{IMEI}", imei).replace("{FIRMWARE}", getFirmware()).replace("{PACKAGE}", getPackage())
    ser = serial(device, 9600)
    if ser.isOpen():
        ser.close()
    ser.open()

    while i <= int(amount):
        # Writes to the printer x amount of times
        ser.write(lineStr.encode())
        time.sleep(.05)
        i += 1
    # Closes the file
    printFile.close()