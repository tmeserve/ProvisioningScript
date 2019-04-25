import serial, time
i = 1
printFile = open("../Template.txt", "r")
lines = printFile.readlines()
lineStr = "".join(lines)
# lineStr = lineStr.replace("{DEVICEID}", deviceid).replace("{IMEI}", imei).replace("{FIRMWARE}", getFirmware()).replace("{PACKAGE}", getPackage())
ser = serial.Serial("/dev/tty.UC-232AC4", 9600)
if ser.isOpen():
    ser.close()
ser.open()

while i <= int(1):
    ser.write(lineStr.encode())
    ser.flush()
    time.sleep(2)
    i += 1

ser.close()
printFile.close()