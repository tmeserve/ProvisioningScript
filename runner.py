import glob, sys, provisioning, serial, os, time
from constants import (AccountID, GroupId, cursor, 
baudrate, apn, server, port, setThreshold, idlethreshold)
from sql import (GetLastDeviceIdByRange, InsertInitialAsset,
InsertInitialDevice, UpdateDeviceProvisioned, Aurora_InsertNote,
GetDeviceByDeviceId)
import datetime
import asyncio
import ftplib
from printing import printlabel
import xml.etree.ElementTree as ET

lastDeviceID = -1

# Gets the available comports/serial ports
def getDeviceLocation():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Useless as of right now but is supposed to rename a file
def rename_open_file(fileobj, newname):
    name = fileobj.name
    mode = fileobj.mode.lower()
    # posn = fileobj.tell()
    fileobj.close()
    os.rename(name, newname)
    newmode = mode
    if "w" in mode:      # can't reopen with "w" mode since
        newmode = "r+"   # it would empty the file; use "r+"
        if "b" in mode:
           newmode += "b"
    fileobj = open(newname, newmode)
    # fileobj.seek(posn)
    return fileobj

# Gets the directory needed.
def getDir(folderName):
    for item in glob.glob(cwd + "/*"):
        if folderName in item and os.path.isdir(item):
            return item
    while True:
        print("Couldn't find the {0} directory.".format(folderName))
        scriptLoc = input("Please enter the script location. ")
        if os.path.isdir(scriptLoc):
            return scriptLoc

def dictToDict(diction, dicttoconvert):
    count = 1
    for item in diction:
        if isinstance(item, str):
            toPrint = str(count) + " - " + item
        else:
            toPrint = str(item[0]) + " - " + item[1].split("/")[-1]
            item = item[1]

        print(str(toPrint))
        dicttoconvert[str(count)] = item
        count += 1
    return dicttoconvert

