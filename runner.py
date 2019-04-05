import glob, sys, provisioning, serial, os, time
from constants import (AccountID, GroupId, cursor, cwd, 
baudrate, apn, server, port, setThreshold, idlethreshold)
from sql import (GetLastDeviceIdByRange, InsertInitialAsset,
InsertInitialDevice, UpdateDeviceProvisioned, Aurora_InsertNote,
GetDeviceByDeviceId)
import datetime
import asyncio
import ftplib

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

# Uploads the file to the ftp server before moving on
@asyncio.coroutine
async def uploadFileToFTP(fileName, fileobj):
    print("Before")
    await ftp.storbinary('STOR {0}'.format(fileName), fileobj)
    print("After")

if __name__ == '__main__':
    cwd = os.getcwd()
    pathToCreate = cwd + "/uploadFiles"
    if not os.path.isdir(pathToCreate):
        os.mkdir(pathToCreate)
    extension = ".config.txt"
    fileNameTmp = "tmpLog" + extension
    fileToCreate = pathToCreate + "/" + fileNameTmp
    provisioning.getFirmware(fileToCreate)
    provisioning.getPackage(fileToCreate)
    inp1 = True
    inp2 = True
    inp3 = True
    inp4 = True
    inp5 = True
    inp6 = True
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
        inp = input("Is it a new or existing device? Type exit to exit the script.")
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
            InsertInitialDevice(deviceid, imei, iccid)
            InsertInitialAsset(deviceid)
            text = "Device " + str(deviceid) + " created.\r\nAccount: CP Stock\r\n Group: STOCK\r\nIMEI: " + str(imei) + "\r\nICCID: " + str(iccid) + "\r\n"
            Aurora_InsertNote(deviceid, initials, text)
        elif inp.lower() == "existing":
            deviceid = input("Please enter the deviceid. ")
            device = GetDeviceByDeviceId(deviceid)
            print("The account name is {0}.\nThe group name is {1}.\nThe IMEI is {2}."
                .format(device[0][0], device[0][1], device[0][6]))
            isCorrect = input("Is that correct so far? ")

            if isCorrect.lower() == 'yes':
                print("The ICCID is {0}".format(device[0][7]))
                iccidCorrect = input("Is the ICCID correct?")
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
    devices = getDeviceLocation()
    devicesToSelect = dictToDict(devices, devicesToSelect)
    while inp4:
        deviceLocNumber = input("Please enter a number corresponding to the wanted device. ")
        if deviceLocNumber in devicesToSelect:
            device = devicesToSelect.get(deviceLocNumber)
            inp4 = False
    
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
    
    result = provisioning.Run(device, scriptFile, deviceid, paramsFile, fileToCreate)
    if result == 1:
        datenow =  datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        logFileName = str(deviceid) + "-" + datenow + extension
        fileToRename = open(fileToCreate, "rb")
        fileToRename.close()
        os.rename(fileToCreate, pathToCreate + "/" + logFileName)
        print(logFileName, " is log file name")
        fileToUpload = open(pathToCreate + "/" + logFileName, 'rb')
        # asyncio.run(uploadFileToFTP(logFileName, fileToUpload))
        ftp = ftplib.FTP('ftp.cphandheld.com', 'provisioning', 'ProvFtp$')
        ftp.storbinary('STOR {0}'.format(logFileName), fileToUpload)
        time.sleep(1)
        fileToUpload.close()
        ftp.close()
        UpdateDeviceProvisioned(datenow, deviceid, apn, server, port, fileToUpload, logFileName)
        text = "Device " + str(deviceid) + " configured. <a target=\"_blank\" href=\"http://www.cphandheld.com/VectorConfigWS/ConfigLogs/" + logFileName + "\">View File</a>"
        Aurora_InsertNote(deviceid, initials, text)
        print("Fully completed provisioning and device set up.")