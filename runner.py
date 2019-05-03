import glob, sys, provisioning, serial, os, time
from constants import (AccountID, GroupId, 
baudrate, apn, server, port, setThreshold, idlethreshold, getFTP,
setupFTPInformation, setupSQLInformation)
from sql import (GetLastDeviceIdByRange, InsertInitialAsset,
InsertInitialDevice, UpdateDeviceProvisioned, Aurora_InsertNote,
GetDeviceByDeviceId)
import datetime
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

def getICCID():
    inp6 = True
    while inp6:
        iccid = input("Please enter the ICCID for the device. ")
        if len(iccid) == 20:
            inp6 = False
        else:
            print("Please input a valid ICCID.")
    return iccid

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

# Converts a list into a dictionary
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

# Runs the script
if __name__ == '__main__':
    setupFTPInformation()
    setupSQLInformation()
    cwd = os.getcwd()
    ftp = getFTP()
    # Retrieves the xml file
    if os.path.isfile(cwd + "/preferences.xml"):
        root = ET.parse(cwd + "/preferences.xml").getroot()
        tree = ET.ElementTree(root)
    else:
        # Sets up the xml file
        root = ET.Element("preferences")
        root.set('config-port', "")
        root.set('printer-port', "")
        root.set('label-copies', "1")
        root.set('href', "")
        tree = ET.ElementTree(root)
        tree.write(cwd + "/preferences.xml")
        root = tree.getroot()
    
    pathToCreate = cwd + "/uploadFiles"
    # Makes the directory
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
            while inp2:
                model = input("Is it an MT-4100 or MT-3060? ")
                if model.lower() == "mt-4100":
                    inp2 = False
                    setThreshold(300)
                    # Grabs the last device id and adds 1
                    deviceid = GetLastDeviceIdByRange(41000000, 41999999) + 1
                elif model.lower() == "mt-3060":
                    inp2 = False
                    setThreshold(2)
                    # Grabs the last device id and adds 1
                    deviceid = GetLastDeviceIdByRange(42000000, 42999999) + 1
                else:
                    print("Please input either MT-4100 or MT-3060.")
                    continue
            print("The deviceid is: ", deviceid)
            imei = input("Please enter the IMEI for the device. ")
            # Retrieves the iccid
            iccid = getICCID()
            inp1 = False
            fileToUpload = open(fileToCreate, 'a')
            # Writes to the file that needs to be uploaded
            fileToUpload.write("Creating new device - {0}.\r\n".format(deviceid))
            # Calls an SQL command and pushes to the db
            InsertInitialDevice(deviceid, imei, iccid)
            # Writes to the file that needs to be uploaded
            fileToUpload.write("Creating new asset.\r\n")
            # Calls an SQL command and pushes to the db
            InsertInitialAsset(deviceid)
            text = "Device " + str(deviceid) + " created.\r\nAccount: CP Stock\r\n Group: STOCK\r\nIMEI: " + str(imei) + "\r\nICCID: " + str(iccid) + "\r\n"
            # Writes to the file that needs to be uploaded
            fileToUpload.write("Aurora Note Added.\r\n")
            # Calls an SQL command and pushes to the db
            Aurora_InsertNote(deviceid, initials, text)
            # Closes the file
            fileToUpload.close()
            isNew = True
        elif inp.lower() == "existing":
            deviceid = input("Please enter the deviceid. ")
            # Gets all of a devices information by the id
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
                    exit = input("Would you like to create a new one or exit? Type exit to exit or new to create a new device.")
                    if exit.lower() == "exit":
                        inp1 = False
                        inp6 = False
                        sys.exit()
                    elif exit.lower() == 'new':
                        while inp2:
                            model = input("Is it an MT-4100 or MT-3060? ")
                            if model.lower() == "mt-4100":
                                inp2 = False
                                setThreshold(300)
                                # 41000000
                                # Gets the last device id and adds 1
                                deviceid = GetLastDeviceIdByRange(41000000, 41999999) + 1
                            elif model.lower() == "mt-3060":
                                inp2 = False
                                setThreshold(2)
                                # Gets the last device id and adds 1
                                deviceid = GetLastDeviceIdByRange(42000000, 42999999) + 1
                            else:
                                print("Please input either MT-4100 or MT-3060.")
                                continue
                        print("The deviceid is: ", deviceid)
                        imei = input("Please enter the IMEI for the device. ")
                        # Retrieves the ICCID
                        iccid = getICCID()
                        inp1 = False
                        fileToUpload = open(fileToCreate, 'a')
                        # Writes to the file
                        fileToUpload.write("Creating new device - {0}.\r\n".format(deviceid))
                        # Calls an SQL command and pushes it to the db
                        InsertInitialDevice(deviceid, imei, iccid)
                        # Writes to the file
                        fileToUpload.write("Creating new asset.\r\n")
                        # Calls an SQL command and pushes it to the db
                        InsertInitialAsset(deviceid)
                        # Writes to the file
                        text = "Device " + str(deviceid) + " created.\r\nAccount: CP Stock\r\n Group: STOCK\r\nIMEI: " + str(imei) + "\r\nICCID: " + str(iccid) + "\r\n"
                        # Writes to the file
                        fileToUpload.write("Aurora Note Added.\r\n")
                        # Calls an SQL command and pushes it to the db
                        Aurora_InsertNote(deviceid, initials, text)
                        # Closes the file
                        fileToUpload.close()
                        isNew = True
        else:
            print("Please enter either new or existing.")
    if not root.attrib.get("config-port") and not root.attrib.get("printer-port") and not root.attrib.get('lable-copies') and root.attrib.get('href'):
        print("Getting available COM ports to choose from.")
        # Gets the COM Port
        devices = getDeviceLocation()
        # Converts the device list to a dictionary
        devicesToSelect = dictToDict(devices, devicesToSelect)
        while inp4:
            configDeviceLocNumber = input("Please enter a number corresponding to the wanted COM Port for the config device. ")
            # Checks if the input is in device dictionary
            if configDeviceLocNumber in devicesToSelect:
                # Sets device to the input
                device = devicesToSelect.get(configDeviceLocNumber)
                inp4 = False
        while inp7:
            printerDeviceLocNumber = input("Please enter a number corresponding to the wanted COM Port for the printer. ")
            # Checks if the input is in device dictionary
            if printerDeviceLocNumber in devicesToSelect and not printerDeviceLocNumber == configDeviceLocNumber:
                # Sets the printer device to the input
                printerDevice = devicesToSelect.get(printerDeviceLocNumber)
                inp7 = False
            if printerDeviceLocNumber == configDeviceLocNumber:
                print("Printer and config device number should not be the same. ")
        while inp8:
            labelsToPrint = input("Please enter a number for the amount of labels to print. ")
            # Checks if the input is a digit
            if labelsToPrint.isdigit():
                inp8 = False
        
        print("Please enter the link to access the config logs. ")
        print("IE: ")
        print("https://example.com/vector/configlogs")
        print("Please note that it will add the forward slash for you and the file name. ")
        href = input("What is the link to access the config logs? ")
        # Stores the settings for later use
        root.set('config-port', device)
        root.set('printer-port', printerDevice)
        root.set('label-copies', labelsToPrint)
        root.set('href', href)
        tree.write(cwd + "/preferences.xml")
    else:
        # Gets the stored values
        device = root.attrib.get("config-port")
        printerDevice = root.attrib.get("printer-port")
        labelsToPrint = root.attrib.get("label-copies")
        href = root.attrib.get("href")
        # If they had modified the xml file and isn't a digit then
        # it makes them input it again
        if not labelsToPrint.isdigit():
            while inp8:
                labelsToPrint = input("Please enter a number for the amount of labels to print. ")
                if labelsToPrint.isdigit():
                    inp8 = False
                else:
                    print("Please enter a number.")
            root.set("label-copies", labelsToPrint)
            tree.write(cwd + "/preferences.xml")
    # Gets the script directory
    script = getDir("scripts")
    filesInDir = []
    # Converts the files of the directory into a list
    for f in os.listdir(script):
        path = os.path.join(script, f)
        if os.path.isfile(path):
            filesInDir.append(path)
    # Converts the list into a dictionary
    for file in filesInDir:
        scripts.get("scripts").append([count, file])
        count += 1
        
    scriptss = scripts.get("scripts")
    scriptsToSelect = dictToDict(scriptss, scriptsToSelect)
    while inp3:
        scriptFileNumber = input("Please enter a number corresponding to the wanted script to provision the device. ")
        # Gets the wanted script
        if scriptFileNumber in scriptsToSelect:
            scriptFile = scriptsToSelect.get(scriptFileNumber)
            inp3 = False
        else:
            scriptFileNumberBottom = scriptss[-1][0]
            scriptFileNumberTop = scriptss[0][0]
            print("\nPlease input a number between {1} and {0}."
            .format(scriptFileNumberBottom, scriptFileNumberTop))
    # Gets the params directory
    param = getDir("params")
    filesInDir = []
    # Converts the files into a list from the directory
    for f in os.listdir(param):
        path = os.path.join(param, f)
        if os.path.isfile(path):
            filesInDir.append(path)
    # Converts the list into a dictionary
    for file in filesInDir:
        params.get("params").append([count3, file])
        count3 += 1
    
    paramss = params.get("params")
    paramsToSelect = dictToDict(paramss, paramsToSelect)
    while inp5:
        paramsFileNumber = input("Please enter a number corresponding to the wanted params_kore file to provision the device with. ")
        # Gets the wanted params file
        if paramsFileNumber in paramsToSelect:
            paramsFile = paramsToSelect.get(paramsFileNumber)
            inp5 = False
        else:
            paramsFileNumberBottom = paramss[-1][0]
            paramsFileNumberTop = params[0][0]
            print("\nPlease enter a number between {1} and {0}."
                .format(paramsFileNumberBottom, paramsFileNumberTop))
    # Gets the firmware version
    provisioning.getFirmware(fileToCreate, device)
    # Gets the package version
    provisioning.getPackage(fileToCreate, device)
    # Provisions the device
    result = provisioning.Run(device, scriptFile, deviceid, paramsFile, fileToCreate)
    # Checks if the device properly connected and set up
    finalCheck = provisioning.finalCheck(device, fileToCreate)
    if result == 1 and finalCheck:
        # Gets the time and date
        datenow =  datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        logFileName = str(deviceid) + "-" + datenow + extension
        fileToRename = open(fileToCreate, "a")
        scriptFileStripped = scriptFile.split("/")
        # Writes to the file
        fileToRename.write("Updating device post-provisioning.\r\n")
        # Updates the device in the db
        UpdateDeviceProvisioned(datenow, deviceid, apn, server, port, scriptFileStripped[-1], logFileName)
        text = "Device " + str(deviceid) + " configured. <a target=\"_blank\" href=\"{0}/".format(href) + logFileName + "\">View File</a>"
        # Writes to the file
        fileToRename.write("Aurora Note Added.\r\n")
        # Inserts the note to the db for customer viewing
        Aurora_InsertNote(deviceid, initials, text)
        if isNew:
            # Prints the label
            printlabel(printerDevice, str(deviceid), str(imei), labelsToPrint)
            # Writes to the file
            fileToRename.write("Label Printed.\r\n")
        # Writes to the file
        fileToRename.write("Sending log file via ftp.\r\n")
        # Closes the file
        fileToRename.close()
        # Renames the file
        os.rename(fileToCreate, pathToCreate + "/" + logFileName)
        fileToUpload = open(pathToCreate + "/" + logFileName, 'rb')
        # Uploads the file through ftp
        ftp.storbinary('STOR {0}'.format(logFileName), fileToUpload)
        time.sleep(1)
        # Closes the file
        fileToUpload.close()
        # Ends connection with the ftp server
        ftp.close()
        print("Fully completed provisioning and device set up.")
    elif not finalCheck:
        print("The GPS Signal couldn't be retrieved. Or the cellular lock couldn't be verified.")