if __name__ == '__main__':
    cwd = os.getcwd()
    if os.path.isfile(cwd + "/preferences.xml"):
        root = ET.parse(cwd + "/preferences.xml").getroot()
        tree = ET.ElementTree(root)
    else:
        root = ET.Element("preferences")
        root.set('config-port', "")
        root.set('printer-port', "")
        root.set('label-copies', "1")
        tree = ET.ElementTree(root)
        # root.close()s
        tree.write(cwd + "/preferences.xml")
        root = tree.getroot()
    pathToCreate = cwd + "/uploadFiles"
    if not os.path.isdir(pathToCreate):
        os.mkdir(pathToCreate)
    
    extension = ".config.txt"
    fileNameTmp = "tmpLog" + extension
    fileToCreate = pathToCreate + "/" + fileNameTmp
    inp1 = True
    inp2 = True
    inp3 = True
    inp4 = True
    inp5 = True
    inp6 = True
    inp7 = True
    inp8 = True
    isNew = False
    scripts = {"scripts" : []}
    params = {"params": []}
    scriptsToSelect = {}
    devicesToSelect = {}
    paramsToSelect = {}
    # device = ""
    script = ""
    scriptFile = ""
    paramsFile = ""
    inp = ""
    count = 1
    count2 = 1
    count3 = 1
    initials = input("Please input your initials. ")

    while inp1:
        inp = input("Is it a new or existing device? ")
        if inp.lower() == "new":
            model = ""
            while inp2:
                model = input("Is it an MT-4100 or MT-3060? ")
                if model.lower() == "mt-4100":
                    inp2 = False
                    setThreshold(300)
                    # 41000000
                    deviceid = GetLastDeviceIdByRange(41000000, 41999999) + 1
                elif model.lower() == "mt-3060":
                    inp2 = False
                    setThreshold(2)
                    deviceid = GetLastDeviceIdByRange(42000000, 42999999) + 1
                else:
                    print("Please input either MT-4100 or MT-3060.")
                    continue
            print("The deviceid is: ", deviceid)
            imei = input("Please enter the IMEI for the device. ")
            while inp6:
                iccid = input("Please enter the ICCID for the device. ")
                if len(iccid) == 20:
                    inp1 = False
                    inp6 = False
                else:
                    print("Please input a valid ICCID.")
            fileToUpload = open(fileToCreate, 'a')
            fileToUpload.write("Creating new device - {0}.\r\n".format(deviceid))
            InsertInitialDevice(deviceid, imei, iccid)
            fileToUpload.write("Creating new asset.\r\n")
            InsertInitialAsset(deviceid)
            text = "Device " + str(deviceid) + " created.\r\nAccount: CP Stock\r\n Group: STOCK\r\nIMEI: " + str(imei) + "\r\nICCID: " + str(iccid) + "\r\n"
            fileToUpload.write("Aurora Note Added.\r\n")
            Aurora_InsertNote(deviceid, initials, text)
            fileToUpload.close()
            isNew = True
        elif inp.lower() == "existing":
            deviceid = input("Please enter the deviceid. ")
            deviceInfo = GetDeviceByDeviceId(deviceid)
            print("The account name is {0}.\nThe group name is {1}.\nThe IMEI is {2}."
                .format(deviceInfo[0][0], deviceInfo[0][1], deviceInfo[0][6]))
            isCorrect = input("Is that correct so far? ")
            imei = deviceInfo[0][6]
            if isCorrect.lower() == 'yes':
                print("The ICCID is {0}".format(deviceInfo[0][7]))
                iccidCorrect = input("Is the ICCID correct? ")
                if iccidCorrect.lower() == 'no':
                    while inp6:
                        iccid = input("Please enter the ICCID for the device. ")
                        if len(iccid) == 20:
                            inp1 = False
                            inp6 = False
                        else:
                            print("Please input a valid ICCID.")
                elif iccidCorrect.lower() == 'yes':
                    inp1 = False
            elif isCorrect.lower() == 'no':
                while inp6:
                    exit = input("Would you like to exit?")
                    if exit.lower() == "yes":
                        inp1 = False
                        inp6 = False
                    elif exit.lower() == 'no':
                        inp6 = False
                        inp1 = True
        else:
            print("Please enter either new or existing.")
    if not root.attrib.get("config-port") and not root.attrib.get("printer-port"):
        devices = getDeviceLocation()
        devicesToSelect = dictToDict(devices, devicesToSelect)
        while inp4:
            configDeviceLocNumber = input("Please enter a number corresponding to the wanted COM Port for the config device. ")
            if configDeviceLocNumber in devicesToSelect:
                device = devicesToSelect.get(configDeviceLocNumber)
                inp4 = False
        printerDevice = input("Please enter the name of the printer.")
        while inp8:
            labelsToPrint = input("Please enter a number for the amount of labels to print. ")
            if labelsToPrint.isdigit():
                inp8 = False

        root.set('config-port', device)
        root.set('printer-port', printerDevice)
        root.set('label-copies', labelsToPrint)
        tree.write(cwd + "/preferences.xml")
    else:
        device = root.attrib.get("config-port")
        printerDevice = root.attrib.get("printer-port")
        labelsToPrint = root.attrib.get("label-copies")
    script = getDir("scripts")
    filesInDir = []
    for f in os.listdir(script):
        path = os.path.join(script, f)
        if os.path.isfile(path):
            filesInDir.append(path)
    for file in filesInDir:
        scripts.get("scripts").append([count, file])
        count += 1
        
    scriptss = scripts.get("scripts")
    scriptsToSelect = dictToDict(scriptss, scriptsToSelect)
    while inp3:
        scriptFileNumber = input("Please enter a number corresponding to the wanted script to provision the device. ")

        if scriptFileNumber in scriptsToSelect:
            scriptFile = scriptsToSelect.get(scriptFileNumber)
            inp3 = False
        else:
            scriptFileNumberBottom = scriptss[-1][0]
            scriptFileNumberTop = scriptss[0][0]
            print("\nPlease input a number between {1} and {0}."
            .format(scriptFileNumberBottom, scriptFileNumberTop))
    
    param = getDir("params")
    filesInDir = []
    for f in os.listdir(param):
        path = os.path.join(param, f)
        if os.path.isfile(path):
            filesInDir.append(path)
    for file in filesInDir:
        params.get("params").append([count3, file])
        count3 += 1
    
    paramss = params.get("params")
    paramsToSelect = dictToDict(paramss, paramsToSelect)
    while inp5:
        paramsFileNumber = input("Please enter a number corresponding to the wanted params_kore file to provision the device with. ")
        if paramsFileNumber in paramsToSelect:
            paramsFile = paramsToSelect.get(paramsFileNumber)
            inp5 = False
        else:
            paramsFileNumberBottom = paramss[-1][0]
            paramsFileNumberTop = params[0][0]
            print("\nPlease enter a number between {1} and {0}."
                .format(paramsFileNumberBottom, paramsFileNumberTop))
    
    provisioning.getFirmware(fileToCreate, device)
    provisioning.getPackage(fileToCreate, device)
    result = provisioning.Run(device, scriptFile, deviceid, paramsFile, fileToCreate)
    if result == 1:
        datenow =  datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        logFileName = str(deviceid) + "-" + datenow + extension
        fileToRename = open(fileToCreate, "a")
        scriptFileStripped = scriptFile.split("/")
        fileToRename.write("Updating device post-provisioning.\r\n")
        UpdateDeviceProvisioned(datenow, deviceid, apn, server, port, scriptFileStripped[-1], logFileName)
        text = "Device " + str(deviceid) + " configured. <a target=\"_blank\" href=\"http://www.cphandheld.com/VectorConfigWS/ConfigLogs/" + logFileName + "\">View File</a>"
        fileToRename.write("Aurora Note Added.\r\n")
        Aurora_InsertNote(deviceid, initials, text)
        if isNew:
            printlabel(printerDevice, str(deviceid), str(imei))
            fileToRename.write("Label Printed")
        fileToRename.write("Sending log file via ftp.\r\n")
        fileToRename.close()
        os.rename(fileToCreate, pathToCreate + "/" + logFileName)
        fileToUpload = open(pathToCreate + "/" + logFileName, 'rb')
        ftp = ftplib.FTP('ftp.cphandheld.com', 'provisioning', 'ProvFtp$')
        ftp.storbinary('STOR {0}'.format(logFileName), fileToUpload)
        time.sleep(1)
        fileToUpload.close()
        ftp.close()
        print("Fully completed provisioning and device set up.")