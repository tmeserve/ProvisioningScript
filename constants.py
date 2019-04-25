import os, ftplib, time
from pyodbc import connect, drivers
import xml.etree.ElementTree as ET

AccountID = "3B71BE1C-460F-437D-BEAB-6A1380940C86"
GroupId = "E5680B2F-662F-4EEE-B0F8-44417135AF15"

ftp = None
conn = None
cursor = None

baudrate=115200
apn="c1.korem2m.com"
server="gps1.engenx.com"
port=1721

def setConn(connection):
    global conn
    conn = connection

def getCursor():
    global cursor
    return cursor

def setCursor(curs):
    global cursor
    cursor = curs

def getFTP():
    global ftp
    return ftp

def setFTP(ft):
    global ftp
    ftp = ft

idlethreshold = 0

def getThreshold():
    global idlethreshold
    return idlethreshold

def setThreshold(threshold):
    idlethreshold = threshold

firmware = None

def getFirmware():
    global firmware
    return firmware

def setFirmware(firm):
    global firmware
    firmware = firm

package = None

def getPackage():
    global package
    return package

def setPackage(pack):
    global package
    package = pack

def setupSQLInformation():
    cwd = os.getcwd()
    global conn, cursor
    inp1 = True
    inp2 = True
    inp3 = True
    inp4 = True
    if os.path.isfile(cwd + "/SQL.xml"):
        root = ET.parse(cwd + "/SQL.xml").getroot()
        tree = ET.ElementTree(root)
    else:
        root = ET.Element('SQL')
        root.set('driver', '')
        root.set('username', '')
        root.set('password', '')
        root.set('server', '')
        root.set('database', '')
        tree = ET.ElementTree(root)
        tree.write(cwd + '/SQL.xml')
        root = tree.getroot()
    if not root.attrib.get('driver') \
        and not root.attrib.get('username') \
        and not root.attrib.get('password') \
        and not root.attrib.get('server') \
        and not root.attrib.get('database'):
        while inp1:
            print("Please enter the driver you'd like to use for the SQL server.")
            print("If you type default it will be:")
            print("{ODBC Driver 17 for SQL Server}")
            print("If you would like a list of available drivers.")
            print("Please type 'list'.")
            print("Otherwise enter another valid driver.")
            time.sleep(3)
            driverInput = input("Please enter a valid option for the driver.")
            if driverInput.lower() == "list":
                for driverOption in drivers():
                    print(driverOption)
            elif driverInput.lower() == "default":
                if "ODBC Driver 17 for SQL Server" in drivers():
                    driver = "{ODBC Driver 17 for SQL Server}"
                    root.set('driver', driver)
                    inp1 = False
                else:
                    print("Couldn't find the default option:")
                    print("{ODBC Driver 17 for SQL Server}")
                    print("As a valid driver installed.")
            elif driverInput in drivers():
                driver = "{" + driverInput + "}"
                inp1 = False
                root.set('driver', driver)
            time.sleep(2)
        username = input("Please enter the username to upload to the SQL server. ")
        root.set('username', username)
        password = input("Please enter the password for the database. ")
        root.set('password', password)
        server = input("Please enter the server IP of the database. ")
        root.set('server', server)
        database = input("Please enter the name of the database you want to upload the files to. ")
        root.set('database', database)
        tree.write(cwd + "/SQL.xml")
        setToCon = connect(driver=driver,
                    uid=username,
                    password=password,
                    server=server,
                    database=database,
                    autocommit=True)
        setConn(setToCon)
        setCursor(setToCon.cursor())
    else:
        setToCon = connect(driver=root.attrib.get('driver'),
                uid=root.attrib.get('username'),
                password=root.attrib.get('password'),
                server=root.attrib.get('server'),
                database=root.attrib.get('database'),
                autocommit=True)
        setConn(setToCon)
        setCursor(setToCon.cursor())

def setupFTPInformation():
    cwd = os.getcwd()
    global ftp
    if os.path.isfile(cwd + "/FTP.xml"):
        root = ET.parse(cwd + "/FTP.xml").getroot()
        tree = ET.ElementTree(root)
    else:
        root = ET.Element('FTP')
        root.set('IP', '')
        root.set('username', '')
        root.set('password', '')
        tree = ET.ElementTree(root)
        tree.write(cwd + "/FTP.xml")
        root = tree.getroot()
    
    if not root.attrib.get('IP') \
        or not root.attrib.get('username') \
        or not root.attrib.get('password'):
        if not root.attrib.get('IP'):
            ip = input("Please enter the IP for the ftp server. ")
            root.set('IP', ip)
        if not root.attrib.get('username'):
            username = input("Please enter the username for the FTP server. ")
            root.set('username', username)
        if not root.attrib.get('password'):
            password = input("Please enter the password for the FTP server. ")
            root.set('password', password)
        tree.write(cwd + "/FTP.xml")
    else:
        ip = root.attrib.get('IP')
        username = root.attrib.get('username')
        password = root.attrib.get('password')
    
    ftp = ftplib.FTP(ip, username, password)